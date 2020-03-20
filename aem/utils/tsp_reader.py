from aem.shared.graph import Graph
from aem.shared.node import Node
import numpy as np


class TSPReader:
    @staticmethod
    def read(path):
        f = open(path, 'r')
        x = f.readlines()
        f.close()
        return x[6:-1]

    def read_graph_with_coords(self, path: str) -> Graph:
        lines = self.read(path)
        lines = [line.strip("\n").split(" ") for line in lines]
        nodes = [Node(node_name, int(x), int(y)) for node_name, x, y in lines]

        coords = {}
        for n in nodes:
            coords[int(n.node_name) - 1] = (n.x, n.y)  # assumes nodes are numbered starting from 1

        adjacency_matrix = np.zeros((len(nodes), len(nodes)))
        for i, node_a in enumerate(nodes):
            for j, node_b in enumerate(nodes):
                adjacency_matrix[i, j] = np.round(np.sqrt((node_a.x - node_b.x) ** 2 + (node_a.y - node_b.y) ** 2), 0)

        g = Graph(adjacency_matrix, coords)
        return g
