class EdgeSwap:
    def __init__(self, edge1, edge2):
        self.n1, self.succ_n1 = edge1
        self.n2, self.succ_n2 = edge2


    def __hash__(self):
        return hash(((self.n1, self.succ_n1), (self.n2, self.succ_n2)))

    def __eq__(self, other):
        return self.__class__ == other.__class__ and \
               self.n1 == other.n1 and \
               self.succ_n1 == other.succ_n1 and \
               self.n2 == other.n2 and \
               self.succ_n2 == other.succ_n2

    def __lt__(self, other):
        return True

    def is_applicable(self, cycle):
        if self.n1 in cycle and self.n2 in cycle and self.succ_n1 in cycle and self.succ_n2 in cycle:
            n1_idx = cycle.index(self.n1)
            n1_succ_idx = cycle.index(self.succ_n1)
            if (n1_idx-n1_succ_idx)%len(cycle) not in [0, len(cycle)-1]:
                return False
            n2_idx = cycle.index(self.n2)
            n2_succ_idx = cycle.index(self.succ_n2)

            if (n2_idx - n2_succ_idx) % len(cycle) not in [0, len(cycle) - 1]:
                return False
            # n1_idx = cycle.index(self.n1)
            # if self.succ_n1 != cycle[(n1_idx + 1) % len(cycle)]:
            #     return False
            # n2_idx = cycle.index(self.n2)
            # if self.succ_n2 != cycle[(n2_idx + 1)% len(cycle)]:
            #     return False
            return True
        return False

    def get_delta(self, graph):
        if self.n1 == self.n2 and self.succ_n1 == self.succ_n2:
            return 0
        return graph.adjacency_matrix[self.n1][self.n2] + graph.adjacency_matrix[self.succ_n1][self.succ_n2] - \
               (graph.adjacency_matrix[self.n1][self.succ_n1] + graph.adjacency_matrix[self.n2][self.succ_n2])

    def alter(self, cycle):
        first_pos = cycle.index(self.succ_n1)
        second_pos = cycle.index(self.n2)
        steps = (second_pos-first_pos)%len(cycle)
        for i in range((steps+1)//2):
            first_iter = (first_pos+i)%len(cycle)
            second_iter = (second_pos-i)%len(cycle)
            cycle[first_iter],cycle[second_iter] = cycle[second_iter],cycle[first_iter]
        return cycle


class NodeSwap:
    def __init__(self, inner, outer, inner_neighbors):
        self.inner = inner
        self.outer = outer
        self.inner_neighbors = inner_neighbors

    def __hash__(self):
        return hash((self.inner, self.outer, self.inner_neighbors))

    def __eq__(self, other):
        return self.__class__ == other.__class__ and \
               self.inner == other.inner and \
               self.outer == other.outer and \
               self.inner_neighbors == other.inner_neighbors

    def __lt__(self, other):
        return True

    def is_applicable(self, cycle):
        if self.inner in cycle and self.outer not in cycle:
            inner_idx = cycle.index(self.inner)
            neigh_left = cycle[inner_idx - 1]
            neigh_right = cycle[(inner_idx + 1) % len(cycle)]
            if neigh_left in self.inner_neighbors and neigh_right in self.inner_neighbors:
                return True
        return False

    def get_delta(self, graph):
        previous = self.inner_neighbors[0]
        next_v = self.inner_neighbors[1]

        return graph.adjacency_matrix[previous][self.outer] + graph.adjacency_matrix[self.outer][next_v] - \
               graph.adjacency_matrix[previous][self.inner] - graph.adjacency_matrix[self.inner][next_v]

    def alter(self, cycle):
        inside_pos = cycle.index(self.inner)
        cycle[inside_pos] = self.outer
        return cycle