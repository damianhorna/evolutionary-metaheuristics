from pandas import DataFrame

from aem.heuristics.lab3.steepest_edge_swap import SteepestEdgeSwap
from aem.utils.plot_util import PlotUtil
from aem.utils.tsp_reader import TSPReader

instances = [
    "data/kroA100.tsp",
    "data/kroB100.tsp"
]

results = {}
#
for instance in instances:
    print(f"Working on {instance}")
    graph = TSPReader().read_graph_with_coords(instance)

    methods = [SteepestEdgeSwap(graph)]
    for method in methods:
        result = method.run(seed=13, number_of_experiments=1)
        results[result.method_classname] = [result.average, result.min, result.max, result.time_average,
                                            result.time_min, result.time_max]
        result.print()
        PlotUtil.plot_best_cycle(result, graph.coords, instance)

    df = DataFrame.from_dict(results)
    df.to_csv(f"results-{instance[8:-4]}.csv")
    with open(f"result-{instance[8:-4]}.latex", "w") as f:
        f.write(df.to_latex())
