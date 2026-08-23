# AI behavior and retrieval

Document extraction uses a strict Pydantic schema. In this offline prototype, a bounded keyword extractor handles the supplied synthetic documents; an OpenAI adapter can be enabled server-side with `OPENAI_API_KEY`. Extraction failure returns a recoverable error and does not infer missing fields.

Retrieval searches a small, curated local EPFO guidance catalogue. Explanations are composed from deterministic results plus retrieved metadata. When no source matches, the response explicitly says the local knowledge base lacks sufficient guidance. The model must never decide eligibility, invent a citation, or describe an external EPFO integration.
