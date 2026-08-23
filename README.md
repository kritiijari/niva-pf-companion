# NIVA — Your PF journey, explained.

NIVA is a civic-tech prototype that helps a citizen understand a synthetic PF withdrawal claim problem, explain why it is blocked, and identify the next action. It is not an official EPFO service and does not connect to EPFO.

## Why NIVA

PF claim status language is difficult to act on. NIVA turns a claim issue into a short, grounded journey: **Understand. Fix. Continue.** Its primary user is a former employee like Priya whose synthetic withdrawal claim is rejected.

## Hero journey

1. Choose **My PF claim has a problem**.
2. Choose or describe an issue and optionally add a synthetic notice.
3. NIVA extracts bounded issue information, runs deterministic checks, retrieves locally curated source metadata, and presents what happened, what to do, why, and the derived workflow timeline.

## Architecture

React + TypeScript/Vite provides the mobile-first interface. FastAPI provides case APIs. The authoritative rules engine derives workflow state from synthetic case facts. A small curated guidance catalogue provides source metadata. See [architecture.md](docs/architecture.md).

AI, when an `OPENAI_API_KEY` is later configured, is limited to schema-validated extraction and explanation; it cannot decide eligibility or override a rule. The delivered offline prototype uses a transparent bounded extraction fallback so the demo works without a key.

## Synthetic demo scenarios

- KYC incomplete
- Bank verification issue
- Missing service information
- Conflicting information
- Ready to continue

## Run locally

Backend (Python 3.11 is the supported local version):

```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Frontend (Node 20+):

```powershell
cd frontend
npm install
npm run dev
```

Open the Vite address shown in the terminal. The UI uploads only synthetic PDF notices through a multipart API; files are held temporarily for extraction and then deleted. The UI retains a clearly disclosed local synthetic preview if the API is unavailable.

## Tests

```powershell
cd backend
pytest tests -q
```

## Safety and known limitations

Do not upload real Aadhaar, PAN, UAN, bank details, OTPs, passwords, or any real personal data. Only synthetic scenarios are supported. Text-based PDFs are extracted in temporary storage and deleted immediately; image OCR is deliberately not enabled yet. The local knowledge index is intentionally small and is not legal or official eligibility advice. See [safety.md](docs/safety.md) and [testing.md](docs/testing.md).

## Roadmap

Add authenticated, consent-based production integrations only with official authorization; replace local guidance metadata with a reviewed official-document ingestion pipeline; add server-side malware-safe file handling and vision extraction; and conduct security/accessibility review before any public use.
