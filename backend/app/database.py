import os, sqlite3
from pathlib import Path
from .domain import CaseData, Language
DB_PATH=Path(os.getenv("NIVA_DATABASE_PATH", Path(__file__).resolve().parents[1]/"niva.db"))
def initialise(path: Path=DB_PATH):
    path.parent.mkdir(parents=True,exist_ok=True)
    with sqlite3.connect(path) as conn: conn.execute("CREATE TABLE IF NOT EXISTS cases (id TEXT PRIMARY KEY, scenario TEXT NOT NULL, language TEXT NOT NULL, case_json TEXT NOT NULL, uploaded_filename TEXT, created_at TEXT DEFAULT CURRENT_TIMESTAMP, updated_at TEXT DEFAULT CURRENT_TIMESTAMP)")
def connection(path: Path=DB_PATH):
    conn=sqlite3.connect(path); conn.row_factory=sqlite3.Row; return conn
def create_case(case_id:str,data:CaseData,language:Language,path:Path=DB_PATH):
    initialise(path)
    with connection(path) as conn: conn.execute("INSERT INTO cases(id,scenario,language,case_json) VALUES(?,?,?,?)",(case_id,data.scenario,language.value,data.model_dump_json()))
def get_case(case_id:str,path:Path=DB_PATH):
    initialise(path)
    with connection(path) as conn: row=conn.execute("SELECT * FROM cases WHERE id=?",(case_id,)).fetchone()
    return None if not row else {"id":row["id"],"scenario":row["scenario"],"language":Language(row["language"]),"data":CaseData.model_validate_json(row["case_json"]),"uploaded_filename":row["uploaded_filename"]}
def update_case(case_id:str,data:CaseData,filename:str|None=None,path:Path=DB_PATH):
    initialise(path)
    with connection(path) as conn: conn.execute("UPDATE cases SET scenario=?,case_json=?,uploaded_filename=COALESCE(?,uploaded_filename),updated_at=CURRENT_TIMESTAMP WHERE id=?",(data.scenario,data.model_dump_json(),filename,case_id))
