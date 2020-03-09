from aem.tsp_reader import TSPReader
import numpy as np


class Node:
    def __init__(self, node_name, x, y):
        self.node_name = node_name
        self.x = x
        self.y = y


lines = TSPReader().read("../data/kroA100.tsp")
lines = [line.strip("\n").split(" ") for line in lines]
nodes = [Node(node_no, int(x), int(y)) for node_no, x, y in lines]

adjacency_matrix = np.zeros((len(nodes), len(nodes)))
for i, node_a in enumerate(nodes):
    for j, node_b in enumerate(nodes):
        adjacency_matrix[i,j] = np.round(np.sqrt((node_a.x - node_b.x) ** 2 + (node_a.y - node_b.y) ** 2), 0)

print(adjacency_matrix)


print("test")