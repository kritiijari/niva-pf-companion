# Testing strategy

Rules tests cover ready, KYC, bank, missing-service, conflict, invalid-type, and resolved cases. API tests cover case creation, analysis, retrieval, timeline, explanation, bad upload, and source retrieval. The end-to-end scenario creates Priya's case, applies a synthetic notice, evaluates rules, retrieves guidance, and verifies a derived action/timeline.

QA cases include empty/oversize descriptions, unsupported and corrupt files, repeated analysis, unavailable retrieval, malformed extraction, locale switching, and unavailable backend. The frontend handles failure with user-facing retry guidance rather than technical error text.
