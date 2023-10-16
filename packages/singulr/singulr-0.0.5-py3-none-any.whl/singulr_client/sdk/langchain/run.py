# Created by msinghal at 12/09/23
from __future__ import annotations
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Union
from uuid import UUID
from pydantic import BaseModel, Field, PrivateAttr, StrictBool, StrictFloat, StrictInt

SCORE_TYPE = Union[StrictBool, StrictInt, StrictFloat, None]
VALUE_TYPE = Union[Dict, StrictBool, StrictInt, StrictFloat, str, None]


class DataType(str, Enum):
    """Enum for dataset data types."""
    kv = "kv"
    llm = "llm"
    chat = "chat"


class DatasetBase(BaseModel):
    """Dataset base model."""

    name: str
    description: Optional[str] = None
    data_type: Optional[DataType] = None

    class Config:
        frozen = True


class DatasetCreate(DatasetBase):
    """Dataset create model."""

    id: Optional[UUID] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Dataset(DatasetBase):
    """Dataset ORM model."""

    id: UUID
    created_at: datetime
    modified_at: Optional[datetime] = Field(default=None)


class RunTypeEnum(str, Enum):
    """(Deprecated) Enum for run types. Use string directly."""

    tool = "tool"
    chain = "chain"
    llm = "llm"
    retriever = "retriever"
    embedding = "embedding"
    prompt = "prompt"
    parser = "parser"


class RunBase(BaseModel):
    """Base Run schema."""

    id: UUID
    name: str
    start_time: datetime
    run_type: str
    """The type of run, such as tool, chain, llm, retriever,
    embedding, prompt, parser."""
    end_time: Optional[datetime] = None
    extra: Optional[dict] = None
    error: Optional[str] = None
    serialized: Optional[dict]
    events: Optional[List[Dict]] = None
    inputs: dict
    outputs: Optional[dict] = None
    reference_example_id: Optional[UUID] = None
    parent_run_id: Optional[UUID] = None
    tags: Optional[List[str]] = None


class Run(RunBase):
    """Run schema when loading from the DB."""

    execution_order: int
    """The execution order of the run within a run trace."""
    session_id: Optional[UUID] = None
    """The project ID this run belongs to."""
    child_run_ids: Optional[List[UUID]] = None
    """The child run IDs of this run."""
    child_runs: Optional[List[Run]] = None
    """The child runs of this run, if instructed to load using the client
    These are not populated by default, as it is a heavier query to make."""
    feedback_stats: Optional[Dict[str, Any]] = None
    """Feedback stats for this run."""
    app_path: Optional[str] = None
    """Relative URL path of this run within the app."""
    _host_url: Optional[str] = PrivateAttr(default=None)

    def __init__(self, _host_url: Optional[str] = None, **kwargs: Any) -> None:
        """Initialize a Run object."""
        super().__init__(**kwargs)
        self._host_url = _host_url

    @property
    def url(self) -> Optional[str]:
        """URL of this run within the app."""
        if self._host_url and self.app_path:
            return f"{self._host_url}{self.app_path}"
        return None


class TracerSession(BaseModel):
    """TracerSession schema for the API.

    Sessions are also referred to as "Projects" in the UI.
    """

    id: UUID
    """The ID of the project."""
    start_time: datetime = Field(default_factory=datetime.utcnow)
    """The time the project was created."""
    name: Optional[str] = None
    """The name of the session."""
    extra: Optional[Dict[str, Any]] = None
    """Extra metadata for the project."""
    tenant_id: UUID
    """The tenant ID this project belongs to."""


class TracerSessionResult(TracerSession):
    """TracerSession schema returned when reading a project
    by ID. Sessions are also referred to as "Projects" in the UI."""

    run_count: Optional[int]
    """The number of runs in the project."""
    latency_p50: Optional[timedelta]
    """The median (50th percentile) latency for the project."""
    latency_p99: Optional[timedelta]
    """The 99th percentile latency for the project."""
    total_tokens: Optional[int]
    """The total number of tokens consumed in the project."""
    prompt_tokens: Optional[int]
    """The total number of prompt tokens consumed in the project."""
    completion_tokens: Optional[int]
    """The total number of completion tokens consumed in the project."""
    last_run_start_time: Optional[datetime]
    """The start time of the last run in the project."""
    feedback_stats: Optional[Dict[str, Any]]
    """Feedback stats for the project."""
    reference_dataset_ids: Optional[List[UUID]]
    """The reference dataset IDs this project's runs were generated on."""
    run_facets: Optional[List[Dict[str, Any]]]
    """Facets for the runs in the project."""
