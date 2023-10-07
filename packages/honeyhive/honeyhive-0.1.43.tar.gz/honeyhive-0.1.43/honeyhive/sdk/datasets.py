from typing import Optional
from io import BufferedReader
import json

from honeyhive.sdk.init import honeyhive_client
from honeyhive.api.models.datasets import (
    UploadDataset,
    DatasetResponse,
    ListDatasetResponse,
    FetchDataset,
)
from honeyhive.api.models.utils import DeleteResponse


def get_datasets(
    name: Optional[str] = None,
    project: Optional[str] = None,
    prompt: Optional[str] = None,
    purpose: Optional[str] = None,
) -> ListDatasetResponse:
    """Get all datasets"""
    client = honeyhive_client()
    return client.get_datasets(
        name=name, task=project, prompt=prompt, purpose=purpose
    )


def get_dataset(name: str) -> DatasetResponse:
    """Get a dataset"""
    client = honeyhive_client()
    return client.get_dataset(name=name)


def create_dataset(
    name: str,
    project: str,
    purpose: str = None,
    file: BufferedReader = None,
    prompt: Optional[str] = None,
    description: Optional[str] = None,
) -> DatasetResponse:
    """Create a dataset"""
    client = honeyhive_client()

    file_contents = file.read()
    file.close()

    # validate the file_contents are a list of json objects
    try:
        file_contents = json.loads(file_contents)
    except json.JSONDecodeError:
        raise ValueError("File contents must be a list of json objects")

    return client.create_dataset(
        dataset=UploadDataset(
            name=name,
            task=project,
            prompt=prompt,
            purpose=purpose,
            description=description,
            file=file_contents,
        )
    )


def delete_dataset(name: str) -> DeleteResponse:
    """Delete a dataset"""
    client = honeyhive_client()
    return client.delete_dataset(name=name)


__all__ = ["get_datasets", "create_dataset", "get_dataset", "delete_dataset"]
