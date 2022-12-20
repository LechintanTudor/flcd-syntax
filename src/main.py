from grammar import Grammar
from parser import Parser
from item import Item
from dot import Dot
from lr0_table import Lr0Table


if __name__ == "__main__":
    grammar = Grammar.load_from_json("docs/simple.json")
    parser = Parser(grammar)
    canonical_collection = parser.canonical_collection()
    lr0_table = Lr0Table(parser.augmented_grammar, canonical_collection)
    print(lr0_table)
