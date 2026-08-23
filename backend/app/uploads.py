from pathlib import Path
import tempfile
from fastapi import UploadFile
from pypdf import PdfReader
MAX_UPLOAD_BYTES=5*1024*1024; ALLOWED={"application/pdf":".pdf","image/png":".png","image/jpeg":".jpg"}
class UploadProblem(Exception): pass
async def extract_upload(upload:UploadFile)->tuple[str,str]:
    content=await upload.read()
    filename=upload.filename or "synthetic-notice"
    generic_pdf=upload.content_type=="application/octet-stream" and filename.lower().endswith(".pdf") and content.startswith(b"%PDF-")
    if upload.content_type not in ALLOWED and not generic_pdf: raise UploadProblem("Please upload a PDF, PNG, or JPEG synthetic notice.")
    if not content: raise UploadProblem("This file is empty. Try another synthetic notice.")
    if len(content)>MAX_UPLOAD_BYTES: raise UploadProblem("This file is larger than 5 MB. Try a smaller synthetic notice.")
    suffix=".pdf" if generic_pdf else ALLOWED[upload.content_type]
    with tempfile.NamedTemporaryFile(suffix=suffix,delete=False) as temp: temp.write(content); path=Path(temp.name)
    try:
        if suffix!=".pdf": raise UploadProblem("Image reading is not enabled in this prototype yet. Please upload a text-based PDF.")
        try: text="\n".join(page.extract_text() or "" for page in PdfReader(str(path)).pages).strip()
        except Exception as exc: raise UploadProblem("We couldn't read this PDF. Try another synthetic notice.") from exc
        if not text: raise UploadProblem("This PDF has no readable text. Try a text-based synthetic PDF.")
        return text,filename
    finally: path.unlink(missing_ok=True)
