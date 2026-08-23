from .domain import CaseData, ClaimStatus, Verification, ServiceRecord, Consistency

SCENARIOS = {
 "kyc": CaseData(scenario="kyc", rejection_reason="KYC verification needs attention"),
 "bank": CaseData(scenario="bank", kyc=Verification.COMPLETE, bank=Verification.FAILED, rejection_reason="Bank account verification could not be completed"),
 "service": CaseData(scenario="service", kyc=Verification.COMPLETE, service=ServiceRecord.MISSING, rejection_reason="Service information is incomplete"),
 "conflict": CaseData(scenario="conflict", kyc=Verification.COMPLETE, consistency=Consistency.CONFLICT, rejection_reason="Information in the claim does not match the service record"),
 "ready": CaseData(scenario="ready", claim_status=ClaimStatus.READY, kyc=Verification.COMPLETE, rejection_reason="No blocking issue found"),
 "resolved": CaseData(scenario="resolved", claim_status=ClaimStatus.RESOLVED, kyc=Verification.COMPLETE, rejection_reason="Claim workflow has been resolved"),
}
