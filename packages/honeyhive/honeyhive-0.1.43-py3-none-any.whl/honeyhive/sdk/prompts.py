from typing import Optional, Any, Dict, List
from honeyhive.api.models.prompts import (
    PromptCreationQuery,
    PromptQuery,
    PromptUpdateQuery,
    PromptResponse,
    ListPromptResponse,
)
from honeyhive.api.models.utils import DeleteResponse
from honeyhive.sdk.init import honeyhive_client


def get_prompts(
    project: Optional[str] = None, prompt_id: Optional[str] = None
) -> List[PromptResponse]:
    """Get all prompts"""
    client = honeyhive_client()
    return client.get_prompts(task=project, name=prompt_id)


def get_deployed_prompts(
    project: Optional[str] = None,
) -> List[PromptResponse]:
    """Get all deployed prompts"""
    client = honeyhive_client()
    prompts = client.get_prompts(task=project)
    return [prompt for prompt in prompts if prompt.is_deployed]


def create_prompt(
    project: str,
    prompt: str,
    version: Optional[int],
    input_variables: Optional[Dict[str, str]],
    model: str,
    provider: Optional[str],
    hyperparameters: Dict[str, Any],
    few_shot_examples: Optional[List[Dict[Any, Any]]],
) -> PromptResponse:
    """Create a prompt"""
    client = honeyhive_client()
    return client.create_prompt(
        prompt=PromptCreationQuery(
            task=project,
            prompt=prompt,
            version=version,
            input_variables=input_variables,
            model=model,
            provider=provider,
            hyperparameters=hyperparameters,
            few_shot_examples=few_shot_examples,
        )
    )


def update_prompt(
    id: str,
    version: int,
    input_variables: Dict[str, str],
    model: str,
    provider: Optional[str],
    hyperparameters: Dict[str, Any],
    is_deployed: bool,
    few_shot_examples: Optional[List[Dict[Any, Any]]],
) -> PromptResponse:
    """Update a prompt"""
    client = honeyhive_client()
    return client.update_prompt(
        prompt=PromptUpdateQuery(
            id=id,
            version=version,
            input_variables=input_variables,
            model=model,
            provider=provider,
            hyperparameters=hyperparameters,
            is_deployed=is_deployed,
            few_shot_examples=few_shot_examples,
        )
    )


def delete_prompt(id: str) -> DeleteResponse:
    """Delete a prompt"""
    client = honeyhive_client()
    return client.delete_prompt(id=id)


__all__ = ["get_prompts", "create_prompt", "update_prompt", "delete_prompt"]
