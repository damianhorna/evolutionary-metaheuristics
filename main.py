from aem.utils.tsp_reader import TSPReader
from aem.heuristics.nearest_neighbor import NearestNeighbor
from aem.heuristics.greedy import Greedy
from aem.heuristics.k_regret import KRegret, KRegretFilter
from aem.utils.plot_util import PlotUtil
from pandas import DataFrame

instances = [
    "data/kroA100.tsp",
    "data/kroB100.tsp"
]

results = {}

for instance in instances:
    print(f"Working on {instance}")
    graph = TSPReader().read_graph_with_coords(instance)
    methods = [NearestNeighbor(graph), Greedy(graph), KRegret(graph, k=1), KRegretFilter(graph, k=1)]
    for method in methods:
        result = method.run()
        results[result.method_classname] = [result.average, result.min, result.max]
        result.print()
        PlotUtil.plot_best_cycle(result, graph.coords, instance)

    df = DataFrame.from_dict(results)
    df.to_csv(f"results-{instance[8:-4]}.csv")
    with open(f"result-{instance[8:-4]}.latex", "w") as f:
        f.write(df.to_latex())
