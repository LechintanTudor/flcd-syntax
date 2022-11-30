import json


class Grammar:
    def __init__(self):
        self.__non_terminals = []
        self.__terminals = []
        self.__productions = {}

    def load_from_file(self, filename):
        with open(filename, 'rt') as f:
            json_data = json.load(f)
            self.__terminals = json_data['terminals']
            self.__non_terminals = list(json_data['nonterminals'].keys())
            for non_terminal in self.__non_terminals:
                if non_terminal not in self.__productions:
                    self.__productions[non_terminal] = []
                self.__productions[non_terminal] = json_data['nonterminals'][non_terminal]

    def get_terminals(self):
        return self.__terminals

    def get_non_terminals(self):
        return self.__non_terminals

    def get_productions(self, non_terminal=None):
        if non_terminal:
            return self.__productions[non_terminal]
        return self.__productions

