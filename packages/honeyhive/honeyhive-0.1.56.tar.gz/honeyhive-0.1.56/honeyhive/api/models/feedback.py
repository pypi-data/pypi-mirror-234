from typing import Dict, Optional, Any

from pydantic import BaseModel, Field


class FeedbackQuery(BaseModel):
    task: str = Field(
        title="Task",
        description="The task for which feedback is being submitted",
    )
    generation_id: str = Field(
        title="Generation ID",
        description="The unique ID of the generation for which feedback is being submitted",
    )
    feedback_json: Dict[str, Any] = Field(
        title="Feedback JSON",
        description="The feedback JSON with one or many feedback items",
    )
    ground_truth: Optional[str] = Field(
        title="Ground Truth", description="The ground truth for the generation"
    )


class FeedbackResponse(BaseModel):
    task: str = Field(
        title="Task",
        description="The task for which feedback is being submitted",
    )
    generation_id: str = Field(
        title="Generation ID",
        description="The unique ID of the generation for which feedback is being submitted",
    )
    feedback: Dict[str, Any] = Field(
        title="Feedback JSON",
        description="The feedback JSON with one or many feedback items",
    )
    ground_truth: Optional[str] = Field(
        title="Ground Truth", description="The ground truth for the generation"
    )
    created_at: str = Field(
        title="Created At",
        description="The timestamp at which the feedback was created",
    )
