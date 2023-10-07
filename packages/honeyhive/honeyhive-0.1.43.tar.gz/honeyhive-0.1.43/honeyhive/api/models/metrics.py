from typing import Optional, List
from pydantic import BaseModel, Field
import datetime


class MetricResponse(BaseModel):
    id: str = Field(
        title="Metric ID", description="The unique ID of the metric"
    )
    object: str = Field(
        title="Object", description="The object type of the metric"
    )
    name: str = Field(title="Name", description="The name of the metric")
    code_snippet: str = Field(
        title="Code Snippet", description="The code snippet for the metric"
    )
    task_name: Optional[str] = Field(
        title="Task Name", description="The task name for the metric"
    )
    created_at: datetime.datetime
    updated_at: datetime.datetime


class ListMetricResponse(BaseModel):
    data: List[MetricResponse] = Field(
        title="Data", description="The list of metrics"
    )


class MetricRequest(BaseModel):
    name: str = Field(title="Name", description="The name of the metric")
    task: str = Field(
        title="Task Name", description="The task name for the metric"
    )
    code_snippet: str = Field(
        title="Code Snippet", description="The code snippet for the metric"
    )
