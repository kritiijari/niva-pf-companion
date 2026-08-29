import logging
import uuid

from fastapi import FastAPI, HTTPException, Request, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from . import database
from .ai import OpenAIAdapter, AIProblem
from .observability import request_id, log
from .rag import retrieve
from .rules import evaluate
from .scenarios import SCENARIOS
from .schemas import *
from .services import infer_scenario, infer_issue, timeline
from .uploads import extract_upload, UploadProblem


# ============================================================
# APP SETUP
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
)

app = FastAPI(
    title="NIVA API",
    version="0.2.0",
)

origins = [
    item
    for item in __import__("os")
    .getenv(
        "NIVA_CORS_ORIGINS",
        "http://localhost:5173,http://127.0.0.1:5173",
    )
    .split(",")
    if item
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "X-Request-ID"],
)


# ============================================================
# STARTUP
# ============================================================

@app.on_event("startup")
def setup():
    database.initialise()


# ============================================================
# REQUEST CORRELATION
# ============================================================

@app.middleware("http")
async def correlation(request: Request, call_next):
    request.state.request_id = request.headers.get(
        "X-Request-ID",
        request_id(),
    )

    response = await call_next(request)

    response.headers["X-Request-ID"] = request.state.request_id

    return response


# ============================================================
# EXPECTED ERROR HANDLER
# ============================================================

@app.exception_handler(HTTPException)
async def expected_error(
    request: Request,
    exc: HTTPException,
):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": "REQUEST_ERROR",
                "message": str(exc.detail),
            },
            "request_id": request.state.request_id,
        },
    )


# ============================================================
# HELPERS
# ============================================================

def case_or_404(case_id):
    value = database.get_case(case_id)

    if not value:
        raise HTTPException(
            404,
            "We couldn't find that synthetic case.",
        )

    return value


def output(case_id, record, extraction):
    """
    Run deterministic rules, retrieve supporting sources,
    generate explanation, and construct timeline.
    """

    result = evaluate(record["data"])

    sources = retrieve(
        f"{result.reason_code.value} "
        f"{record['data'].rejection_reason}"
    )

    explanation = OpenAIAdapter().explain(
        result,
        record["data"],
        sources,
        record["language"],
    )

    return (
        result,
        explanation,
        timeline(result.current_step),
    )


def resolve_scenario(description: str, current_scenario: str):
    """
    Convert natural-language input into one of the actual
    keys present in SCENARIOS.

    Example:

        "PF withdrawal rejected because KYC is incomplete"

        infer_scenario -> withdrawal
        infer_issue    -> kyc
        final scenario -> kyc
    """

    # --------------------------------------------------------
    # 1. First try deterministic issue classification.
    # --------------------------------------------------------

    issue = infer_issue(description)

    if issue and issue in SCENARIOS:
        return issue

    # --------------------------------------------------------
    # 2. Try scenario classification.
    #
    # infer_scenario() returns broad workflow categories such
    # as "withdrawal" or "transfer". Those are NOT necessarily
    # SCENARIOS keys, so only accept them when they actually
    # exist in SCENARIOS.
    # --------------------------------------------------------

    scenario = infer_scenario(description)

    if scenario and scenario in SCENARIOS:
        return scenario

    # --------------------------------------------------------
    # 3. Keep the existing case scenario as the final fallback.
    # --------------------------------------------------------

    if current_scenario in SCENARIOS:
        return current_scenario

    return None


# ============================================================
# HEALTH
# ============================================================

@app.get("/health")
def health(request: Request):
    return {
        "status": "ok",
        "request_id": request.state.request_id,
    }


# ============================================================
# SCENARIOS
# ============================================================

@app.get("/scenarios")
def scenarios(request: Request):
    return {
        "scenarios": [
            {
                "id": key,
                "label": value.rejection_reason,
            }
            for key, value in SCENARIOS.items()
            if key != "resolved"
        ],
        "request_id": request.state.request_id,
    }


# ============================================================
# CREATE CASE
# ============================================================

@app.post(
    "/cases",
    response_model=CaseCreated,
    status_code=201,
)
def create_case(
    payload: CreateCaseRequest,
    request: Request,
):
    if payload.scenario not in SCENARIOS:
        raise HTTPException(
            400,
            "Choose one of the available synthetic scenarios.",
        )

    case_data = SCENARIOS[payload.scenario].model_copy(
        update={
            "claim_type": payload.claim_type.value,
        }
    )

    case_id = str(uuid.uuid4())

    database.create_case(
        case_id,
        case_data,
        payload.language,
    )

    log(
        "case_created",
        request.state.request_id,
        case_id=case_id,
        scenario=payload.scenario,
        claim_type=payload.claim_type.value,
    )

    return CaseCreated(
        case_id=case_id,
        request_id=request.state.request_id,
    )


# ============================================================
# DOCUMENT UPLOAD
# ============================================================

@app.post(
    "/cases/{case_id}/documents",
    response_model=ExtractionResult,
)
async def document(
    case_id: str,
    request: Request,
    file: UploadFile = File(...),
):
    record = case_or_404(case_id)

    try:
        text, filename = await extract_upload(file)
    except UploadProblem as exc:
        raise HTTPException(
            422,
            str(exc),
        )

    try:
        extraction = OpenAIAdapter().extract(text)
    except AIProblem as exc:
        raise HTTPException(
            503,
            str(exc),
        )

    # --------------------------------------------------------
    # Resolve the scenario from the extracted text.
    # --------------------------------------------------------

    scenario = resolve_scenario(
        text,
        record["scenario"],
    )

    if not scenario:
        raise HTTPException(
            422,
            "We couldn't understand this synthetic notice. "
            "Please choose an issue.",
        )

    database.update_case(
        case_id,
        SCENARIOS[scenario].model_copy(),
        filename,
    )

    log(
        "document_processed",
        request.state.request_id,
        case_id=case_id,
        mode=extraction.mode,
        scenario=scenario,
    )

    return extraction


# ============================================================
# ANALYZE CASE
# ============================================================

@app.post(
    "/cases/{case_id}/analyze",
    response_model=AnalysisResponse,
)
def analyze(
    case_id: str,
    payload: AnalyzeRequest,
    request: Request,
):
    record = case_or_404(case_id)

    # --------------------------------------------------------
    # 1. Extract information from the user's description.
    # --------------------------------------------------------

    try:
        extraction = OpenAIAdapter().extract(
            payload.description
        )
    except AIProblem as exc:
        raise HTTPException(
            503,
            str(exc),
        )

    # --------------------------------------------------------
    # 2. Resolve the actual SCENARIOS key.
    #
    # IMPORTANT:
    #
    # infer_scenario("PF withdrawal...")
    #     -> "withdrawal"
    #
    # But "withdrawal" is NOT a SCENARIOS key.
    #
    # infer_issue("...KYC verification...")
    #     -> "kyc"
    #
    # "kyc" IS a SCENARIOS key.
    # --------------------------------------------------------

    scenario = resolve_scenario(
        payload.description,
        record["scenario"],
    )

    # --------------------------------------------------------
    # 3. Validate scenario.
    # --------------------------------------------------------

    if not scenario:
        raise HTTPException(
            422,
            "We couldn't understand this synthetic notice. "
            "Please choose an issue.",
        )

    # --------------------------------------------------------
    # 4. Load the corresponding synthetic scenario data.
    # --------------------------------------------------------

    data = SCENARIOS[scenario].model_copy()

    database.update_case(
        case_id,
        data,
    )

    record = case_or_404(case_id)

    # --------------------------------------------------------
    # 5. Run deterministic rules + explanation + timeline.
    # --------------------------------------------------------

    result, explanation, steps = output(
        case_id,
        record,
        extraction,
    )

    # --------------------------------------------------------
    # 6. Log analysis.
    # --------------------------------------------------------

    log(
        "case_analyzed",
        request.state.request_id,
        case_id=case_id,
        reason=result.reason_code,
        scenario=scenario,
    )

    # --------------------------------------------------------
    # 7. Return complete analysis response.
    # --------------------------------------------------------

    return AnalysisResponse(
        case_id=case_id,
        extraction=extraction,
        result=result,
        explanation=explanation,
        timeline=steps,
        request_id=request.state.request_id,
    )


# ============================================================
# READ CASE
# ============================================================

@app.get(
    "/cases/{case_id}",
    response_model=CaseResponse,
)
def read_case(
    case_id: str,
    request: Request,
):
    record = case_or_404(case_id)

    result, explanation, _ = output(
        case_id,
        record,
        None,
    )

    return CaseResponse(
        case_id=case_id,
        scenario=record["scenario"],
        language=record["language"],
        result=result,
        explanation=explanation,
        request_id=request.state.request_id,
    )


# ============================================================
# READ TIMELINE
# ============================================================

@app.get(
    "/cases/{case_id}/timeline",
    response_model=TimelineResponse,
)
def read_timeline(
    case_id: str,
    request: Request,
):
    record = case_or_404(case_id)

    return TimelineResponse(
        case_id=case_id,
        timeline=timeline(
            evaluate(record["data"]).current_step
        ),
        request_id=request.state.request_id,
    )


# ============================================================
# QUESTIONS
# ============================================================

@app.post(
    "/cases/{case_id}/questions",
    response_model=QuestionResponse,
)
def question(
    case_id: str,
    payload: QuestionRequest,
    request: Request,
):
    record = case_or_404(case_id)

    result, explanation, _ = output(
        case_id,
        record,
        None,
    )

    sources = [
        source.model_dump()
        for source in explanation.source_references
    ]

    question_text = payload.question.lower()

    if (
        "what" in question_text
        or "do" in question_text
    ):
        answer = explanation.what_to_do[0]
    else:
        answer = explanation.why

    return QuestionResponse(
        answer=answer,
        sources=sources,
        request_id=request.state.request_id,
    )


# ============================================================
# SERVE FRONTEND (SPA)
# ============================================================

from pathlib import Path
from fastapi.staticfiles import StaticFiles

frontend_dist = Path(__file__).resolve().parents[2] / "frontend" / "dist"

if frontend_dist.exists():
    app.mount("/", StaticFiles(directory=frontend_dist, html=True), name="frontend")