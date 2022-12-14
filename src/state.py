import copy


class State:
    def __init__(self, productions: dict[str, list[list[str]]] = None):
        if productions is None:
            self._productions = {}
        else:
            self._productions = copy.deepcopy(productions)

    def add_production(self, src: str, dst: list[str]) -> bool:
        if src not in self._productions:
            self._productions[src] = []

        if dst in self._productions[src]:
            return False

        self._productions.append(dst)
        return True

    def add_productions(self, src: str, dst_list: list[list[str]]) -> bool:
        if src not in self._productions:
            self._productions[src] = []

        added_at_least_one_production = False

        for dst in dst_list:
            if dst not in self._productions[src]:
                self._productions.append(dst)
                added_at_least_one_production = True

        return added_at_least_one_production

    def iter_productions(self):
        for src, dst_list in self._productions:
            for dst in dst_list:
                yield src, dst
