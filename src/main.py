from grammar import Grammar
from parser import Parser
from item import Item
from dot import Dot
from lr0_table import Lr0Table


if __name__ == "__main__":
    grammar = Grammar.load_from_json("docs/simple.json")
    parser = Parser(grammar)

    print(f"{parser.lr0_table}\n")

    result = parser.parse(
        [
            "a",
            "b",
            "b",
            "b",
            "c",
        ]
    )

    for r in result:
        print(r)
