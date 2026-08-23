# Architecture

```text
Mobile web app
      | REST / JSON
FastAPI case manager ---- SQLite-ready in-memory prototype store
      |                         |
      |                    audit-safe logs
      v
Deterministic rules engine <--- structured extraction
      |                                |
      +-------- retrieval -----------+
                         |
                  grounded explanation
                         |
                      citizen
```

The frontend owns only interaction state. FastAPI creates and reads cases, selects synthetic scenarios, extracts a limited document schema, runs rules, and returns the derived timeline. The rules engine evaluates ordered checks (claim type, service information, KYC, bank verification, consistency) and supplies the authoritative state, reason, and next action. AI is optional and constrained to structured extraction/explanation; no model result can change a workflow decision. The local knowledge service returns only supplied source metadata and declines unsupported claims.
