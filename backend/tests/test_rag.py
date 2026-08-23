from app.rag import retrieve
def test_retrieval_preserves_official_metadata():
    source=retrieve("KYC bank verification")[0]
    assert source.document_id and "epfindia.gov.in" in source.url and source.section
def test_no_relevant_result(): assert retrieve("unrelated astrophysics vocabulary") == []
