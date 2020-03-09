from aem.tsp_reader import TSPReader
from aem.greedy import Greedy

graph = TSPReader().read_as_graph("../data/kroA100.tsp")
print(graph.adjacency_matrix)

greedy = Greedy(graph)

greedy.run()
