from dataclasses import dataclass, field
from typing import Generic, List, Optional, TypeVar

from dataclasses_json import config, dataclass_json

from ..generic import Post, UUID

T = TypeVar("T")


@dataclass_json
@dataclass
class PagedRequest(Generic[T]):
    error: bool
    page: int = field(metadata=config(field_name="page#"))
    pages: int

    index: Optional[List[UUID]]
    autoget: Optional[List[T]]



@dataclass_json
@dataclass
class ReportDetails:
    comment: str
    reason: str
    time: int
    user: str


@dataclass_json
@dataclass
class Report:
    _id: UUID
    content: Post
    escalated: bool
    reports: List[ReportDetails]
    status: str
    type_: str = field(metadata=config(field_name="type"))



class ReportRequest(PagedRequest):
    autoget: List[Report]


@dataclass_json
@dataclass
class AdminNotesResponse:
    _id: str
    notes: str
    last_modified_by: str
    last_modified_at: int
    error: bool
