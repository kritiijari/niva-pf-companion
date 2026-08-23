from enum import Enum
from pydantic import BaseModel, Field
class Language(str, Enum): EN="en"; HI="hi"; KN="kn"
class ClaimType(str, Enum): WITHDRAWAL="withdrawal"
class ClaimStatus(str, Enum): DRAFT="draft"; REJECTED="rejected"; READY="ready"; RESOLVED="resolved"
class Verification(str, Enum): COMPLETE="complete"; INCOMPLETE="incomplete"; FAILED="failed"
class ServiceRecord(str, Enum): COMPLETE="complete"; MISSING="missing"
class Consistency(str, Enum): CONSISTENT="consistent"; CONFLICT="conflict"
class WorkflowState(str, Enum):
    CLAIM_PREPARATION="claim_preparation"; ELIGIBILITY_CHECK="eligibility_check"; KYC_VERIFICATION="kyc_verification"; BANK_VERIFICATION="bank_verification"; CLAIM_SUBMISSION="claim_submission"; PROCESSING="processing"; PAYMENT="payment"; RESOLVED="resolved"
class ReasonCode(str, Enum):
    KYC_INCOMPLETE="KYC_INCOMPLETE"; BANK_VERIFICATION_FAILED="BANK_VERIFICATION_FAILED"; SERVICE_INFORMATION_MISSING="SERVICE_INFORMATION_MISSING"; INFORMATION_CONFLICT="INFORMATION_CONFLICT"; READY_TO_CONTINUE="READY_TO_CONTINUE"; INVALID_CLAIM_TYPE="INVALID_CLAIM_TYPE"; CLAIM_RESOLVED="CLAIM_RESOLVED"
class CaseData(BaseModel):
    scenario: str="kyc"; citizen_name: str="Priya (synthetic)"; claim_type: str=ClaimType.WITHDRAWAL.value; claim_status: ClaimStatus=ClaimStatus.REJECTED; kyc: Verification=Verification.INCOMPLETE; bank: Verification=Verification.COMPLETE; service: ServiceRecord=ServiceRecord.COMPLETE; consistency: Consistency=Consistency.CONSISTENT; rejection_reason: str="KYC verification needs attention"
class RuleResult(BaseModel):
    status: str; reason_code: ReasonCode; current_step: WorkflowState; next_action: str; severity: str; required_information: list[str]=Field(default_factory=list); explanation_context: dict[str,str]=Field(default_factory=dict); confidence: str="deterministic"
class ExtractionResult(BaseModel):
    claim_type: str|None=None; claim_status: str|None=None; rejection_reason: str|None=None; mentioned_documents: list[str]=Field(default_factory=list); mentioned_issue: str|None=None; dates: list[str]=Field(default_factory=list); important_fields: dict[str,str]=Field(default_factory=dict); scenario_hint: str|None=None; mode: str="demo_mock"
class SourceReference(BaseModel): document_id: str; title: str; url: str; section: str; excerpt: str
class Explanation(BaseModel):
    what_happened: str; what_to_do: list[str]; why: str; source_references: list[SourceReference]=Field(default_factory=list); language: Language; mode: str
