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
