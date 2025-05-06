from pydantic import BaseModel, Field
from typing import List

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