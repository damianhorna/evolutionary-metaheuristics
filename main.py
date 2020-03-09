from aem.tsp_reader import TSPReader


graph = TSPReader().read_as_graph("../data/kroA100.tsp")
print(graph.adjacency_matrix)
