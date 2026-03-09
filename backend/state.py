from typing import Annotated, TypedDict, List
import operator
from pydantic import BaseModel, Field

class Researchers(BaseModel):
    name: str = Field(description='The name of the researcher')
    role: str = Field(description='The role of the researcher in the context of the topic')
    research_interests: str = Field(description='The research interests of the researcher')
    CV: str = Field(description='A short cv information about the researcher, one line max.')

    @property
    def description(self) -> str:
        return f"Name: {self.name}\nRole: {self.role}\nResearch Interests: {self.research_interests}\nCV Information: {self.CV}"

class Res_List(BaseModel):
    re_list: List[Researchers] = Field(description='The list of researchers')

class Re_State(TypedDict):
    re_list: List[Researchers]
    topic: str
    max_researchers: int= 3

class QuestionState(TypedDict):
    context: Annotated[list, operator.add]
    questions_answer: Annotated[list, operator.add]
    researcher: Researchers
    report: str  
    topic_description: str

class SearchQuery(BaseModel):
    search: str = Field(description='The search query')