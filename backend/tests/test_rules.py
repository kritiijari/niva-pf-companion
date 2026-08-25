import pytest
from app.scenarios import SCENARIOS
from app.rules import evaluate
from app.domain import ReasonCode
@pytest.mark.parametrize("scenario,reason", [("kyc",ReasonCode.KYC_INCOMPLETE),("bank",ReasonCode.BANK_VERIFICATION_FAILED),("service",ReasonCode.SERVICE_INFORMATION_MISSING),("conflict",ReasonCode.INFORMATION_CONFLICT),("ready",ReasonCode.READY_TO_CONTINUE),("resolved",ReasonCode.CLAIM_RESOLVED),("transfer_service",ReasonCode.TRANSFER_SERVICE_MISSING),("transfer_conflict",ReasonCode.TRANSFER_INFORMATION_CONFLICT),("transfer_ready",ReasonCode.TRANSFER_READY)])
def test_rules(scenario, reason): assert evaluate(SCENARIOS[scenario]).reason_code == reason
def test_invalid_claim_type():
    case=SCENARIOS["ready"].model_copy(update={"claim_type":"unsupported"})
    assert evaluate(case).reason_code == ReasonCode.INVALID_CLAIM_TYPE
