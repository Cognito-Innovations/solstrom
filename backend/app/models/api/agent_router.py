from pydantic import BaseModel, Field
from typing import List, Optional

class ProjectSource(BaseModel):
    source_name: Optional[str] = Field(
        None,
        description="Name of the source where the project information came from"
    )
    source_url: Optional[str] = Field(
        None,
        description="URL of the source where the project information came from"
    )

class ProjectResponse(BaseModel):
    response: List[str] = Field(
        ..., description="Bullet-point response to the project validation"
    )
    is_greeting: bool = Field(
        default=False, 
        description="Whether the message is a greeting or unrelated to a project"
    )
    exists_in_data: bool = Field(
        default=False,
        description="Does this project exist in the current dataset?"
    )
    exists_elsewhere: bool = Field(
        default=False, 
        description="Does this project seem to exist outside of the dataset (e.g., online)?"
    )
    relevant_projects: List[str] = Field(
        default_factory=list,
        description="IDs of relevant similar projects"
    )
    sources: List[ProjectSource] = Field(
        default_factory=list,
        description="List of sources for the project information"
    )