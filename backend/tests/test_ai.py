from app.ai import OpenAIAdapter
from app.domain import Language
from app.rules import evaluate
from app.scenarios import SCENARIOS
from app.services import COPY, local_explanation
def test_demo_adapter_extracts_without_api_key():
    item=OpenAIAdapter(api_key="").extract("Synthetic notice: KYC rejected")
    assert item.mode=="demo_mock" and item.scenario_hint=="kyc"

def test_every_reason_code_has_a_nonempty_explanation_in_all_languages():
    scenarios = {evaluate(case).reason_code.value: case for case in SCENARIOS.values()}
    for language in Language:
        for reason_code, case in scenarios.items():
            explanation = local_explanation(evaluate(case), [], language)
            assert reason_code in COPY
            assert explanation.what_happened and explanation.what_to_do and explanation.why
