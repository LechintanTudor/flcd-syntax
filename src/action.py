from enum import auto, Enum
from dataclasses import dataclass
from typing import Optional
from production import Production


class ActionType(Enum):
    SHIFT = auto()
    REDUCE = auto()
    ACCEPT = auto()
    ERROR = auto()


@dataclass
class Action:
    kind: ActionType
    production: Optional[Production] = None

    def __str__(self) -> str:
        if self.kind == ActionType.REDUCE:
            return f"Action(REDUCE, {self.production})"
        else:
            return f"Action({self.kind.name})"
