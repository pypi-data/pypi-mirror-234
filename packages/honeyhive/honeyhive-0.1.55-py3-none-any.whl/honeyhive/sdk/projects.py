from typing import Optional, List
from honeyhive.api.models.tasks import (
    TaskCreationQuery,
    TaskUpdateQuery,
    TaskResponse,
    ListTaskResponse,
)
from honeyhive.api.models.fine_tuned_models import FineTunedModelResponse
from honeyhive.api.models.prompts import PromptResponse
from honeyhive.api.models.datasets import DatasetResponse
from honeyhive.api.models.metrics import MetricResponse
from honeyhive.api.models.utils import DeleteResponse
from honeyhive.sdk.init import honeyhive_client


def get_projects(
    name: Optional[str] = None,
) -> ListTaskResponse:
    """Get all tasks"""
    client = honeyhive_client()
    return client.get_tasks(name=name)


def get(name: str) -> TaskResponse:
    """Get a task"""
    client = honeyhive_client()
    return client.get_tasks(name=name)


def create(
    name: str,
    type: str,
    fine_tuned_models: Optional[List[FineTunedModelResponse]] = [],
    prompts: Optional[List[PromptResponse]] = [],
    datasets: Optional[List[DatasetResponse]] = [],
    metrics: Optional[List[MetricResponse]] = []
) -> TaskResponse:
    """Create a task"""
    client = honeyhive_client()
    return client.create_task(
        task=TaskCreationQuery(
            name=name,
            type=type,
            fine_tuned_models=fine_tuned_models,
            prompts=prompts,
            datasets=datasets,
            metrics=metrics,
        )
    )


def update(
    task_id: str,
    name: Optional[str] = None,
    type: Optional[str] = None,
    fine_tuned_models: Optional[List[FineTunedModelResponse]] = [],
    prompts: Optional[List[PromptResponse]] = [],
    datasets: Optional[List[DatasetResponse]] = [],
    metrics: Optional[List[MetricResponse]] = [],
) -> TaskResponse:
    """Update a task"""
    client = honeyhive_client()
    return client.update_task(
        task_id=task_id,
        task=TaskUpdateQuery(
            name=name,
            type=type,
            fine_tuned_models=fine_tuned_models,
            prompts=prompts,
            datasets=datasets,
            metrics=metrics,
        ),
    )


def delete(name: str) -> DeleteResponse:
    """Delete a task"""
    client = honeyhive_client()
    return client.delete_task(name=name)


__all__ = [
    "get_projects",
    "get",
    "create",
    "update",
    "delete",
]
