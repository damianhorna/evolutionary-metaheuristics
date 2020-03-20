from aem.heuristics.heuristic import Heuristic


class KRegret(Heuristic):
    def __init__(self, graph, k=1):
        super().__init__(graph)
        self.k = k

    def build_cycle(self, start_vertex=0) -> list:
        cycle = [start_vertex]
        next_vertex = self.graph.get_closest_unvisited_neighbor_idx(from_vertex=cycle[-1], visited=cycle)
        cycle.append(next_vertex)
        while len(cycle) < self.graph.no_of_vertices() // 2:
            costs_dict = self.compute_insertion_costs(cycle)
            costs_dict = self.sort_insertion_costs(costs_dict)
            k_regret_dict = self.compute_k_regret_dict(costs_dict)
            best_candidate_to_insert = max(k_regret_dict, key=k_regret_dict.get)
            best_insert_position, best_insert_cost = costs_dict[best_candidate_to_insert][0]
            cycle.insert(best_insert_position, best_candidate_to_insert)
        return cycle

    def compute_k_regret_dict(self, costs_dict):
        k_regret_dict = {}
        for vertex in costs_dict:
            k_regret_dict[vertex] = 0
            for i in range(self.k):
                k_regret_dict[vertex] += costs_dict[vertex][i+1][1] - costs_dict[vertex][0][1]
        return k_regret_dict

    def compute_insertion_costs(self, cycle: list) -> dict:
        costs = {}
        for vertex in range(self.graph.no_of_vertices()):
            if vertex not in cycle:
                costs[vertex] = []
                for position in range(len(cycle)):
                    tmp_cycle = cycle.copy()
                    tmp_cycle.insert(position, vertex)
                    cycle_cost = self.graph.compute_cycle_length(tmp_cycle)
                    costs[vertex].append((position, cycle_cost))
        return costs

    @staticmethod
    def sort_insertion_costs(costs: dict) -> dict:
        for vertex in costs:
            costs[vertex] = sorted(costs[vertex], key=lambda x: x[1])
        return costs
