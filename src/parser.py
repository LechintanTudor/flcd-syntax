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
    """For the given item, returns the next symbol after dot, if any."""
    try:
        dot_index = item.rhp.index(Dot)

        if dot_index < len(item.rhp) - 1:
            return item.rhp[dot_index + 1]
        else:
            return None
    except ValueError:
        return None


def get_item_with_shifted_dot(item: Item) -> Optional[Item]:
    """
    If the given item has a dot in a non-final position, returns the item with the
    dot and the next symbol after the dot swapped.
    """
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
    """Returns the topmost state in the stack, if any."""
    for element in reversed(stack):
        if isinstance(element, int):
            return element

    return None


def remove_production(stack: list, production: Production) -> bool:
    """
    Removes the given production from the stack and returns whether the removal was
    successful.
    """
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
    """Parser for a provided grammar."""

    def __init__(self, grammar: Grammar):
        self._augmented_grammar = grammar.augment()
        self._canonical_collection = self.canonical_collection()
        self._lr0_table = Lr0Table(self._augmented_grammar, self._canonical_collection)

    def closure(self, starting_item: Item) -> State:
        """Computes a state from the provided starting item."""
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
        """
        Returns the state obtained from the closure of the shifted item that contains the provided
        symbol after the dot, if any.
        """
        for item in state.items:
            symbol_after_dot = get_symbol_after_dot(item)

            if symbol_after_dot != symbol:
                continue

            shifted_item = get_item_with_shifted_dot(item)
            return self.closure(shifted_item)

        return None

    def canonical_collection(self) -> CanonicalCollection:
        """Returns the canonical collection generated from the augmented grammar."""
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
        """
        Returns the augmented grammar generated from the grammar provided when
        creating the parser.
        """
        return self._augmented_grammar

    @property
    def lr0_table(self) -> Lr0Table:
        """Returns the lr0 table associated with the grammar provided when creating the parser."""
        return self._lr0_table

    def parse(self, terminals: list[Terminal]) -> list[Production]:
        """Parses a list of terminals into a list of productions."""
        alfa = ["$", 0]
        beta = terminals + ["$"]
        pi = []

        while self._lr0_table.actions[alfa[-1]].kind != ActionType.ACCEPT:
            state_index = get_topmost_state_index(alfa)
            action = self._lr0_table.actions[state_index]

            if action.kind == ActionType.SHIFT:
                next_state_index = self._lr0_table.gotos[state_index][beta[0]]

                if next_state_index is None:
                    raise ValueError("Parser error")

                alfa += [beta[0], next_state_index]
                beta.pop(0)
            elif action.kind == ActionType.REDUCE:
                if remove_production(alfa, action.production):
                    state_index = get_topmost_state_index(alfa)
                    next_state_index = self._lr0_table.gotos[state_index][
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

        if len(beta) != 1:
            raise ValueError("Input stack not empty")

        return pi
