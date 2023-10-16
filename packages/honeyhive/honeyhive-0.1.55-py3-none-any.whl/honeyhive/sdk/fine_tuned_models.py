from typing import Optional
from honeyhive.api.models.fine_tuned_models import (
    FineTunedModelResponse,
    ListFineTunedModelResponse,
)
from honeyhive.sdk.init import honeyhive_client


def get_fine_tuned_models(
    project: Optional[str] = None, model_id: Optional[str] = None
) -> ListFineTunedModelResponse:
    """Get all fine tuned models"""
    client = honeyhive_client()
    return client.get_fine_tuned_models(task=project, model_id=model_id)


def get_fine_tuned_model(model_id: str) -> FineTunedModelResponse:
    """Get a fine tuned model"""
    client = honeyhive_client()
    return client.get_fine_tuned_model(model_id=model_id)


__all__ = ["get_fine_tuned_models", "get_fine_tuned_model"]
