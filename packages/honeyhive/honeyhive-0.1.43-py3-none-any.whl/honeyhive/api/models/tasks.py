from .fine_tuned_models import FineTunedModelResponse
from .prompts import PromptResponse
from .datasets import DatasetResponse
from .metrics import MetricResponse

from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field
import datetime


class TaskResponse(BaseModel):
    id: str = Field(title="Task ID", description="The unique ID of the task")
    name: str = Field(title="Task Name", description="The name of the task")
    type: Optional[str] = Field(
        title="Task Type", description="The type of the task"
    )
    fine_tuned_models: Optional[List[FineTunedModelResponse]]
    prompts: List[PromptResponse]
    datasets: Optional[List[DatasetResponse]]
    metrics: Optional[List[MetricResponse]]
    created_at: datetime.datetime
    updated_at: datetime.datetime


class TaskCreationQuery(BaseModel):
    name: str = Field(title="Task Name", description="The name of the task")
    type: Optional[str] = Field(
        title="Task Type", description="The type of the task"
    )
    fine_tuned_models: Optional[List[FineTunedModelResponse]] = Field(
        title="Fine Tuned Models",
        description="The fine tuned models for the task",
    )
    prompts: Optional[List[PromptResponse]] = Field(
        title="Prompts", description="The prompts for the task"
    )
    datasets: Optional[List[DatasetResponse]] = Field(
        title="Datasets", description="The datasets for the task"
    )
    metrics: Optional[List[MetricResponse]] = Field(
        title="Metrics", description="The metrics for the task"
    )


class TaskUpdateQuery(BaseModel):
    name: Optional[str] = Field(
        title="Task Name", description="The name of the task"
    )
    type: Optional[str] = Field(
        title="Task Type", description="The type of the task"
    )
    fine_tuned_models: Optional[List[FineTunedModelResponse]] = Field(
        title="Fine Tuned Models",
        description="The fine tuned models for the task",
    )
    prompts: Optional[List[PromptResponse]] = Field(
        title="Prompts", description="The prompts for the task"
    )
    datasets: Optional[List[DatasetResponse]] = Field(
        title="Datasets", description="The datasets for the task"
    )
    metrics: Optional[List[MetricResponse]] = Field(
        title="Metrics", description="The metrics for the task"
    )


class ListTaskResponse(BaseModel):
    data: List[TaskResponse] = Field(
        title="List of tasks", description="The list of tasks"
    )
