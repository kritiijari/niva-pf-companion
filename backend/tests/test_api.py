from fastapi.testclient import TestClient
from app.main import app
client=TestClient(app)
def test_kyc_journey():
    case=client.post("/cases",json={"scenario":"kyc"}).json()["case_id"]
    response=client.post(f"/cases/{case}/analyze",json={"description":"My claim was rejected, KYC is pending"})
    assert response.status_code==200
    body=response.json(); assert body["result"]["reason_code"]=="KYC_INCOMPLETE"; assert body["timeline"][2]["state"]=="current"
def test_unknown_case(): assert client.get("/cases/nope").status_code==404
def test_timeline_and_question():
    case=client.post("/cases",json={"scenario":"kyc","language":"hi"}).json()["case_id"]
    assert client.get(f"/cases/{case}/timeline").status_code==200
    answer=client.post(f"/cases/{case}/questions",json={"question":"What should I do?"})
    assert answer.status_code==200 and answer.json()["sources"]

def test_all_demo_descriptions_resolve_deterministically():
    cases = [
        ("My PF withdrawal claim was rejected because my KYC verification is incomplete.", "KYC_INCOMPLETE", "EPFO FAQ on UAN & KYC"),
        ("My PF withdrawal claim was rejected because my personal and PF account details do not match.", "INFORMATION_CONFLICT", "EPFO FAQ on UAN & KYC"),
        ("My PF withdrawal claim was rejected because my bank account details are incorrect.", "BANK_VERIFICATION_FAILED", "EPFO FAQ on UAN & KYC"),
        ("My PF withdrawal claim cannot proceed because employment service information is missing.", "SERVICE_INFORMATION_MISSING", "EPFO Guidance on Employment and Service Information"),
        ("My PF transfer request needs additional information about my previous employment.", "TRANSFER_SERVICE_MISSING", "EPFO FAQ on Transfer Claims for Employees"),
        ("My PF transfer request has a mismatch with my previous employer records.", "TRANSFER_INFORMATION_CONFLICT", "EPFO FAQ on Transfer Claims for Employees"),
        ("My PF transfer appears ready to proceed.", "TRANSFER_READY", "EPFO FAQ on Transfer Claims for Employees"),
    ]
    for description, reason, source_title in cases:
        case = client.post("/cases", json={"scenario": "kyc"}).json()["case_id"]
        response = client.post(f"/cases/{case}/analyze", json={"description": description})
        assert response.status_code == 200
        assert response.json()["result"]["reason_code"] == reason
        assert response.json()["explanation"]["source_references"][0]["title"] == source_title

def test_explanations_cover_every_supported_language():
    for language in ("en", "hi", "kn"):
        case = client.post("/cases", json={"scenario": "transfer_ready", "claim_type": "transfer", "language": language}).json()["case_id"]
        response = client.get(f"/cases/{case}")
        assert response.status_code == 200
        explanation = response.json()["explanation"]
        assert explanation["language"] == language
        assert explanation["what_happened"] and explanation["what_to_do"]

def test_cors_allows_both_documented_local_vite_origins():
    for origin in ("http://localhost:5173", "http://127.0.0.1:5173"):
        response = client.options("/cases", headers={
            "Origin": origin,
            "Access-Control-Request-Method": "POST",
        })
        assert response.status_code == 200
        assert response.headers["access-control-allow-origin"] == origin
