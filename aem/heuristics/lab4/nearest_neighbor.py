from aem.heuristics.heuristic import Heuristic


class NearestNeighbor(Heuristic):
    def __init__(self, graph):
        super().__init__(graph)

    def build_cycle(self, cycle) -> list:
        while len(cycle) < self.graph.no_of_vertices() // 2:
            next_closest = self.graph.get_closest_unvisited_neighbor_idx(from_vertex=cycle[-1], visited=cycle)
            cycle.append(next_closest)
        return cycle
