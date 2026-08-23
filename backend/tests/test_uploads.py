import asyncio
from io import BytesIO
from fastapi import UploadFile
from app import uploads
from app.uploads import UploadProblem, extract_upload
def upload(name,content_type,data): return UploadFile(file=BytesIO(data),filename=name,headers={"content-type":content_type})
def test_rejects_invalid_type():
    try: asyncio.run(extract_upload(upload("notice.txt","text/plain",b"no")))
    except UploadProblem as exc: assert "PDF" in str(exc)
    else: assert False
def test_rejects_malformed_pdf():
    try: asyncio.run(extract_upload(upload("notice.pdf","application/pdf",b"not a PDF")))
    except UploadProblem as exc: assert "couldn't read" in str(exc)
    else: assert False
def test_extracts_text_pdf(monkeypatch):
    class Page: 
        def extract_text(self): return "Synthetic KYC verification notice"
    class Reader:
        def __init__(self,path): self.pages=[Page()]
    monkeypatch.setattr(uploads,"PdfReader",Reader)
    text,name=asyncio.run(extract_upload(upload("notice.pdf","application/pdf",b"%PDF-1.4")))
    assert "KYC" in text and name=="notice.pdf"
def test_allows_generic_mime_only_for_pdf_signature(monkeypatch):
    class Page:
        def extract_text(self): return "Synthetic KYC verification notice"
    class Reader:
        def __init__(self,path): self.pages=[Page()]
    monkeypatch.setattr(uploads,"PdfReader",Reader)
    text,_=asyncio.run(extract_upload(upload("notice.pdf","application/octet-stream",b"%PDF-1.4")))
    assert "KYC" in text
def test_rejects_oversize_upload():
    try: asyncio.run(extract_upload(upload("notice.pdf","application/pdf",b"x"*(uploads.MAX_UPLOAD_BYTES+1))))
    except UploadProblem as exc: assert "5 MB" in str(exc)
    else: assert False
