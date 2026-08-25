from .domain import *


def evaluate(case: CaseData) -> RuleResult:

    # -----------------------------
    # RESOLVED
    # -----------------------------

    if case.claim_status == ClaimStatus.RESOLVED:
        return RuleResult(
            status="resolved",
            reason_code=ReasonCode.CLAIM_RESOLVED,
            current_step=WorkflowState.RESOLVED,
            next_action="view_resolution",
            severity="success",
        )

    # -----------------------------
    # PF TRANSFER JOURNEY
    # -----------------------------

    if case.claim_type == ClaimType.TRANSFER.value:

        if case.service == ServiceRecord.MISSING:
            return RuleResult(
                status="blocked",
                reason_code=ReasonCode.TRANSFER_SERVICE_MISSING,
                current_step=WorkflowState.ELIGIBILITY_CHECK,
                next_action="complete_previous_employment_information",
                severity="warning",
                required_information=[
                    "Complete previous employment service information"
                ],
            )

        if case.consistency != Consistency.CONSISTENT:
            return RuleResult(
                status="blocked",
                reason_code=ReasonCode.TRANSFER_INFORMATION_CONFLICT,
                current_step=WorkflowState.ELIGIBILITY_CHECK,
                next_action="resolve_transfer_information_conflict",
                severity="warning",
                required_information=[
                    "Resolve the conflict between previous and current employment records"
                ],
            )

        return RuleResult(
            status="ready",
            reason_code=ReasonCode.TRANSFER_READY,
            current_step=WorkflowState.CLAIM_SUBMISSION,
            next_action="continue_transfer",
            severity="success",
        )

    # -----------------------------
    # PF WITHDRAWAL JOURNEY
    # -----------------------------

    if case.claim_type == ClaimType.WITHDRAWAL.value:

        if case.service == ServiceRecord.MISSING:
            return RuleResult(
                status="blocked",
                reason_code=ReasonCode.SERVICE_INFORMATION_MISSING,
                current_step=WorkflowState.ELIGIBILITY_CHECK,
                next_action="complete_service_information",
                severity="warning",
                required_information=["Complete service information"],
            )

        if case.kyc != Verification.COMPLETE:
            return RuleResult(
                status="blocked",
                reason_code=ReasonCode.KYC_INCOMPLETE,
                current_step=WorkflowState.KYC_VERIFICATION,
                next_action="complete_kyc",
                severity="warning",
                required_information=["Complete KYC verification"],
            )

        if case.bank != Verification.COMPLETE:
            return RuleResult(
                status="blocked",
                reason_code=ReasonCode.BANK_VERIFICATION_FAILED,
                current_step=WorkflowState.BANK_VERIFICATION,
                next_action="review_bank_verification",
                severity="warning",
                required_information=["Review bank verification"],
            )

        if case.consistency != Consistency.CONSISTENT:
            return RuleResult(
                status="blocked",
                reason_code=ReasonCode.INFORMATION_CONFLICT,
                current_step=WorkflowState.ELIGIBILITY_CHECK,
                next_action="resolve_information_conflict",
                severity="warning",
                required_information=["Resolve conflicting information"],
            )

        return RuleResult(
            status="ready",
            reason_code=ReasonCode.READY_TO_CONTINUE,
            current_step=WorkflowState.CLAIM_SUBMISSION,
            next_action="continue_claim",
            severity="success",
        )

    # -----------------------------
    # INVALID CLAIM TYPE
    # -----------------------------

    return RuleResult(
        status="needs_review",
        reason_code=ReasonCode.INVALID_CLAIM_TYPE,
        current_step=WorkflowState.CLAIM_PREPARATION,
        next_action="confirm_claim_type",
        severity="warning",
    )