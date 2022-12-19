from grammar import Grammar
from parser import Parser
from item import Item
from dot import Dot


if __name__ == "__main__":
    grammar = Grammar.load_from_json("docs/simple.json")
    parser = Parser(grammar)
    print(parser.closure(Item("S'", [Dot, "S"])))
