from grammar import Grammar


class Console:
    def __init__(self):
        self.grammar = Grammar()
        self.cmds = {
            'load': self.handle_load_file,
            'terminals': self.handle_terminals,
            'nonterminals': self.handle_nonterminals,
            'productions': self.handle_productions
        }

    def handle_load_file(self):
        filename = input('Enter file name/relative path:\n').strip()
        try:
            self.grammar.load_from_file(filename)
            print('File loaded successfully')
        except Exception as e:
            print(e)

    def handle_terminals(self):
        print(self.grammar.get_terminals())

    def handle_nonterminals(self):
        print(self.grammar.get_non_terminals())

    def handle_productions(self):
        non_terminal = input('Enter non_terminal or press enter if you want to see all productions\n').strip()
        if len(non_terminal) == 0:
            print(self.grammar.get_productions())
        else:
            print(self.grammar.get_productions(non_terminal=non_terminal))

    def run(self):
        while True:
            self.print_menu()
            cmd = input('Enter your command: ')
            if cmd == 'exit':
                break
            if cmd not in self.cmds:
                print('Invalid command')
                continue
            self.cmds[cmd]()

    def print_menu(self):
        print('Commands:\n'
              '1. load - Load a grammar from a file\n'
              '2. terminals - Print the terminals from the grammar\n'
              '3. nonterminals - Print the nonterminals from the grammar\n'
              '4. productions - See the productions from the grammar\n'
              '5. exit')
