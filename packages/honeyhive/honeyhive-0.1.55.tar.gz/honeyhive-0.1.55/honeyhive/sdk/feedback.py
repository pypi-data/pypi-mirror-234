from typing import Any, Dict, List, Optional
from honeyhive.api.models.feedback import FeedbackQuery, FeedbackResponse
from honeyhive.sdk.init import honeyhive_client


def generation_feedback(
    project: str,
    generation_id: str,
    feedback_json: Dict[str, Any],
    ground_truth: Optional[str] = None,
) -> FeedbackResponse:
    """Submit feedback"""
    client = honeyhive_client()
    return client.feedback(
        feedback=FeedbackQuery(
            task=project,
            generation_id=generation_id,
            feedback_json=feedback_json,
            ground_truth=ground_truth,
        )
    )


__all__ = ["generation_feedback"]
