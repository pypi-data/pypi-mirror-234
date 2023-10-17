import requests
from requests import HTTPError
from uplink import Body, Consumer, Query, delete, get, json
from uplink import put, post, response_handler, returns
from uplink.auth import BearerToken
from typing import List, Dict, Any

from honeyhive.api.models.utils import DeleteResponse

from honeyhive.api.models.tasks import (
    TaskCreationQuery,
    ListTaskResponse,
    TaskResponse,
    TaskUpdateQuery
)

from honeyhive.api.models.evaluations import (
    EvaluationLoggingQuery,
    SuccessResponse
)

from honeyhive.api.models.prompts import (
    ListPromptResponse,
    PromptResponse,
    PromptCreationQuery,
    PromptUpdateQuery
)

from honeyhive.api.models.fine_tuned_models import (
    ListFineTunedModelResponse,
    FineTunedModelResponse
)

from honeyhive.api.models.datasets import (
    ListDatasetResponse,
    DatasetResponse,
    FetchDataset,
    UploadDataset
)

from honeyhive.api.models.generations import (
    ListGenerationResponse,
    GenerationResponse,
    GenerateQuery,
    GenerationLoggingQuery,
    Generation
)

from honeyhive.api.models.chat import (
    ChatQuery,
    ChatResponse
)

from honeyhive.api.models.feedback import (
    FeedbackQuery,
    FeedbackResponse
)

from honeyhive.api.models.metrics import (
    ListMetricResponse,
    MetricResponse,
    MetricRequest
)

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


def raise_for_status(response: requests.Response):
    """Checks whether the response was successful."""
    try:
        response.raise_for_status()
        return response
    finally:
        if response.status_code >= 400:
            raise HTTPError(response.text)


@response_handler(raise_for_status)
class HoneyHive(Consumer):
    """HoneyHive API Client"""

    # Tasks API
    @returns.json
    @get("/tasks", args={"name": Body})
    def get_tasks(
        self,
        name: Body(type=str) = None,
    ) -> List[TaskResponse]:
        """Get all tasks"""
    
    @json
    @returns.json
    @post("/tasks", args={"task": Body(TaskCreationQuery)})
    def create_task(
        self,
        task: Body(TaskCreationQuery),
    ) -> TaskResponse:
        """Create a task"""

    @json
    @returns.json
    @put("/tasks/{id}", args={"task": Body(TaskUpdateQuery)})
    def update_task(
        self,
        id: str,
        task: Body(TaskUpdateQuery),
    ) -> TaskResponse:
        """Update a task"""
    
    @returns.json
    @delete("/tasks/{name}")
    def delete_task(
        self,
        name: str,
    ) -> DeleteResponse:
        """Delete a task"""
    
    @returns.json
    @get("/generations", args={"task": Query, "prompt": Query, "model_id": Query})
    def get_generations(
        self,
        task: Query = None,
        prompt: Query = None,
        model_id: Query = None
    ) -> List[Generation]:
        """Get all generations"""
    
    # Prompts API
    @returns.json
    @get("/prompts", args={"task": Query, "name": Query})
    def get_prompts(
        self,
        task: Query = None,
        name: Query = None
    ) -> List[PromptResponse]:
        """Get all prompts"""

    @json
    @returns.json
    @post("/prompts", args={"prompt": Body(PromptCreationQuery)})
    def create_prompt(
        self,
        prompt: Body(PromptCreationQuery),
    ) -> PromptResponse:
        """Create a prompt"""
    
    @returns.json
    @put("/prompts/{id}", args={"prompt": Body(PromptUpdateQuery)})
    def update_prompt(
        self,
        id: str,
        prompt: Body(PromptUpdateQuery),
    ) -> PromptResponse:
        """Update a prompt"""
    
    @returns.json
    @delete("/prompts/{name}")
    def delete_prompt(
        self,
        name: str,
    ) -> DeleteResponse:
        """Delete a prompt"""
    

    # Fine Tuned Models API
    @returns.json
    @get("/fine_tuned_models", args={"task": Query, "model_id": Query})
    def get_fine_tuned_models(
        self,
        task: Query = Query(None),
        model_id: Query = Query(None),
    ) -> List[FineTunedModelResponse]:
        """Get all fine tuned models"""
    
    @returns.json
    @get("/fine_tuned_models/{id}")
    def get_fine_tuned_model(
        self,
        id: str,
    ) -> FineTunedModelResponse:
        """Get a fine tuned model"""
    
    # Datasets API
    @returns.json
    @get("/datasets", args={"task": Query, "prompt": Query, "name": Query, "purpose": Query})
    def get_datasets(
        self,
        task: Query = None,
        prompt: Query = None,
        name: Query = None,
        purpose: Query = None,
    ) -> List[DatasetResponse]:
        """Get all datasets"""
    
    @json
    @returns.json
    @post("/datasets", args={"dataset": Body(type=UploadDataset)})
    def create_dataset(
        self,
        dataset: Body(type=UploadDataset),
    ) -> DatasetResponse:
        """Create a dataset"""
    
    @returns.json
    @get("/datasets/{name}")
    def get_dataset(
        self,
        name: str,
    ) -> DatasetResponse:
        """Get a dataset"""
    
    @returns.json
    @delete("/datasets/{name}")
    def delete_dataset(
        self,
        name: str,
    ) -> DeleteResponse:
        """Delete a dataset"""
    
    # Metrics API
    @returns.json
    @get("/metrics", args={"task": Query, "metric_id": Query})
    def get_metrics(
        self,
        task: Query = Query(None),
        metric_id: Query = Query(None),
    ) -> List[MetricResponse]:
        """Get all metrics"""

    @returns.json
    @post("/metrics", args={"metric": Body(MetricRequest)})
    def create_metric(
        self,
        metric: Body(MetricRequest),
    ) -> MetricResponse:
        """Create a metric"""
    
    @returns.json
    @get("/metrics/{id}")
    def get_metric(
        self,
        id: str,
    ) -> MetricResponse:
        """Get a metric"""
    
    @returns.json
    @delete("/metrics/{id}")
    def delete_metric(
        self,
        id: str,
    ) -> DeleteResponse:
        """Delete a metric"""
    
    # Generations API
    @json
    @returns.json
    @post("/generations", args={"generation": Body(GenerateQuery)})
    def generate(
        self,
        generation: Body(GenerateQuery),
    ) -> GenerationResponse:
        """Generate a text"""
    
    # Generations API stream
    @json
    @post("/generations", args={"generation": Body(GenerateQuery)})
    def generate_stream(
        self,
        generation: Body(GenerateQuery),
    ):
        """Generate a text"""
    
    # Chat API
    @json
    @returns.json
    @post("/chat", args={"chat": Body(ChatQuery)})
    def chat(
        self,
        chat: Body(ChatQuery),
    ) -> ChatResponse:
        """Generate a chat completion"""

    # Chat API
    @json
    @post("/chat", args={"chat": Body(ChatQuery)})
    def chat_stream(
        self,
        chat: Body(ChatQuery),
    ):
        """Generate a chat completion stream"""
    
    # Log Generation
    @json
    @returns.json
    @post("/generations/log", args={"generation": Body(GenerationLoggingQuery)})
    def log_generation(
        self,
        generation: Body(GenerationLoggingQuery),
    ) -> GenerationResponse:
        """Generate a text"""
    
    # Feedback API
    @json
    @returns.json
    @post("/feedback", args={"feedback": Body(FeedbackQuery)})
    def feedback(
        self,
        feedback: Body(FeedbackQuery),
    ) -> FeedbackResponse:
        """Send feedback"""
    
    # Evaluations API
    @json
    @returns.json
    @post("/evaluations", args={"evaluation": Body(EvaluationLoggingQuery)})
    def log_evaluation(
        self,
        evaluation: Body(EvaluationLoggingQuery),
    ) -> SuccessResponse:
        """Log an evaluation"""
    
    # Sessions API
    @json
    @returns.json
    @post("/session/start", args={"session": Body(SessionStartQuery)})
    def start_session(
        self,
        session: Body(SessionStartQuery),
    ) -> SessionStartResponse:
        """Start a session"""
    
    @json
    @returns.json
    @post("/session/{session_id}/end")
    def end_session(
        self,
        session_id: str,
    ) -> SessionEndResponse:
        """End a session"""
    
    @json
    @returns.json
    @post("/session/{session_id}/event", args={"session": Body(SessionEventQuery)})
    def log_event(
        self,
        session_id: str,
        session: Body(SessionEventQuery),
    ) -> SessionEventResponse:
        """Log an event"""
    
    @json
    @returns.json
    @post("/session/{session_id}/feedback", args={"session": Body(SessionFeedback)})
    def log_session_feedback(
        self,
        session_id: str,
        session: Body(SessionFeedback),
    ) -> SuccessResponse:
        """Log session feedback"""
    
    @json
    @returns.json
    @get("/session/{session_id}")
    def get_session(
        self,
        session_id: str,
    ) -> SessionEventQuery:
        """Get a session"""
    
    @json
    @returns.json
    @get("/session", args={"query": Body(SessionQuery)})
    def get_sessions(
        self,
        query: SessionQuery,
    ) -> List[SessionEventQuery]:
        """Get all sessions"""
    
    @json
    @returns.json
    @post("/sessions/{session_id}/traces", args={"trace": Body(SessionTrace)})
    def log_trace(
        self,
        session_id: str,
        trace: Body(SessionTrace),
    ) -> SuccessResponse:
        """Log a trace"""

def get_client(base_url: str, api_key: str) -> HoneyHive:
    """Get a HoneyHive API client"""
    return HoneyHive(base_url=base_url, auth=BearerToken(api_key))
