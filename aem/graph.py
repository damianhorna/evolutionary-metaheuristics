import numpy as np


class Graph:

    def __init__(self, adjacency_matrix):
        self.adjacency_matrix = adjacency_matrix
        self.cache = {}

    def get_closest_neighbor_index(self, vertex_no):
        if vertex_no in self.cache:
            return self.cache[vertex_no]
        valid_idx = np.where(self.adjacency_matrix[vertex_no, :] != 0)[0]
        out = valid_idx[self.adjacency_matrix[vertex_no, :][valid_idx].argmin()]
        self.cache[vertex_no] = out
        return out

    def no_of_vertices(self) -> int:
        return self.adjacency_matrix.shape[0]

    def compute_cycle_length(self, cycle) -> int:
        cycle_length = 0
        for i in range(len(cycle)):
            v1 = cycle[i]
            v2 = cycle[(i+1) % len(cycle)]
            cycle_length += self.adjacency_matrix[v1, v2]
        return cycle_length
