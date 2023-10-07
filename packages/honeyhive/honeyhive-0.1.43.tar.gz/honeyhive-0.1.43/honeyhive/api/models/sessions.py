from typing import Dict, List, Optional, Any

from pydantic import BaseModel, Field

class SessionStartQuery(BaseModel):
    session_id: str = Field(
        title="Session ID",
        description="The ID of the session"
    )
    project: str = Field(
        title="Project",
        description="The project name for the session"
    )
    source: str = Field(
        title="Source",
        description="The source of the session"
    )
    session_name: Optional[str] = Field(
        title="Session Name",
        description="The name for the session"
    )
    session_type: Optional[str] = Field(
        title="Session Type",
        description="The type for the session, default is chain"
    )
    user_properties: Optional[Dict] = Field(
        title="User Properties",
        description="The user properties for the user starting the session"
    )
    metadata: Optional[Dict] = Field(
        title="Metadata",
        description="Metadata for the session"
    )

class SessionStartResponse(BaseModel):
    session_id: str = Field(
        title="Session ID",
        description="The ID of the started session"
    )
    project_id: str = Field(
        title="Project ID",
        description="The ID of the project for the session"
    )

class SessionEndResponse(BaseModel):
    success: bool = Field(
        title="Success",
        description="Whether ending the session was successful"
    )

class SessionEventQuery(BaseModel):
    created_at: str = Field(
        title="Created At",
        description="The time the event was created"
    )
    session_id: str = Field(
        title="Session ID",
        description="The ID of the session"
    )
    event_id: str = Field(
        title="Event ID",
        description="The ID of the event"
    )
    parent_id: Optional[Any] = Field(
        title="Parent ID",
        description="The parent ID of the event"
    )
    event_type: str = Field(
        title="Event Type",
        description="The type of the event"
    )
    event_name: str = Field(
        title="Event Name",
        description="The name for the event"
    )
    config: Dict = Field(
        title="Config",
        description="The configuration of LLM, Tool or other for the event"
    )
    children: Optional[List] = Field(
        title="Children",
        description="Child events"
    )
    inputs: Dict = Field(
        title="Inputs",
        description="Inputs to the event"
    )
    output: str = Field(
        title="Output", 
        description="Output of the event"
    )
    error: Optional[Any] = Field(
        title="Error",
        description="Error from the event"
    )
    source: Optional[str] = Field(
        title="Source",
        description="Source of the event"
    )
    duration: Optional[float] = Field(
        title="Duration",
        description="Duration of the event"
    )
    event_properties: Optional[Dict] = Field(
        title="Event Properties",
        description="Properties of the event"
    )
    user_properties: Optional[Dict] = Field(
        title="User Properties",
        description="User properties for the event"
    )
    metrics: Optional[Dict] = Field(
        title="Metrics",
        description="Metrics for the event"
    )
    feedback: Optional[Dict] = Field(
        title="Feedback",
        description="Feedback for the event"
    )
    metadata: Optional[Dict] = Field(
        title="Metadata",
        description="Metadata for the event"
    )

class SessionEventResponse(BaseModel):
    success: bool = Field(
        title="Success",
        description="Whether recording the event was successful"
    )
    event_id: str = Field(
        title="Event ID",
        description="The ID of the event"
    )

class SessionFeedback(BaseModel):
    feedback: Dict[str, Any] = Field(
        title="Feedback",
        description="The feedback for the session"
    )
    event_id: Optional[str] = Field(
        title="Event ID",
        description="The ID of the specific event to provide feedback for"
    )
    ground_truth: Optional[str] = Field(
        title="Ground Truth",
        description="The ground truth for the event/session"
    )

class SessionQuery(BaseModel):
    project: str = Field(
        title="Project",
        description="The project to query sessions for"
    )
    query: Dict = Field(
        title="Query",
        description="The query for finding sessions"
    )
    limit: Optional[int] = Field(  
        title="Limit",
        description="The maximum number of sessions to return"
    )

class SessionTrace(BaseModel):
    logs: List[SessionEventQuery] = Field(
        title="Logs",
        description="The trace logs for the session"
    )