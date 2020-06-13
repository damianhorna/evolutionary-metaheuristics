from aem.heuristics.alter.steepest import Steepest
from aem.heuristics.alter.greedy import Greedy
from aem.heuristics.alter.action_factory import NodeSwapActionFactory,EdgeSwapActionFactory
from aem.utils.tsp_reader import TSPReader
from aem.utils.plot_util import PlotUtil
from pandas import DataFrame

instances = [
    "data/kroA100.tsp",
    "data/kroB100.tsp"
]

results = {}
#
for instance in instances:
    print(f"Working on {instance}")
    graph = TSPReader().read_graph_with_coords(instance)

    methods = [Greedy, Steepest]
    action_factory = [NodeSwapActionFactory(), EdgeSwapActionFactory()]
    for factory in action_factory:

        for method in methods:
            method = method(graph, factory)
            result = method.run(seed=13, number_of_experiments=100)
            results[result.method_classname] = [result.average, result.min, result.max, result.time_average, result.time_min, result.time_max]
            result.print()
            PlotUtil.plot_best_cycle(result, graph.coords, instance)

    df = DataFrame.from_dict(results)
    df.to_csv(f"results-{instance[8:-4]}.csv")
    with open(f"result-{instance[8:-4]}.latex", "w") as f:
        f.write(df.to_latex())
