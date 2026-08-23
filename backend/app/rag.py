"""A dependency-free local vector-store adapter for reviewed knowledge records."""
import hashlib, json, math, re
from pathlib import Path
from .domain import SourceReference
ROOT=Path(__file__).resolve().parents[2]/"knowledge"; DOCUMENTS=ROOT/"documents"; INDEX=ROOT/"processed"/"index.json"; DIMENSIONS=128
def embedding(text:str):
    vector=[0.0]*DIMENSIONS
    for term in re.findall(r"[a-z]{3,}",text.lower()): vector[int(hashlib.sha256(term.encode()).hexdigest(),16)%DIMENSIONS]+=1
    length=math.sqrt(sum(item*item for item in vector)) or 1;return [item/length for item in vector]
def _parse(path:Path):
    raw=path.read_text(encoding="utf-8");parts=raw.split("---",2);meta={}
    for line in parts[1].strip().splitlines():
        if ":" in line:key,value=line.split(":",1);meta[key.strip()]=value.strip()
    return {**meta,"excerpt":parts[2].strip()}
def build_index():
    records=[]
    for path in DOCUMENTS.glob("*.md"):
        record=_parse(path);record["embedding"]=embedding(record["section"]+" "+record["excerpt"]);records.append(record)
    INDEX.parent.mkdir(exist_ok=True);INDEX.write_text(json.dumps(records),encoding="utf-8");return records
def retrieve(query:str,limit:int=2)->list[SourceReference]:
    records=json.loads(INDEX.read_text(encoding="utf-8")) if INDEX.exists() else build_index();query_vector=embedding(query);query_terms=set(re.findall(r"[a-z]{3,}",query.lower()));ranked=[]
    for record in records:
        record_terms=set(re.findall(r"[a-z]{3,}",(record["section"]+" "+record["excerpt"]).lower()))
        if not query_terms.intersection(record_terms): continue
        score=sum(a*b for a,b in zip(query_vector,record["embedding"]))
        if score>.08:ranked.append((score,record))
    return [SourceReference(document_id=item["document_id"],title=item["title"],url=item["url"],section=item["section"],excerpt=item["excerpt"]) for _,item in sorted(ranked,reverse=True,key=lambda pair:pair[0])[:limit]]
