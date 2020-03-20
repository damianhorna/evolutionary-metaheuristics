from aem.heuristics.heuristic import Heuristic


class KRegret(Heuristic):
    def __init__(self, graph, k=1):
        super().__init__(graph)
        self.k = k

    def build_cycle(self, start_vertex=0) -> list:
        cycle = [start_vertex]
        next_vertex = self.graph.get_closest_unvisited_neighbor_idx(from_vertex=cycle[-1], visited=cycle)
        cycle.append(next_vertex)
        while len(cycle) < 50:
            # we can insert either first or second closest depending on cost (1-regret)
            idx_1, cost_1 = self.select_greedy(cycle)
            tmp_cycle = cycle + [idx_1]
            idx_2, cost_2 = self.select_greedy(tmp_cycle)
            total_cost_1_2 = cost_1 + cost_2

            idx_3, cost_3 = self.select_greedy(cycle, exclude=[idx_1])
            tmp_cycle = cycle + [idx_3]
            idx_4, cost_4 = self.select_greedy(tmp_cycle)
            total_cost_3_4 = cost_3 + cost_4

            if total_cost_1_2 < total_cost_3_4:
                cycle.append(idx_1)
            else:
                cycle.append(idx_3)

        return cycle

    def select_greedy(self, cycle, exclude=[]):
        min_cost = float('inf')
        min_cost_vertex_idx = None
        for i in range(self.graph.no_of_vertices()):
            if i not in cycle and i not in exclude:
                first_closest = self.graph.get_closest_visited_idx(from_vertex=i, visited=cycle)
                tmp_cycle = [i for i in cycle if i != first_closest]
                second_closest = self.graph.get_closest_visited_idx(from_vertex=i, visited=tmp_cycle)

                insertion_cost = self.graph.cost(first_closest, i) + self.graph.cost(second_closest, i)
                if insertion_cost < min_cost:
                    min_cost = insertion_cost
                    min_cost_vertex_idx = i
        return min_cost_vertex_idx, min_cost
