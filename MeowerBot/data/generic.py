from dataclasses import dataclass
from typing import NewType, TypeVar

from dataclasses_json import dataclass_json

T = TypeVar("T")
UUID = NewType("UUID", str)
BitFlag = NewType("BitFlag", int)


@dataclass_json
@dataclass
class Timestamp:
    d: str
    e: int
    h: str
    mi: str
    mo: str
    s: str
    y: str


@dataclass_json
@dataclass
class Post:
    _id: UUID
    isDeleted: bool
    p: str
    post_id: UUID
    post_origin: str
    t: Timestamp
    type: int
    u: str
