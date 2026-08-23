# NIVA product specification

NIVA is a synthetic-data prototype that helps people understand a PF claim issue and take the next concrete step. Its hero flow is: choose a claim problem, add a description or a synthetic notice, receive a deterministic workflow result, read a grounded explanation, and view the resulting journey.

The primary persona is Priya, a former employee whose withdrawal claim is blocked. The product is not an EPFO service and never requests real identity, bank, or OTP data. Withdrawal and transfer entry points deliberately remain marked as unavailable in this prototype.

## Scope

English, Hindi, and Kannada presentation; five synthetic scenarios; document-like text extraction; deterministic outcome; locally curated guidance with source references; a mobile-first accessible web flow; and an API-backed case record. The rules engine, rather than AI or the browser, is the decision authority.

## Implementation plan

1. Establish documented boundaries and a typed FastAPI foundation.
2. Add synthetic cases, a state machine, deterministic rules, retrieval, extraction fallback, and tests.
3. Build the single focused React journey and integrate it with the API, retaining a useful demo fallback when the API is not running.
4. Exercise unit and end-to-end flows, then refine loading, errors, accessibility, and mobile layout.
