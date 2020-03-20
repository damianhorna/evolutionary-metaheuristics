from aem.tsp_reader import TSPReader
from aem.greedy import Greedy
from aem.plot_util import PlotUtil

instances = [
    "../data/kroA100.tsp",
    "../data/kroB100.tsp"
]

for instance in instances:
    print(f"Working on {instance}")
    graph, coords = TSPReader().read_graph_with_coords(instance)
    print("Adjacency matrix:")
    print(graph.adjacency_matrix)

    greedy = Greedy(graph)

    greedy_result = greedy.run()
    greedy_result.print()
    PlotUtil.plot_best_cycle(greedy_result, coords, instance)
