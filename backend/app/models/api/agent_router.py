from pydantic import BaseModel, Field
from typing import List

class ProjectResponse(BaseModel):
    response: List[str] = Field(
        ..., description="Bullet-point response to the project validation"
    )
    is_greeting: bool = Field(
        ..., description="Whether the message is a greeting or unrelated to a project"
    )
    exists_in_data: bool = Field(
        ..., description="Does this project exist in the current dataset?"
    )
    exists_elsewhere: bool = Field(
        ..., description="Does this project seem to exist outside of the dataset (e.g., online)?"
    )
    relevant_projects: List[str] = Field(
        default_factory=list,
        description="IDs of relevant similar projects"
    )
