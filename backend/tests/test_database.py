from pathlib import Path
from app.database import create_case, get_case, update_case
from app.domain import Language
from app.scenarios import SCENARIOS
def test_case_persists_across_connections(tmp_path:Path):
    path=tmp_path/"niva.db"; create_case("case-1",SCENARIOS["kyc"],Language.EN,path)
    record=get_case("case-1",path); assert record and record["scenario"]=="kyc"
    update_case("case-1",SCENARIOS["bank"],"notice.pdf",path)
    updated=get_case("case-1",path); assert updated["scenario"]=="bank" and updated["uploaded_filename"]=="notice.pdf"
