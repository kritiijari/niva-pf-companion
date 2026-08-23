from pydantic import BaseModel, Field
from .domain import Language, RuleResult, ExtractionResult, Explanation
class CreateCaseRequest(BaseModel): scenario: str="kyc"; language: Language=Language.EN
class CaseCreated(BaseModel): case_id: str; request_id: str
class AnalyzeRequest(BaseModel): description: str=Field(default="", max_length=3000)
class TimelineItem(BaseModel): key: str; label: str; state: str
class AnalysisResponse(BaseModel): case_id: str; extraction: ExtractionResult; result: RuleResult; explanation: Explanation; timeline: list[TimelineItem]; request_id: str
class CaseResponse(BaseModel): case_id: str; scenario: str; language: Language; result: RuleResult; explanation: Explanation; request_id: str
class TimelineResponse(BaseModel): case_id: str; timeline: list[TimelineItem]; request_id: str
class QuestionRequest(BaseModel): question: str=Field(min_length=1,max_length=500)
class QuestionResponse(BaseModel): answer: str; sources: list[dict]; request_id: str
