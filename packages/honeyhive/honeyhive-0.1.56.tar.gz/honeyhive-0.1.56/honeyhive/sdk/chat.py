from typing import Dict, List, Optional, Any
from honeyhive.api.models.chat import (
    ChatQuery,
    ChatResponse
)
from honeyhive.sdk.init import honeyhive_client

def create(
    project: str,
    model: str = "gpt-3.5-turbo",
    messages: List[Dict[str, Any]] = [],
    provider: Optional[str] = "openai",
    version: Optional[str] = "unknown",
    inputs: Optional[Dict[str, Any]] = {},
    functions: Optional[List[Dict[str, Any]]] = None,
    function_call: Optional[str] = None,
    plugins: Optional[List[str]] = None,
    source: Optional[str] = "unknown",
    num_samples: Optional[int] = 1,
    stream: Optional[bool] = False,
    user: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = {},
    ground_truth: Optional[str] = "",
    **kwargs
):
    # parse the kwargs into hyperparameters
    hyperparameters = kwargs
    client = honeyhive_client()

    if stream == False:
        return client.chat(
            chat=ChatQuery(
                project=project,
                model=model,
                messages=messages,
                provider=provider,
                version=version,
                inputs=inputs,
                functions=functions,
                function_call=function_call,
                plugins=plugins,
                source=source,
                num_samples=num_samples,
                stream=stream,
                user=user,
                metadata=metadata,
                ground_truth=ground_truth,
                hyperparameters=hyperparameters,
            )
        )
    else:
        return client.chat_stream(
            chat=ChatQuery(
                project=project,
                model=model,
                messages=messages,
                provider=provider,
                version=version,
                inputs=inputs,
                functions=functions,
                function_call=function_call,
                plugins=plugins,
                source=source,
                num_samples=num_samples,
                stream=stream,
                user=user,
                metadata=metadata,
                ground_truth=ground_truth,
                hyperparameters=hyperparameters,
            )
        )

__all__ = ["create"]
