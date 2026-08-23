from .domain import WorkflowState
ORDER=[WorkflowState.CLAIM_PREPARATION,WorkflowState.ELIGIBILITY_CHECK,WorkflowState.KYC_VERIFICATION,WorkflowState.BANK_VERIFICATION,WorkflowState.CLAIM_SUBMISSION,WorkflowState.PROCESSING,WorkflowState.PAYMENT,WorkflowState.RESOLVED]
def can_transition(current:WorkflowState,target:WorkflowState)->bool: return target==current or (current in ORDER and target in ORDER and ORDER.index(target)<=ORDER.index(current)+1)
