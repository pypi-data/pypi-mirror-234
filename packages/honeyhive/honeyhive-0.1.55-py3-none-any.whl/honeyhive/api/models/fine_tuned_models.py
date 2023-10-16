from typing import Optional, List
from pydantic import BaseModel, Field
import datetime


class FineTunedModelResponse(BaseModel):
    id: str = Field(
        title="Fine Tuned Model ID",
        description="The unique ID of the fine tuned model",
    )
    object: str = Field(
        title="Object", description="The object type of the fine tuned model"
    )
    model: str = Field(
        title="Model", description="The model used for fine tuning"
    )
    created_at: datetime.datetime = Field(
        title="Created At",
        description="The date and time when the fine tuned model was created",
    )
    updated_at: datetime.datetime = Field(
        title="Updated At",
        description="The date and time when the fine tuned model was last updated",
    )
    fine_tuned_model: Optional[str] = Field(
        title="Fine Tuned Model", description="The fine tuned model"
    )
    hyperparams: Optional[str] = Field(
        title="Hyperparameters",
        description="The hyperparameters used for fine tuning",
    )
    org_id: str = Field(
        title="Organization ID",
        description="The unique ID of the organization",
    )
    result_files: Optional[str] = Field(
        title="Result Files",
        description="The result files of the fine tuned model",
    )
    status: str = Field(
        title="Status", description="The status of the fine tuned model"
    )
    validation_files: Optional[str] = Field(
        title="Validation Files",
        description="The validation files used for fine tuning",
    )
    training_files: Optional[str] = Field(
        title="Training Files",
        description="The training files used for fine tuning",
    )


class ListFineTunedModelResponse(BaseModel):
    data: List[FineTunedModelResponse] = Field(
        title="Data", description="The list of fine tuned models"
    )
