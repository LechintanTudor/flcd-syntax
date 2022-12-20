from grammar import Grammar
from parser import Parser
from item import Item
from dot import Dot
from lr0_table import Lr0Table


if __name__ == "__main__":
    grammar = Grammar.load_from_json("docs/syntax.json")
    parser = Parser(grammar)
    result = parser.parse(
        [
            "~",
            "var",
            "identifier",
            ":",
            "type",
            ";",
            "read",
            "(",
            "identifier",
            ")",
            ";",
            "~",
        ]
    )

    for r in result:
        print(r)
