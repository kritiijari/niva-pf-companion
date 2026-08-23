# Curated official guidance

The local knowledge pipeline reads reviewed Markdown source records in `documents/`. Each record preserves a document ID, title, official source URL, relevant section, and a short indexed extract. The current included source is **EPFO FAQ on UAN & KYC**: `https://www.epfindia.gov.in/site_docs/PDFs/Circulars/Y2020-2021/FAQUANKYC.pdf`.

Run `python scripts/ingest_knowledge.py` to validate source metadata and rebuild `processed/index.json`. The current prototype uses a small local hashed-vector retriever; it is deliberately labelled as local retrieval, not a live EPFO search. A ChromaDB embedding index can replace this adapter without changing the API contract.
