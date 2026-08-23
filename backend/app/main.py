import logging, uuid
from fastapi import FastAPI, HTTPException, Request, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from . import database
from .ai import OpenAIAdapter, AIProblem
from .domain import CaseData
from .observability import request_id, log
from .rag import retrieve
from .rules import evaluate
from .scenarios import SCENARIOS
from .schemas import *
from .services import infer_scenario, timeline
from .uploads import extract_upload, UploadProblem
logging.basicConfig(level=logging.INFO,format="%(message)s")
app=FastAPI(title="NIVA API",version="0.2.0")
origins=[item for item in __import__('os').getenv("NIVA_CORS_ORIGINS","http://localhost:5173").split(",") if item]
app.add_middleware(CORSMiddleware,allow_origins=origins,allow_credentials=False,allow_methods=["GET","POST"],allow_headers=["Content-Type","X-Request-ID"])
@app.on_event("startup")
def setup(): database.initialise()
@app.middleware("http")
async def correlation(request:Request,call_next):
    request.state.request_id=request.headers.get("X-Request-ID",request_id())
    response=await call_next(request);response.headers["X-Request-ID"]=request.state.request_id;return response
@app.exception_handler(HTTPException)
async def expected_error(request:Request,exc:HTTPException): return JSONResponse(status_code=exc.status_code,content={"error":{"code":"REQUEST_ERROR","message":str(exc.detail)},"request_id":request.state.request_id})
def case_or_404(case_id):
    value=database.get_case(case_id)
    if not value: raise HTTPException(404,"We couldn't find that synthetic case.")
    return value
def output(case_id,record,extraction):
    result=evaluate(record["data"]); sources=retrieve(f"{result.reason_code.value} {record['data'].rejection_reason}")
    explanation=OpenAIAdapter().explain(result,record["data"],sources,record["language"])
    return result,explanation,timeline(result.current_step)
@app.get("/health")
def health(request:Request): return {"status":"ok","request_id":request.state.request_id}
@app.get("/scenarios")
def scenarios(request:Request): return {"scenarios":[{"id":key,"label":value.rejection_reason} for key,value in SCENARIOS.items() if key!="resolved"],"request_id":request.state.request_id}
@app.post("/cases",response_model=CaseCreated,status_code=201)
def create_case(payload:CreateCaseRequest,request:Request):
    if payload.scenario not in SCENARIOS: raise HTTPException(400,"Choose one of the available synthetic scenarios.")
    case_id=str(uuid.uuid4());database.create_case(case_id,SCENARIOS[payload.scenario].model_copy(),payload.language);log("case_created",request.state.request_id,case_id=case_id,scenario=payload.scenario);return CaseCreated(case_id=case_id,request_id=request.state.request_id)
@app.post("/cases/{case_id}/documents",response_model=ExtractionResult)
async def document(case_id:str,request:Request,file:UploadFile=File(...)):
    record=case_or_404(case_id)
    try: text,filename=await extract_upload(file)
    except UploadProblem as exc: raise HTTPException(422,str(exc))
    try: extraction=OpenAIAdapter().extract(text)
    except AIProblem as exc: raise HTTPException(503,str(exc))
    scenario=extraction.scenario_hint or record["scenario"]
    database.update_case(case_id,SCENARIOS[scenario].model_copy(),filename);log("document_processed",request.state.request_id,case_id=case_id,mode=extraction.mode);return extraction
@app.post("/cases/{case_id}/analyze",response_model=AnalysisResponse)
def analyze(case_id:str,payload:AnalyzeRequest,request:Request):
    record=case_or_404(case_id)
    try: extraction=OpenAIAdapter().extract(payload.description)
    except AIProblem as exc: raise HTTPException(503,str(exc))
    scenario=extraction.scenario_hint or record["scenario"]
    if scenario not in SCENARIOS: raise HTTPException(422,"We couldn't understand this synthetic notice. Please choose an issue.")
    data=SCENARIOS[scenario].model_copy();database.update_case(case_id,data);record=case_or_404(case_id);result,explanation,steps=output(case_id,record,extraction);log("case_analyzed",request.state.request_id,case_id=case_id,reason=result.reason_code);return AnalysisResponse(case_id=case_id,extraction=extraction,result=result,explanation=explanation,timeline=steps,request_id=request.state.request_id)
@app.get("/cases/{case_id}",response_model=CaseResponse)
def read_case(case_id:str,request:Request):
    record=case_or_404(case_id);result,explanation,_=output(case_id,record,None);return CaseResponse(case_id=case_id,scenario=record["scenario"],language=record["language"],result=result,explanation=explanation,request_id=request.state.request_id)
@app.get("/cases/{case_id}/timeline",response_model=TimelineResponse)
def read_timeline(case_id:str,request:Request):
    record=case_or_404(case_id);return TimelineResponse(case_id=case_id,timeline=timeline(evaluate(record["data"]).current_step),request_id=request.state.request_id)
@app.post("/cases/{case_id}/questions",response_model=QuestionResponse)
def question(case_id:str,payload:QuestionRequest,request:Request):
    record=case_or_404(case_id);result,explanation,_=output(case_id,record,None);sources=[source.model_dump() for source in explanation.source_references]
    answer=explanation.what_to_do[0] if "what" in payload.question.lower() or "do" in payload.question.lower() else explanation.why
    return QuestionResponse(answer=answer,sources=sources,request_id=request.state.request_id)
