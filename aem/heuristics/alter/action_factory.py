import itertools
import numpy as np

from aem.heuristics.alter.action import *


def pair_permutations(n):
    perm = list(itertools.permutations(range(n), 2))
    np.random.shuffle(perm)

    return perm


class ActionFactory:

    def generate(self, cycle, graph) -> Action:
        pass


class NodeSwapActionFactory(ActionFactory):

    def generate(self, cycle, graph) -> Action:
        for (a, b) in pair_permutations(graph.no_of_vertices()):
            if a < b or True:
                action_inner = SwapInnerNodes(a, b)
                action_outer = SwapInnerOuter(a, b)
                if action_inner.is_valid(cycle, graph):
                    yield action_inner
                elif action_outer.is_valid(cycle, graph):
                    yield action_outer


class EdgeSwapActionFactory(ActionFactory):

    def generate(self, cycle, graph) -> Action:
        for (a, b) in pair_permutations(graph.no_of_vertices()):
            action_inner = SwapInnerEdges(a, b)
            action_outer = SwapInnerOuter(a, b)
            if action_inner.is_valid(cycle, graph) and a!=b:
                yield action_inner
            elif a<b and action_outer.is_valid(cycle, graph):
                yield action_outer
