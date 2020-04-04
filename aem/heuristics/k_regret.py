from aem.heuristics.heuristic import Heuristic
import numpy as np
import math

class KRegret(Heuristic):
    def __init__(self, graph, k=1):
        super().__init__(graph)
        self.k = k

    def build_cycle(self, start_vertex=0) -> list:
        cycle = [start_vertex]
        next_vertex = self.graph.get_closest_unvisited_neighbor_idx(from_vertex=cycle[-1], visited=cycle)
        cycle.append(next_vertex)

        available = [x for x in range(self.graph.no_of_vertices()) if x not in cycle]
        expected_no_of_vertices = math.ceil(self.graph.no_of_vertices() / 2)
        while len(cycle) < expected_no_of_vertices:
            costs = self.compute_insertion_costs(cycle, available)

            costs_sorted_idx = costs.argsort(axis=1)
            costs_sorted = costs.copy()
            costs_sorted.sort(axis=1)

            poz = np.argmax(np.sum(costs_sorted[:, 1:self.k + 1], axis=1) - costs_sorted[:, 0])

            cycle.insert(costs_sorted_idx[poz][0], available[poz])
            available.pop(poz)

        return cycle

    def compute_insertion_costs(self, cycle: list, available: list) -> dict:
        roll = [cycle[-1]] + cycle[:-1]  # np.roll(cycle, 1)
        res = self.graph.adjacency_matrix[cycle][:, available].T + self.graph.adjacency_matrix[available][:, roll] - \
              self.graph.adjacency_matrix[cycle, roll]
        return res


class KRegretFilter(Heuristic):
    def __init__(self, graph, k=1):
        super().__init__(graph)
        self.k = k

    def build_cycle(self, start_vertex=0) -> list:
        cycle = [start_vertex]
        next_vertex = self.graph.get_closest_unvisited_neighbor_idx(from_vertex=cycle[-1], visited=cycle)
        cycle.append(next_vertex)

        available = [x for x in range(self.graph.no_of_vertices()) if x not in cycle]
        expected_no_of_vertices = math.ceil(self.graph.no_of_vertices() / 2)
        while len(cycle) < expected_no_of_vertices:
            costs = self.compute_insertion_costs(cycle, available)
            best_idx = np.argsort(np.min(costs, axis=1))[:expected_no_of_vertices - len(cycle)]

            costs = costs[best_idx]
            costs_sorted_idx = costs.argsort(axis=1)
            costs_sorted = costs.copy()
            costs_sorted.sort(axis=1)

            poz = np.argmax(np.sum(costs_sorted[:, 1:self.k + 1], axis=1) - costs_sorted[:, 0])

            cycle.insert(costs_sorted_idx[poz][0], available[best_idx[poz]])
            available.pop(best_idx[poz])

        return cycle

    def compute_insertion_costs(self, cycle: list, available: list) -> dict:
        roll = [cycle[-1]] + cycle[:-1]  # np.roll(cycle, 1)
        res = self.graph.adjacency_matrix[cycle][:, available].T + self.graph.adjacency_matrix[available][:, roll] - \
              self.graph.adjacency_matrix[cycle, roll]
        return res
