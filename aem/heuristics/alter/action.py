import numpy as np
import copy


class Action:
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def is_valid(self, cycle, graph):
        pass

    def get_delta(self, cycle, graph):
        pass

    def alter(self, cycle, graph, _copy):
        if _copy:
            return copy.copy(cycle)
        return cycle


class SwapInnerOuter(Action):
    def __init__(self, first, second):
        super().__init__(first, second)

    def __hash__(self):
        return hash((self.first,self.second,self.__class__))

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.first == other.first and self.second == other.second

    def is_valid(self, cycle, graph):
        return (self.first in cycle) ^ (self.second in cycle)

    def get_inner(self, cycle):
        if self.first in cycle:
            return self.first
        return self.second

    def get_outer(self, cycle):
        if self.first not in cycle:
            return self.first
        return self.second

    def get_delta(self, cycle, graph):
        outer = self.get_outer(cycle)
        inner = self.get_inner(cycle)
        inner_pos = cycle.index(inner)

        previous = cycle[inner_pos - 1]
        next = cycle[(inner_pos + 1) % len(cycle)]

        return graph.adjacency_matrix[previous][outer] + graph.adjacency_matrix[outer][next] - graph.adjacency_matrix[previous][inner] - graph.adjacency_matrix[inner][next]

    def alter(self, cycle, graph, _copy):
        cycle = super().alter(cycle, graph, _copy)
        outer = self.get_outer(cycle)
        inner = self.get_inner(cycle)
        inside_pos = cycle.index(inner)

        cycle[inside_pos] = outer
        return cycle

class SwapInner(Action):
    def __init__(self, first, second):
        super().__init__(first, second)

    def is_valid(self, cycle, graph):
        return (self.first in cycle) and (self.second in cycle)


class SwapInnerNodes(SwapInner):
    def __init__(self, first, second):
        super().__init__(first, second)

    def get_delta(self, cycle, graph):
        first_pos = cycle.index(self.first)
        second_pos = cycle.index(self.second)

        #first_pos,second_pos = min(first_pos,second_pos),max(first_pos,second_pos)
        cycle_len = len(cycle)
        if (first_pos+1)%cycle_len == second_pos or (first_pos-1)%cycle_len == second_pos:
            if (first_pos-1)%cycle_len == second_pos:
                (first_pos,first), (second_pos,second) = (second_pos, self.second),(first_pos, self.first)
            else:
                (first_pos, first), (second_pos, second) = (first_pos, self.first),(second_pos, self.second)
            first_previous = cycle[first_pos - 1]
            second_next = cycle[(second_pos + 1) % cycle_len]

            return graph.adjacency_matrix[second][first]+graph.adjacency_matrix[first_previous][second]+\
                graph.adjacency_matrix[first][second_next] - graph.adjacency_matrix[first][second] -\
                graph.adjacency_matrix[first_previous][first]-graph.adjacency_matrix[second][second_next]
        else:
            first_previous = cycle[first_pos - 1]
            first_next = cycle[(first_pos + 1) % cycle_len]

            second_previous = cycle[second_pos - 1]
            second_next = cycle[(second_pos + 1) % cycle_len]

            return graph.adjacency_matrix[second_previous][self.first] + graph.adjacency_matrix[self.first][second_next] + \
               graph.adjacency_matrix[first_previous][self.second] + graph.adjacency_matrix[self.second][first_next] - \
               (graph.adjacency_matrix[first_previous][self.first] + graph.adjacency_matrix[self.first][first_next]) - \
               (graph.adjacency_matrix[second_previous][self.second] + graph.adjacency_matrix[self.second][second_next])

    def alter(self, cycle, graph, _copy):
        cycle = super().alter(cycle, graph, _copy)
        first_pos = cycle.index(self.first)
        second_pos = cycle.index(self.second)
        cycle[first_pos] = self.second
        cycle[second_pos] = self.first

        return cycle


class SwapInnerEdges(SwapInner):
    def __init__(self, first, second):
        super().__init__(first, second)

    def __hash__(self):
        return hash((self.first, self.second, self.__class__))

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.first == other.first and self.second == other.second

    def get_delta(self, cycle, graph):
        first_pos = cycle.index(self.first)
        second_pos = cycle.index(self.second)

        first_previous = cycle[first_pos - 1]
        second_next = cycle[(second_pos + 1) % len(cycle)]
        cycle_len = len(cycle)
        # TODO FIX: hardcoded 49?
        if (second_pos-first_pos)%cycle_len in [1, 99]:
            if (second_pos+1)%cycle_len == first_pos:
                self.first, first_pos, self.second, second_pos = self.second, second_pos, self.first, first_pos
            else:
                self.first, first_pos, self.second, second_pos = self.first, first_pos, self.second, second_pos
            first_previous = cycle[first_pos - 1]
            second_next = cycle[(second_pos + 1) % len(cycle)]

        return graph.adjacency_matrix[first_previous][self.second] + graph.adjacency_matrix[self.first][second_next] - \
               (graph.adjacency_matrix[first_previous][self.first] + graph.adjacency_matrix[self.second][second_next])

    def alter(self, cycle, graph, _copy):
        cycle = super().alter(cycle, graph, _copy)

        first_pos = cycle.index(self.first)
        second_pos = cycle.index(self.second)
        steps = (second_pos-first_pos)%len(cycle)
        for i in range((steps+1)//2):
            first_iter = (first_pos+i)%len(cycle)
            second_iter = (second_pos-i)%len(cycle)
            cycle[first_iter],cycle[second_iter] = cycle[second_iter],cycle[first_iter]
        return cycle
