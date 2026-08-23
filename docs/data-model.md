# Data model

`Case` contains a random case ID, locale, synthetic citizen marker, claim type/status, KYC state, bank state, service record state, consistency state, and rejection reason. It may retain a safe file name but never raw document contents.

`RuleResult` contains `status`, `reason_code`, `current_step`, `next_action`, `severity`, `required_information`, `explanation_context`, and `confidence="deterministic"`.

`TimelineStep` is derived from `current_step`; it is never separately authored by the client. `Guidance` preserves title, URL, section, and excerpt. Events include request ID, event name, case ID, and non-sensitive outcome only.
