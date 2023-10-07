from typing import Optional, Any, Dict
from pydantic import BaseModel, Field


class DeleteResponse(BaseModel):
    deleted: bool = Field(
        title="Deleted",
        description="The boolean value indicating whether the object was deleted or not",
    )
