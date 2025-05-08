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
    response: str = Field(..., description="The generated response to the user's query")
    confidence_score: float = Field(
        default=0.7,
        ge=0.0,
        le=1.0,
        description="Confidence score of the response (0.0 to 1.0)"
    )
    suggested_actions: List[str] = Field(
        default_factory=list,
        description="Optional list of suggested actions"
    )
    relevant_projects: List[str] = Field(
        default_factory=list,
        description="Optional list of relevant project IDs"
    )
    sources: List[ProjectSource] = Field(
        default_factory=list,
        description="List of sources for the project information"
    )