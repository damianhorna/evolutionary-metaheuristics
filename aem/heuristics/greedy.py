from aem.heuristics.heuristic import Heuristic
from typing import List
import numpy as np
import math


class Greedy(Heuristic):
    def __init__(self, graph):
        super().__init__(graph)

    def get_insertion_costs(self, cycle: List[int]):
        cycle_set = set(cycle)
        not_used_idx = [x for x in range(self.graph.no_of_vertices()) if x not in cycle_set]
        roll = [cycle[-1]] + cycle[:-1]  # np.roll(cycle, 1)
        return (
            self.graph.adjacency_matrix[cycle][:, not_used_idx].T + self.graph.adjacency_matrix[not_used_idx][:, roll] - \
            self.graph.adjacency_matrix[cycle, roll],
            not_used_idx)

    # def cost_of_insert(self, idx: int, position: int, cycle: List[int]):
    #     first_position = (position - 1) % len(cycle)
    #     second_position = position
    #     first_idx = cycle[first_position]
    #     second_idx = cycle[second_position]
    #     return self.graph.adjacency_matrix[first_idx][idx] + self.graph.adjacency_matrix[idx][second_idx] - \
    #            self.graph.adjacency_matrix[first_idx][second_idx]

    def build_cycle(self, start_vertex=0) -> list:
        cycle = [start_vertex]
        next_vertex = self.graph.get_closest_unvisited_neighbor_idx(from_vertex=cycle[-1], visited=cycle)
        cycle.append(next_vertex)

        while len(cycle) < math.ceil(self.graph.no_of_vertices() / 2):
            tmp, idx = self.get_insertion_costs(cycle)
            res = np.unravel_index(tmp.argmin(), tmp.shape)
            cycle.insert(res[1], idx[res[0]])
        return cycle
