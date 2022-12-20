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
    for item in state.items:
        try:
            dot_index = item.rhp.index(Dot)

            if dot_index < len(item.rhp) - 1:
                return True
        except ValueError:
            pass

    return False


def should_reduce(state: State) -> Optional[Production]:
    for item in state.items:
        try:
            dot_index = item.rhp.index(Dot)

            if dot_index == len(item.rhp) - 1:
                return Production(item.lhp, item.rhp[:-1])
        except:
            pass

    return None


def should_accept(state: State, starting_item: Item) -> bool:
    end_item = Item(starting_item.lhp, starting_item.rhp[1:] + [Dot])
    return end_item in state.items


def get_action(state: State, starting_item: Item) -> Action:
    if should_accept(state, starting_item):
        return Action(ActionType.ACCEPT)
    elif should_shift(state):
        return Action(ActionType.SHIFT)
    elif (production := should_reduce(state)) is not None:
        return Action(ActionType.REDUCE, production)
    else:
        return Action(ActionType.ERROR)


def get_goto_row(
    augmented_grammar: AugmentedGrammar,
    canonical_collection: CanonicalCollection,
    state_index: int,
) -> dict[Symbol, Optional[int]]:
    goto_row = {symbol: None for symbol in augmented_grammar.symbols()}

    if state_index not in canonical_collection.edges:
        return goto_row

    for edge in canonical_collection.edges[state_index]:
        goto_row[edge.symbol] = edge.state_index

    return goto_row


class Lr0Table:
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
