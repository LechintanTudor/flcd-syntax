from grammar import Grammar
from dot import Dot
from state import State
from item import Item
from typing import Optional
from parser_types import ItemSymbol, Symbol
from canonical_collection import CanonicalCollection, StateIndexEdge


def get_symbol_after_dot(item: Item) -> Optional[ItemSymbol]:
    try:
        dot_index = item.rhp.index(Dot)

        if dot_index < len(item.rhp) - 1:
            return item.rhp[dot_index + 1]
        else:
            return None
    except ValueError:
        return None


def get_item_with_shifted_dot(item: Item) -> Optional[Item]:
    try:
        dot_index = item.rhp.index(Dot)

        if dot_index == len(item.rhp) - 1:
            return None

        rhp = (
            item.rhp[:dot_index]
            + [item.rhp[dot_index + 1], Dot]
            + item.rhp[dot_index + 2 :]
        )

        return Item(item.lhp, rhp)
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

    def goto(self, state: State, symbol: Symbol) -> Optional[State]:
        for item in state.items:
            symbol_after_dot = get_symbol_after_dot(item)

            if symbol_after_dot != symbol:
                continue

            shifted_item = get_item_with_shifted_dot(item)
            return self.closure(shifted_item)

        return None

    def canonical_collection(self) -> CanonicalCollection:
        starting_item = next(
            self._augmented_grammar.items_for(self._augmented_grammar.start_nonterminal)
        )

        initial_state = self.closure(starting_item)

        states = [initial_state]
        edges = {}

        while True:
            new_state_found = False

            i = 0
            while i < len(states):
                state = states[i]

                for symbol in self._augmented_grammar.symbols():
                    next_state = self.goto(state, symbol)

                    if next_state is None:
                        continue

                    next_state_index = None

                    try:
                        next_state_index = states.index(next_state)
                    except ValueError:
                        next_state_index = len(states)
                        states.append(next_state)
                        new_state_found = True

                    if i not in edges:
                        edges[i] = []

                    state_index_edge = StateIndexEdge(symbol, next_state_index)

                    if not state_index_edge in edges[i]:
                        edges[i].append(state_index_edge)

                i += 1
                
            if not new_state_found:
                break

        return CanonicalCollection(states, edges)
