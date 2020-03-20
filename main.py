from aem.utils.tsp_reader import TSPReader
from aem.heuristics.nearest_neighbor import NearestNeighbor
from aem.heuristics.greedy import Greedy
from aem.heuristics.k_regret import KRegret
from aem.utils.plot_util import PlotUtil

instances = [
    "../data/kroA100.tsp",
    "../data/kroB100.tsp"
]

for instance in instances:
    print(f"Working on {instance}")
    graph, coords = TSPReader().read_graph_with_coords(instance)
    methods = [NearestNeighbor(graph), Greedy(graph)]  # KRegret(graph)
    for method in methods:
        result = method.run()
        result.print()
        PlotUtil.plot_best_cycle(result, coords, instance)
