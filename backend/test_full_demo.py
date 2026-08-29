from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app


c = TestClient(app)


# ---------------------------------------------------------
# 1. BASIC API / ERROR HANDLING
# ---------------------------------------------------------

h = c.get("/health")
assert h.status_code == 200, h.text
print("OK health")

unknown = c.get("/cases/nope")
assert unknown.status_code == 404

body = unknown.json()
assert "error" in body and "message" in body["error"]
assert "Traceback" not in str(body)
print("OK 404 handling")

bad = c.post("/cases", json={"scenario": "not-a-real-scenario"})
assert bad.status_code == 400
assert "error" in bad.json()
print("OK invalid scenario handling")


# ---------------------------------------------------------
# 2. ALL MAJOR NIVA REASON CODES
# ---------------------------------------------------------

cases = [
    (
        "kyc",
        "withdrawal",
        "My PF withdrawal claim was rejected because my KYC verification is incomplete.",
        "KYC_INCOMPLETE",
    ),
    (
        "bank",
        "withdrawal",
        "My PF withdrawal claim was rejected because my bank account details are incorrect.",
        "BANK_VERIFICATION_FAILED",
    ),
    (
        "service",
        "withdrawal",
        "My PF withdrawal claim cannot proceed because employment service information is missing.",
        "SERVICE_INFORMATION_MISSING",
    ),
    (
        "conflict",
        "withdrawal",
        "My PF withdrawal claim was rejected because my personal and PF account details do not match.",
        "INFORMATION_CONFLICT",
    ),
    (
        "ready",
        "withdrawal",
        "My PF withdrawal claim appears ready to continue.",
        "READY_TO_CONTINUE",
    ),
    (
        "transfer_service",
        "transfer",
        "My PF transfer request needs additional information about my previous employment.",
        "TRANSFER_SERVICE_MISSING",
    ),
    (
        "transfer_conflict",
        "transfer",
        "My PF transfer request has a mismatch with my previous employer records.",
        "TRANSFER_INFORMATION_CONFLICT",
    ),
    (
        "transfer_ready",
        "transfer",
        "My PF transfer appears ready to proceed.",
        "TRANSFER_READY",
    ),
]


for scenario, claim, desc, reason in cases:

    created = c.post(
        "/cases",
        json={
            "scenario": scenario,
            "claim_type": claim,
            "language": "en",
        },
    )

    assert created.status_code == 201, created.text

    cid = created.json()["case_id"]

    res = c.post(
        f"/cases/{cid}/analyze",
        json={"description": desc},
    )

    assert res.status_code == 200, res.text

    data = res.json()

    # Correct deterministic outcome
    assert data["result"]["reason_code"] == reason

    # Explanation exists
    expl = data["explanation"]

    assert expl["what_happened"]
    assert expl["what_to_do"]
    assert expl["why"]
    assert expl["title"]

    # Timeline exists
    assert data["timeline"]

    # Extraction object exists
    assert data.get("extraction") is not None

    # Official source exists
    src = expl.get("source_references") or []

    assert src, f"missing source for {reason}"
    assert src[0]["url"].startswith("http")

    print("OK", reason)


# ---------------------------------------------------------
# 3. MULTILINGUAL BACKEND TEST
# ---------------------------------------------------------

for lang in ("en", "hi", "kn"):

    created = c.post(
        "/cases",
        json={
            "scenario": "kyc",
            "claim_type": "withdrawal",
            "language": lang,
        },
    )

    assert created.status_code == 201, created.text

    cid = created.json()["case_id"]

    res = c.post(
        f"/cases/{cid}/analyze",
        json={
            "description": "KYC verification is incomplete",
        },
    )

    assert res.status_code == 200, res.text

    data = res.json()
    expl = data["explanation"]

    assert data["result"]["reason_code"] == "KYC_INCOMPLETE"
    assert expl["language"] == lang
    assert expl["title"]

    print("OK language", lang)


# ---------------------------------------------------------
# 4. SYNTHETIC PDF UPLOAD
# ---------------------------------------------------------

pdf = Path(
    r"C:\Users\Kriti_2\Downloads\niva-pf-companion"
    r"\data\synthetic\kyc-incomplete-notice.pdf"
)

assert pdf.exists(), f"PDF not found: {pdf}"

created = c.post(
    "/cases",
    json={
        "scenario": "kyc",
        "claim_type": "withdrawal",
    },
)

assert created.status_code == 201, created.text

cid = created.json()["case_id"]

with pdf.open("rb") as f:

    up = c.post(
        f"/cases/{cid}/documents",
        files={
            "file": (
                "kyc-incomplete-notice.pdf",
                f,
                "application/pdf",
            )
        },
    )

assert up.status_code == 200, up.text

ext = up.json()

assert ext.get("scenario_hint") == "kyc"

print("OK PDF upload:", ext.get("mode"))


# ---------------------------------------------------------
# 5. PDF + ANALYSIS
# ---------------------------------------------------------

res = c.post(
    f"/cases/{cid}/analyze",
    json={
        "description": "",
    },
)

assert res.status_code == 200, res.text

data = res.json()

assert data["result"]["reason_code"] == "KYC_INCOMPLETE"

print("OK PDF analysis")


# ---------------------------------------------------------
# 6. GENERAL NATURAL-LANGUAGE ANALYSIS
# ---------------------------------------------------------

created = c.post(
    "/cases",
    json={
        "scenario": "kyc",
        "claim_type": "withdrawal",
    },
)

assert created.status_code == 201, created.text

cid = created.json()["case_id"]

res = c.post(
    f"/cases/{cid}/analyze",
    json={
        "description": (
            "My PF claim was rejected because my bank "
            "details could not be verified."
        ),
    },
)

assert res.status_code == 200, res.text

data = res.json()

assert data["result"]["reason_code"] == "BANK_VERIFICATION_FAILED"

print("OK general natural-language bank analysis")


# ---------------------------------------------------------
# FINAL RESULT
# ---------------------------------------------------------

print()
print("=" * 60)
print("ALL NIVA FULL DEMO CHECKS PASSED")
print("=" * 60)