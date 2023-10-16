from typing import Dict, List, Optional, Any

from pydantic import BaseModel, Field


class EvaluationLoggingQuery(BaseModel):
    name: str = Field(
        title="Evaluation Name", description="The name of the evaluation"
    )
    task: str = Field(
        title="Project",
        description="The project for which the evaluation is being created",
    )
    prompts: List[Dict[str, Any]] = Field(
        title="Prompts",
        description="The prompts for which the evaluation is being created",
    )
    dataset: List[Dict[str, Any]] = Field(
        title="Dataset",
        description="The dataset for which the evaluation is being created",
    )
    datasetName: str = Field(
        title="Dataset Name",
        description="The name of the dataset for which the evaluation is being created",
    )
    summary: Optional[List[Dict[str, Any]]] = Field(
        title="Summary", description="The metric summary of the evaluation"
    )
    results: List[Dict[str, Any]] = Field(
        title="Results", description="The results of the evaluation"
    )
    accepted: List[List[Any]] = Field(
        title="Accepted",
        description="The accepted completions for the prompts that are being evaluated",
    )
    metrics: List[List[Dict[str, Any]]] = Field(
        title="Metrics",
        description="The metrics that are computed for the completions",
    )
    metrics_to_compute: List[str] = Field(
        title="Metrics to Compute",
        description="The metrics that are computed for the completions",
    )
    comments: List[Dict[str, Any]] = Field(
        title="Comments", description="The comments for the evaluation"
    )
    generations: Optional[List[Any]] = Field(
        title="Generations",
        description="The completions for prompts that are being evaluated",
    )
    description: Optional[str] = Field(
        title="Evaluation Description",
        description="The description of the evaluation",
    )


class SuccessResponse(BaseModel):
    success: bool = Field(
        title="Success", description="Whether the request was successful"
    )
    id: Optional[str] = Field(
        title="ID", description="The ID of the object that was created"
    )
