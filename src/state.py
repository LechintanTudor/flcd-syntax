from dataclasses import dataclass
from functools import reduce
from item import Item


@dataclass
class State:
    items: list[Item]

    def __str__(self) -> str:
        return "\n".join([str(i) for i in self.items])

    @property
    def starting_item(self) -> Item:
        return self.items[0]
