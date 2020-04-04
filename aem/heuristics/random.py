from aem.heuristics.heuristic import Heuristic
from typing import List
import numpy as np


class Random(Heuristic):
    def __init__(self, graph):
        super().__init__(graph)

    def build_cycle(self, start_vertex=0) -> list:
        cycle = [start_vertex]
        while len(cycle) < self.graph.no_of_vertices() // 2:
            new_vertex = np.random.randint(self.graph.no_of_vertices())
            while new_vertex in cycle:
                new_vertex = np.random.randint(self.graph.no_of_vertices())
            cycle.append(new_vertex)
        return cycle
