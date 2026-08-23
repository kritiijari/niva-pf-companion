"""Validate reviewed official-source metadata and rebuild the local vector index."""
from pathlib import Path
import sys
PROJECT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(PROJECT/"backend"))
ROOT=PROJECT/"knowledge"/"documents"
for path in ROOT.glob("*.md"):
    text=path.read_text(encoding="utf-8")
    if "epfindia.gov.in" not in text: raise SystemExit(f"Unverified source domain: {path.name}")
    print(f"validated {path.name}")
from app.rag import build_index
print(f"indexed {len(build_index())} document chunks")
