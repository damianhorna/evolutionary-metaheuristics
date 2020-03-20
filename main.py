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
    methods = [Greedy(graph)]
    for method in methods:
        result = method.run()
        result.print()
        PlotUtil.plot_best_cycle(result, coords, instance)
