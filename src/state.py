from dataclasses import dataclass
from functools import reduce
from item import Item


@dataclass
class State:
    items: list[Item]

    def __str__(self) -> str:
        return "\n".join([str(i) for i in self.items])

    def __eq__(self, other) -> bool:
        if self is other:
            return True

        if not isinstance(other, State):
            return False

        if len(self.items) != len(other.items):
            return False

        for item in self.items:
            if item not in other.items:
                return False

        return True

    @property
    def starting_item(self) -> Item:
        return self.items[0]
