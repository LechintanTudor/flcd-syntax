from action import ActionType
from augmented_grammar import AugmentedGrammar
from canonical_collection import CanonicalCollection, StateIndexEdge
from dot import Dot
from grammar import Grammar
from item import Item
from lr0_table import Lr0Table
from parser_types import ItemSymbol, Symbol, Terminal
from state import State
from typing import Optional
from production import Production


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


def get_topmost_state_index(stack: list) -> Optional[int]:
    for element in reversed(stack):
        if isinstance(element, int):
            return element

    return None


def remove_production(stack: list, production: Production) -> bool:
    starting_index = len(stack) - 2 * len(production.rhp)

    if starting_index < 0:
        return False

    for i in range(starting_index, len(stack), 2):
        if stack[i] != production.rhp[(i - starting_index) // 2]:
            return False

    for _ in range(2 * len(production.rhp)):
        stack.pop()

    return True


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

    @property
    def augmented_grammar(self) -> AugmentedGrammar:
        return self._augmented_grammar

    def parse(self, terminals: list[Terminal]) -> list[Production]:
        canonical_collection = self.canonical_collection()
        lr0_table = Lr0Table(self._augmented_grammar, canonical_collection)

        alfa = ["$", 0]
        beta = terminals + ["$"]
        pi = []

        while lr0_table.actions[alfa[-1]].kind != ActionType.ACCEPT:
            state_index = get_topmost_state_index(alfa)
            action = lr0_table.actions[state_index]

            if action.kind == ActionType.SHIFT:
                next_state_index = lr0_table.gotos[state_index][beta[0]]

                if next_state_index is None:
                    raise ValueError("Parser error")

                alfa += [beta[0], next_state_index]
                beta.pop(0)
            elif action.kind == ActionType.REDUCE:
                if remove_production(alfa, action.production):
                    state_index = get_topmost_state_index(alfa)
                    next_state_index = lr0_table.gotos[state_index][
                        action.production.lhp
                    ]
                    alfa += [action.production.lhp, next_state_index]
                    pi.insert(0, action.production)
                else:
                    raise ValueError("Parser error")
            elif action.kind == ActionType.ACCEPT:
                return pi
            else:
                raise ValueError("Parser error")

        return pi
