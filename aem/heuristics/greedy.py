from aem.heuristics.heuristic import Heuristic


class Greedy(Heuristic):
    def __init__(self, graph):
        super().__init__(graph)

    def build_cycle(self, start_vertex=0) -> list:
        cycle = [start_vertex]
        next_vertex = self.graph.get_closest_unvisited_neighbor_idx(from_vertex=cycle[-1], visited=cycle)
        cycle.append(next_vertex)
        while len(cycle) < self.graph.no_of_vertices() // 2:
            best_cycle = None
            best_cycle_cost = float("inf")
            for i in range(self.graph.no_of_vertices()):
                if i not in cycle:
                    for j in range(len(cycle)):
                        tmp_cycle = cycle.copy()
                        tmp_cycle.insert(j, i)
                        cycle_cost = self.graph.compute_cycle_length(tmp_cycle)
                        if cycle_cost < best_cycle_cost:
                            best_cycle = tmp_cycle.copy()
                            best_cycle_cost = cycle_cost
            cycle = best_cycle.copy()
        return cycle
