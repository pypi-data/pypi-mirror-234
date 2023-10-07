from honeyhive.api.models.sessions import (
    SessionStartQuery,
    SessionStartResponse,
    SessionEndResponse,
    SessionEventQuery,
    SessionEventResponse,
    SessionQuery,
    SessionTrace,
    SessionFeedback
)

from typing import Dict, List, Any, Optional

import asyncio
import inspect
import traceback

# TODO add error handling

def start(
    project: str,
    source: str,
    session_name: str = None,
    session_type: str = "chain",
    user_properties: Dict = None,
    metadata: Dict = None
):
    """Start a session"""
    from honeyhive.sdk.init import honeyhive_client
    client = honeyhive_client()

    import uuid
    session_id = str(uuid.uuid4())

    if metadata is None:
        metadata = {}
    
    session_init = client.start_session(
        session=SessionStartQuery(
            session_id=session_id,
            project=project,
            source=source,
            session_name=session_name,
            session_type=session_type,
            user_properties=user_properties,
            metadata=metadata
        )
    )

    return session_init

def end(
    session_id: str
):
    """End a session"""
    from honeyhive.sdk.init import honeyhive_client
    client = honeyhive_client()

    client.end_session(
        session_id=session_id
    )

    return {
        "success": True
    }

def log_event(
    session_id: str,
    event_type: str,
    event_name: str,
    config: Dict,
    input: Dict,
    output: str,
    event_id: str = None,
    error: str = None,
    duration: float = None,
    children: List[Dict] = None,
    parent_id: str = None,
    event_properties: Dict = None,
    user_properties: Dict = None,
    metrics: Dict = None,
    feedback: Dict = None,
    metadata: Dict = None
):
    """Log an event"""
    from honeyhive.sdk.init import honeyhive_client
    client = honeyhive_client()

    if event_id is None:
        import uuid
        event_id = str(uuid.uuid4())
    
    client.log_event(
        session_id=session_id,
        session=SessionEventQuery(
            session_id=session_id,
            created_at="",
            event_id=event_id,
            event_type=event_type,
            event_name=event_name,
            config=config,
            inputs=input,
            output=output,
            error=error,
            duration=duration,
            children=children,
            parent_id=parent_id,
            event_properties=event_properties,
            user_properties=user_properties,
            metrics=metrics,
            feedback=feedback,
            metadata=metadata
        )
    )

    return {
        "success": True,
        "event_id": event_id
    }

def feedback(
    session_id: str,
    feedback: Dict,
    event_id: str = None,
    ground_truth: str = None
):
    """Log session feedback"""
    from honeyhive.sdk.init import honeyhive_client
    client = honeyhive_client()

    # TODO add logic to handle nesting feedback

    client.log_session_feedback(
        session_id=session_id,
        session=SessionFeedback(
            feedback=feedback,
            event_id=event_id,
            ground_truth=ground_truth
        )
    )

    return {
        "success": True
    }

def get(
    session_id: str
):
    """Get a session"""
    from honeyhive.sdk.init import honeyhive_client
    client = honeyhive_client()

    session = client.get_session(
        session_id=session_id
    )

    return session

def get_all(
    project: str,
    query: Dict,
    limit: int = None
):
    """Get all sessions"""
    from honeyhive.sdk.init import honeyhive_client
    client = honeyhive_client()

    sessions = client.get_sessions(
        query=SessionQuery(
            project=project,
            query=query,
            limit=limit
        )
    )

    return sessions

import traceback

def trace_chain(func):
  def wrapper(*args, **kwargs):
    stack = traceback.extract_stack()
    for frame_summary in stack:
      f = inspect.currentframe()
      print(f.f_locals)
    return func(*args, **kwargs)
  return wrapper


__all__ = [
    "start",
    "end",
    "log_event",
    "feedback",
    "trace_chain",
    "get",
    "get_all"
]