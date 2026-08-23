import os
from .domain import ExtractionResult, Explanation, Language, RuleResult, CaseData, SourceReference
from .services import local_extraction, local_explanation
class AIProblem(Exception): pass
SYSTEM="You extract facts from SYNTHETIC PF notices. Missing facts are null. Never decide eligibility, invent requirements, sources, identifiers, or rules. Return only the provided JSON schema."
class OpenAIAdapter:
    def __init__(self,api_key:str|None=None): self.api_key=api_key or os.getenv("OPENAI_API_KEY")
    @property
    def mode(self): return "openai" if self.api_key else "demo_mock"
    def extract(self,text:str)->ExtractionResult:
        if not self.api_key: return local_extraction(text)
        try:
            from openai import OpenAI
            client=OpenAI(api_key=self.api_key,timeout=12.0,max_retries=1)
            response=client.responses.create(model=os.getenv("OPENAI_MODEL","gpt-4.1-mini"),instructions=SYSTEM,input=text,text={"format":{"type":"json_schema","name":"claim_extraction","schema":ExtractionResult.model_json_schema(),"strict":True}})
            return ExtractionResult.model_validate_json(response.output_text).model_copy(update={"mode":"openai"})
        except Exception as exc: raise AIProblem("We couldn't extract information from this notice right now. You can describe the issue instead.") from exc
    def explain(self,result:RuleResult,case:CaseData,sources:list[SourceReference],language:Language)->Explanation: return local_explanation(result,sources,language,self.mode)
