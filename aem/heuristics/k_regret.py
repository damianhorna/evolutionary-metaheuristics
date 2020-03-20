from aem.heuristics.heuristic import Heuristic


class KRegret(Heuristic):
    def __init__(self, graph):
        super().__init__(graph)

    def build_cycle(self, start_vertex=0) -> list:
        cycle = [start_vertex]
        return cycle