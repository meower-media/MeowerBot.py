from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import Literal

class UpdateRelationshipBody:
    state: Literal[0, 1, 2]