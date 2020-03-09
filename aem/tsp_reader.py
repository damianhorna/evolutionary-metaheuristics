from aem.graph import Graph
from aem.node import Node
import numpy as np


class TSPReader:
    @staticmethod
    def read(path):
        f = open(path, 'r')
        x = f.readlines()
        f.close()
        return x[6:-1]

    def read_as_graph(self, path: str) -> Graph:
        lines = self.read(path)
        lines = [line.strip("\n").split(" ") for line in lines]
        nodes = [Node(node_no, int(x), int(y)) for node_no, x, y in lines]

        adjacency_matrix = np.zeros((len(nodes), len(nodes)))
        for i, node_a in enumerate(nodes):
            for j, node_b in enumerate(nodes):
                adjacency_matrix[i, j] = np.round(np.sqrt((node_a.x - node_b.x) ** 2 + (node_a.y - node_b.y) ** 2), 0)

        g = Graph(adjacency_matrix)
        return g
