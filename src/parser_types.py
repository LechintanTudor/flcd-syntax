from typing import TypeVar, Union, NewType

Terminal = NewType("Terminal", str)
Nonterminal = NewType("Nonterminal", str)
Symbol = Union[Terminal, Nonterminal]
