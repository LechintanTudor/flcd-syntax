from grammar import Grammar
from dot import Dot
from state import State
from item import Item
from typing import Optional
from parser_types import ItemSymbol


def get_symbol_after_dot(item: Item) -> Optional[ItemSymbol]:
    try:
        dot_index = item.rhp.index(Dot)

        if dot_index < len(item.rhp) - 1:
            return item.rhp[dot_index + 1]
        else:
            return None
    except ValueError:
        return None


class Parser:
    def __init__(self, grammar: Grammar):
        self._augmented_grammar = grammar.augment()

    def closure(self, starting_item: Item) -> State:
        items = [starting_item]

        while True:
            items_changed = False

            for item in items:
                symbol_after_dot = get_symbol_after_dot(item)

                if symbol_after_dot is None:
                    continue

                for item in self._augmented_grammar.items_for(symbol_after_dot):
                    if item not in items:
                        items.append(item)
                        items_changed = True

            if not items_changed:
                break

        return State(items)
