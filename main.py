from aem.tsp_reader import TSPReader
from aem.greedy import Greedy

graph = TSPReader().read_as_graph("../data/kroA100.tsp")
print("Adjacency matrix:")
print(graph.adjacency_matrix)

greedy = Greedy(graph)

greedy_result = greedy.run()
greedy_result.print()
