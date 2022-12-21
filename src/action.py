from enum import auto, Enum
from dataclasses import dataclass
from typing import Optional
from production import Production


class ActionType(Enum):
    """Type of action."""

    SHIFT = auto()
    REDUCE = auto()
    ACCEPT = auto()
    ERROR = auto()


@dataclass
class Action:
    """Action that corresponds to a state in the LR0 table."""

    kind: ActionType
    production: Optional[Production] = None

    def __str__(self) -> str:
        if self.kind == ActionType.REDUCE:
            return f"Action(REDUCE, {self.production})"
        else:
            return f"Action({self.kind.name})"
