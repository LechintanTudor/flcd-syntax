from augmented_grammar import AugmentedGrammar
from action import Action, ActionType
from canonical_collection import CanonicalCollection
from dot import Dot
from state import State
from production import Production
from item import Item
from typing import Optional
from parser_types import Symbol


def should_shift(state: State) -> bool:
    """Checks if the given state requires a shift action."""
    for item in state.items:
        try:
            dot_index = item.rhp.index(Dot)

            if dot_index < len(item.rhp) - 1:
                return True
        except ValueError:
            pass

    return False


def should_reduce(state: State) -> Optional[Production]:
    """
    Checks if the given state requires a reduce action.
    If so, returns the production used for reduction.
    """
    res_production: Optional[Production] = None
    for item in state.items:
        try:
            dot_index = item.rhp.index(Dot)

            if dot_index == len(item.rhp) - 1:
                if res_production:
                    raise ValueError(f"!reduce-reduce conflict in state!\n{state}")
                res_production = Production(item.lhp, item.rhp[:-1])
        except:
            pass

    return res_production


def should_accept(state: State, starting_item: Item) -> bool:
    """Checks if the given state requires an accept action."""
    end_item = Item(starting_item.lhp, starting_item.rhp[1:] + [Dot])
    return end_item in state.items


def get_action(state: State, starting_item: Item) -> Action:
    """Returns the action required by the given state."""
    if should_accept(state, starting_item):
        return Action(ActionType.ACCEPT)

    future_actions: list[Action] = []

    if should_shift(state):
        future_actions.append(Action(ActionType.SHIFT))
    if (production := should_reduce(state)) is not None:
        future_actions.append(Action(ActionType.REDUCE, production))

    if len(future_actions) == 1:
        return future_actions[0]
    if len(future_actions) > 1:
        raise ValueError(f"!shift-reduce conflict in state!\n{state}")

    return Action(ActionType.ERROR)


def get_goto_row(
    augmented_grammar: AugmentedGrammar,
    canonical_collection: CanonicalCollection,
    state_index: int,
) -> dict[Symbol, Optional[int]]:
    """Returns the goto row of the state at the given index."""
    goto_row = {symbol: None for symbol in augmented_grammar.symbols()}

    if state_index not in canonical_collection.edges:
        return goto_row

    for edge in canonical_collection.edges[state_index]:
        goto_row[edge.symbol] = edge.state_index

    return goto_row


class Lr0Table:
    """Lr0 table computed from an augmented grammar."""

    def __init__(
        self,
        augmented_grammar: AugmentedGrammar,
        canonical_collection: CanonicalCollection,
    ):
        starting_item = canonical_collection.starting_item

        self.actions = [
            get_action(state, starting_item) for state in canonical_collection.states
        ]

        self.gotos = [
            get_goto_row(augmented_grammar, canonical_collection, state_index)
            for state_index in range(len(canonical_collection.states))
        ]

    def __str__(self) -> str:
        result_str = ""

        for i, (action, gotos) in enumerate(zip(self.actions, self.gotos)):
            result_str = f"{result_str}\n{i}: {action} | {gotos}"

        return result_str
