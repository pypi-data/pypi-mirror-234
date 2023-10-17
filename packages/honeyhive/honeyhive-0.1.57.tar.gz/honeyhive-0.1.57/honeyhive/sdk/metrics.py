from typing import Optional, List
from honeyhive.api.models.metrics import (
    MetricResponse,
    ListMetricResponse,
    MetricRequest,
)
from honeyhive.api.models.utils import DeleteResponse
from honeyhive.sdk.init import honeyhive_client


def get_metrics(
    project: str, metric_id: Optional[str]
) -> List[MetricResponse]:
    """Get all metrics"""
    client = honeyhive_client()
    return client.get_metrics(task=project, metric_id=metric_id)


def get_metric(metric_id: str) -> MetricResponse:
    """Get a metric"""
    client = honeyhive_client()
    return client.get_metric(metric_id=metric_id)


def create_metric(
    name: str, project: str, code_snippet: str
) -> MetricResponse:
    """Create a metric"""

    # TODO add validation for code_snippet

    client = honeyhive_client()
    return client.create_metric(
        metric=MetricRequest(
            name=name, task=project, code_snippet=code_snippet
        )
    )


def delete_metric(metric_id: str) -> DeleteResponse:
    """Delete a metric"""
    client = honeyhive_client()
    return client.delete_metric(metric_id=metric_id)


__all__ = ["get_metrics", "get_metric", "create_metric", "delete_metric"]
