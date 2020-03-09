import numpy as np


class Graph:

    def __init__(self, adjacency_matrix):
        self.adjacency_matrix = adjacency_matrix

    def get_closest_neighbor_index(self, vertex_no):
        valid_idx = np.where(self.adjacency_matrix[vertex_no, :] != 0)[0]
        out = valid_idx[self.adjacency_matrix[vertex_no, :][valid_idx].argmin()]
        return out
