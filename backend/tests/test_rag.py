from app.rag import INDEX, retrieve
import json
import pytest
def test_retrieval_preserves_official_metadata():
    source=retrieve("KYC bank verification")[0]
    assert source.document_id and "epfindia.gov.in" in source.url and source.section
def test_no_relevant_result(): assert retrieve("unrelated astrophysics vocabulary") == []

@pytest.mark.parametrize(("query", "title"), [
    ("KYC_INCOMPLETE incomplete KYC", "EPFO FAQ on UAN & KYC"),
    ("SERVICE_INFORMATION_MISSING employment service information", "EPFO Guidance on Employment and Service Information"),
    ("TRANSFER_SERVICE_MISSING previous employment transfer", "EPFO FAQ on Transfer Claims for Employees"),
    ("TRANSFER_INFORMATION_CONFLICT transfer mismatch previous employer", "EPFO FAQ on Transfer Claims for Employees"),
])
def test_retrieval_returns_expected_reviewed_document(query, title):
    assert retrieve(query)[0].title == title

def test_stale_index_is_rebuilt():
    original = INDEX.read_text(encoding="utf-8") if INDEX.exists() else None
    try:
        INDEX.parent.mkdir(parents=True, exist_ok=True)
        INDEX.write_text(json.dumps([{"title": "stale"}]), encoding="utf-8")
        assert retrieve("KYC incomplete")[0].document_id == "epfo-faq-uan-kyc-2020"
    finally:
        if original is None:
            INDEX.unlink(missing_ok=True)
        else:
            INDEX.write_text(original, encoding="utf-8")
