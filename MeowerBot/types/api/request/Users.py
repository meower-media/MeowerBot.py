from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import Literal
from typing import TypedDict

class UpdateRelationshipBody(TypedDict):
    state: Literal[0, 1, 2]