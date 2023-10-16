from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
import datetime


class DatasetResponse(BaseModel):
    name: str = Field(
        title="Dataset Name", description="The name of the dataset file"
    )
    bytes: int = Field(
        title="Bytes", description="The size of the dataset in bytes"
    )
    created_at: datetime.datetime = Field(
        title="Created At",
        description="The date and time when the dataset was created",
    )
    task: str = Field(
        title="Task", description="The task related to the dataset"
    )
    prompt: Optional[str] = Field(
        title="Prompt", description="The prompt related to the dataset"
    )
    purpose: str = Field(
        title="Purpose", description="The purpose of the dataset"
    )
    description: Optional[str] = Field(
        title="Description", description="The description of the dataset"
    )


class ListDatasetResponse(BaseModel):
    data: List[DatasetResponse] = Field(
        title="Data", description="The list of datasets"
    )


class FetchDataset(BaseModel):
    name: Optional[str] = Field(
        title="Dataset ID", description="The unique ID of the dataset"
    )
    task: Optional[str] = Field(
        title="Task", description="The dataset related to a task"
    )
    prompt: Optional[str] = Field(
        title="Prompt", description="The dataset related to a prompt"
    )
    purpose: Optional[str] = Field(
        title="Purpose", description="The purpose of the dataset"
    )


class UploadDataset(BaseModel):
    name: str = Field(title="Name", description="The name of the dataset")
    task: str = Field(
        title="Task", description="The dataset related to a task"
    )
    prompt: Optional[str] = Field(
        title="Prompt", description="The dataset related to a prompt"
    )
    purpose: str = Field(
        title="Purpose", description="The purpose of the dataset"
    )
    description: Optional[str] = Field(
        title="Description", description="The description of the dataset"
    )
    file: List[Dict[str, Any]] = Field(
        title="File", description="The dataset file"
    )
