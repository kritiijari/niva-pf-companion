from .domain import (
    CaseData,
    ClaimStatus,
    Verification,
    ServiceRecord,
    Consistency,
    ClaimType,
)

SCENARIOS = {
    # -----------------------------
    # PF WITHDRAWAL SCENARIOS
    # -----------------------------

    "kyc": CaseData(
        scenario="kyc",
        claim_type=ClaimType.WITHDRAWAL.value,
        rejection_reason="KYC verification needs attention",
    ),

    "bank": CaseData(
        scenario="bank",
        claim_type=ClaimType.WITHDRAWAL.value,
        kyc=Verification.COMPLETE,
        bank=Verification.FAILED,
        rejection_reason="Bank account verification could not be completed",
    ),

    "service": CaseData(
        scenario="service",
        claim_type=ClaimType.WITHDRAWAL.value,
        kyc=Verification.COMPLETE,
        service=ServiceRecord.MISSING,
        rejection_reason="Service information is incomplete",
    ),

    "conflict": CaseData(
        scenario="conflict",
        claim_type=ClaimType.WITHDRAWAL.value,
        kyc=Verification.COMPLETE,
        consistency=Consistency.CONFLICT,
        rejection_reason="Information in the claim does not match the service record",
    ),

    "ready": CaseData(
        scenario="ready",
        claim_type=ClaimType.WITHDRAWAL.value,
        claim_status=ClaimStatus.READY,
        kyc=Verification.COMPLETE,
        rejection_reason="No blocking issue found",
    ),

    "resolved": CaseData(
        scenario="resolved",
        claim_type=ClaimType.WITHDRAWAL.value,
        claim_status=ClaimStatus.RESOLVED,
        kyc=Verification.COMPLETE,
        rejection_reason="Claim workflow has been resolved",
    ),

    # -----------------------------
    # PF TRANSFER SCENARIOS
    # -----------------------------

    "transfer_service": CaseData(
        scenario="transfer_service",
        claim_type=ClaimType.TRANSFER.value,
        kyc=Verification.COMPLETE,
        service=ServiceRecord.MISSING,
        rejection_reason="Previous employment service information is incomplete",
    ),

    "transfer_conflict": CaseData(
        scenario="transfer_conflict",
        claim_type=ClaimType.TRANSFER.value,
        kyc=Verification.COMPLETE,
        service=ServiceRecord.COMPLETE,
        consistency=Consistency.CONFLICT,
        rejection_reason="Previous and current employment information does not match",
    ),

    "transfer_ready": CaseData(
        scenario="transfer_ready",
        claim_type=ClaimType.TRANSFER.value,
        claim_status=ClaimStatus.READY,
        kyc=Verification.COMPLETE,
        service=ServiceRecord.COMPLETE,
        consistency=Consistency.CONSISTENT,
        rejection_reason="Transfer request is ready to continue",
    ),
}