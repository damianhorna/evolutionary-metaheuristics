from aem.heuristics.heuristic import Heuristic


class Greedy(Heuristic):
    def __init__(self, graph):
        super().__init__(graph)

    def build_cycle(self, start_vertex=0) -> list:
        cycle = [start_vertex]
        next_vertex = self.graph.get_closest_unvisited_neighbor_idx(from_vertex=cycle[-1], visited=cycle)
        cycle.append(next_vertex)
        while len(cycle) < 50:
            # for each vertex find two visited that are closest and compute cost
            min_cost = float('inf')
            min_cost_vertex_idx = None
            for i in range(self.graph.no_of_vertices()):
                if i not in cycle:
                    first_closest = self.graph.get_closest_visited_idx(from_vertex=i, visited=cycle)
                    tmp_cycle = [i for i in cycle if i != first_closest]
                    second_closest = self.graph.get_closest_visited_idx(from_vertex=i, visited=tmp_cycle)

                    insertion_cost = self.graph.cost(first_closest, i) + self.graph.cost(second_closest, i)
                    if insertion_cost < min_cost:
                        min_cost = insertion_cost
                        min_cost_vertex_idx = i
            cycle.append(min_cost_vertex_idx)
        return cycle
