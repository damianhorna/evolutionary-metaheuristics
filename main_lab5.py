from pandas import DataFrame

from aem.heuristics.lab5.hybrid_evolutionary import HybridEvolutionary
from aem.utils.plot_util import PlotUtil
from aem.utils.tsp_reader import TSPReader

instances = [
    "data/kroA200.tsp",
    "data/kroB200.tsp"
]

results = {}
#
for instance in instances:
    print(f"Working on {instance}")
    graph = TSPReader().read_graph_with_coords(instance)

    methods = [HybridEvolutionary(graph)]
    for method in methods:
        result = method.run(seed=13, time_limit=35, population_size=20, number_of_experiments=1)
        results[result.method_classname] = [result.average, result.min, result.max, result.time_average,
                                            result.time_min, result.time_max]
        result.print()
        PlotUtil.plot_best_cycle(result, graph.coords, instance)

    df = DataFrame.from_dict(results)
    df.to_csv(f"results-{instance[8:-4]}.csv")
    with open(f"result-{instance[8:-4]}.latex", "w") as f:
        f.write(df.to_latex())
