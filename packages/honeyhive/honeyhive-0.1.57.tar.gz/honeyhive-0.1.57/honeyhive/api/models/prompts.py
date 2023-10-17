from typing import Optional, Dict, List, Any
from pydantic import BaseModel, Field
import datetime


class PromptResponse(BaseModel):
    name: str = Field(
        title="Prompt name", description="The unique name of the prompt"
    )
    version: Optional[str] = Field(
        title="Version", description="The version of the prompt"
    )
    task: str = Field(
        title="Task",
        description="The task for which the prompt is being created",
    )
    text: str = Field(title="Text", description="The text of the prompt")
    input_variables: Optional[List[str]] = Field(
        title="Input Variables",
        description="The input variables to feed into the prompt",
    )
    model: str = Field(
        title="Model", description="The model to be used for the prompt"
    )
    hyperparameters: Dict[str, Any] = Field(
        title="Hyperparameters",
        description="The hyperparameters for the prompt",
    )
    is_deployed: Optional[bool] = Field(
        title="Is Deployed",
        description="The flag to indicate if the prompt is deployed",
    )
    few_shot_examples: Optional[List[Dict[Any, Any]]] = Field(
        title="Few Shot Examples",
        description="The few shot examples for the prompt, specified as a list of dictionaries"
        + " where each dictionary has a key-value pair of input variables and the corresponding"
        + " completion",
    )
    created_at: datetime.datetime
    updated_at: datetime.datetime


class PromptQuery(BaseModel):
    task: Optional[str] = Field(
        title="Task",
        description="The task for which the prompt is being created",
    )
    id: Optional[str] = Field(
        title="Prompt ID", description="The unique ID of the prompt"
    )


class ListPromptResponse(BaseModel):
    data: List[PromptResponse] = Field(
        title="Data", description="The list of prompts"
    )


class PromptCreationQuery(BaseModel):
    task: str = Field(
        title="Task",
        description="The task for which the prompt is being created",
    )
    text: str = Field(
        title="Text", description="The text of the prompt to be created"
    )
    version: Optional[int] = Field(
        title="Version", description="The version of the prompt"
    )
    input_variables: Optional[List[str]] = Field(
        title="Input Variables",
        description="The input variables to feed into the prompt",
    )
    model: str = Field(
        title="Model", description="The model to be used for the prompt"
    )
    provider: str = Field(
        title="Provider",
        description="The provider of the model to be used for the prompt",
    )
    hyperparameters: Dict[str, Any] = Field(
        title="Hyperparameters",
        description="The hyperparameters for the prompt",
    )
    few_shot_examples: Optional[List[Dict[Any, Any]]] = Field(
        title="Few Shot Examples",
        description="The few shot examples for the prompt, specified as a list of dictionaries"
        + " where each dictionary has a key-value pair of input variables and the corresponding"
        + " completion",
    )


class PromptUpdateQuery(BaseModel):
    id: str = Field(
        title="Prompt ID", description="The unique ID of the prompt"
    )
    version: int = Field(
        title="Version", description="The version of the prompt"
    )
    input_variables: List[str] = Field(
        title="Input Variables",
        description="The input variables to feed into the prompt",
    )
    model: str = Field(
        title="Model", description="The model to be used for the prompt"
    )
    provider: str = Field(
        title="Provider",
        description="The provider of the model to be used for the prompt",
    )
    hyperparameters: Dict[str, Any] = Field(
        title="Hyperparameters",
        description="The hyperparameters for the prompt",
    )
    is_deployed: bool = Field(
        title="Is Deployed",
        description="The flag to indicate if the prompt is deployed",
    )
    few_shot_examples: Optional[List[Dict[Any, Any]]] = Field(
        title="Few Shot Examples",
        description="The few shot examples for the prompt, specified as a list of dictionaries"
        + " where each dictionary has a key-value pair of input variables and the corresponding"
        + " completion",
    )
