from pandas import DataFrame

from aem.heuristics.lab3.steepest_edge_swap import SteepestEdgeSwap
from aem.heuristics.lab3.steepest_edge_swap_candidate import SteepestEdgeSwapCandidate
from aem.heuristics.lab3.steepest_edge_swap_lom import SteepestEdgeSwapListOfMoves
from aem.utils.plot_util import PlotUtil
from aem.utils.tsp_reader import TSPReader
import numpy as np
import matplotlib.pyplot as plt

instances = [
    "data/kroA200.tsp",
    "data/kroB200.tsp"
]

results = {}
#
def common_nodes(cycle_a, cycle_b):
    a = set(cycle_a)
    b = set(cycle_b)
    return len(a.intersection(b))

def common_edges(cycle_a, cycle_b):
    a = set()
    a.add((cycle_a[0],cycle_a[-1]))
    a.add((cycle_a[-1], cycle_a[1]))
    for x,y in zip(cycle_a, cycle_a[1:]):
        a.add((x,y))
        a.add((y,x))

    b = set()
    b.add((cycle_b[0], cycle_b[-1]))
    b.add((cycle_b[-1], cycle_b[1]))

    for x, y in zip(cycle_b, cycle_b[1:]):
        b.add((x, y))
        b.add((y, x))

    return len(a.intersection(b))/2

for instance in instances:
    print(f"Working on {instance}")
    graph = TSPReader().read_graph_with_coords(instance)

    method = SteepestEdgeSwapListOfMoves(graph)
    seeds = [np.random.randint(100000) for _ in range(10000)]
    results = []
    for i in range(1000):
        if i%10 == 0:
            print(i)
        results.append(method.run(seed=seeds[i], number_of_experiments=1))
    scores = [_.max for _ in results]
    cycles = [_.best_cycle for _ in results]

    best_poz = np.argmin(scores)
    ce = [common_edges(c, cycles[best_poz]) for c in cycles]
    cn = [common_nodes(c, cycles[best_poz]) for c in cycles]
    ce_all = [np.mean([common_edges(c1, c2) for c2 in cycles]) for c1 in cycles]
    cn_all = [np.mean([common_nodes(c1, c2) for c2 in cycles]) for c1 in cycles]
    plt.scatter(scores, ce)
    plt.title("Common edges best")
    plt.savefig("plots/"+instance.split("/")[1]+"e_best.png")
    plt.close()
    plt.scatter(scores, cn)
    plt.title("Common nodes best")
    plt.savefig("plots/"+instance.split("/")[1]+"n_best.png")
    plt.close()
    plt.scatter(scores, ce_all)
    plt.title("Common edges mean")
    plt.savefig("plots/"+instance.split("/")[1]+"e_all.png")
    plt.close()
    plt.scatter(scores, cn_all)
    plt.title("Common nodes mean")
    plt.savefig("plots/"+instance.split("/")[1]+"n_all.png")
    plt.close()
    print("Edges best", np.corrcoef(scores, ce))
    print("Nodes best", np.corrcoef(scores, cn))
    print("Edges all", np.corrcoef(scores, ce_all))
    print("Nodes all", np.corrcoef(scores, ce_all))






