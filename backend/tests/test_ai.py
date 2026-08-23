from app.ai import OpenAIAdapter
def test_demo_adapter_extracts_without_api_key():
    item=OpenAIAdapter(api_key="").extract("Synthetic notice: KYC rejected")
    assert item.mode=="demo_mock" and item.scenario_hint=="kyc"
