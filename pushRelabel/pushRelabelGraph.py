# Adapted from https://github.com/karnigili/MaxFlow

import numpy as np


class Graph:
    '''
    A flow graph object for push relable algorithm
    Calculates max flow using different methods
    '''

    def __init__(self, data=None):
        n, m = np.shape(data)
        assert n == m, "data must be square"

        # edge properties
        self.capacity = data
        self.flow = np.zeros((n, n), dtype=np.int)

        self.size = n

        # vertices properties
        self.vertices = np.array([i for i in range(self.size)])
        self.excess = [0] * self.size
        self.distance = [0] * self.size
        self.level = [-1] * self.size
        self.seen = [0] * self.size
        assert sum(self.capacity[-1]) == 0 and sum(self.capacity[:, 0]) \
               == 0, "source must be first, sink must be last"
        self.source = 0
        self.sink = 51

    def push_relable(self, origin=None, goal=None):

        '''
        objective: unlike the previous two, this algorithm optimizes
        based on local decisions. Front to back, this algorithm iterates
        on the list of vertexes in the graph repeatedly selecting an
        overflowing vertex and discharge it: using push and relabel until
        the vertex deactivates.
        ** performance exceeds Dinic for dense graphs.
        parameters :
            self - object
            origin - int, an index for the origin, the default is the source
            goal - int, an index for the goal, the default is sink

        output
            graph max flow
        complexity
            O(V^3)
            Each vertex can be relabeled 2V times; discahrging pushes
            (uses the full residual capacity) And a discahrging pushes.
            There is a max of V discahrging pushes
            can be done on any edge. Hence max of 2V discahrging pushes.
            Pushes for an edge and its linked edge (numbered E) are O(VE).
            There are O(V^2) relabling operation called on V vertexes - O(V^3).
            Adding these O(V^3+VE) = O(V^3).
            (Since V<=E<=V^2 this conclusion is viable)
        '''
        # initiates vars
        n = self.size

        goal = goal or self.sink
        origin = origin or self.source

        # inter_nodes, not sink or source, are viable for push
        inter_nodes = [i for i in range(n) if i != origin and i != goal]

        # pushes max capacity from source
        self.distance[origin] = n
        self.excess[origin] = float('inf')

        # resolves excess on source neighbors
        for v in range(n):
            self._push(origin, v)

        potential_vertex = 0

        while potential_vertex < len(inter_nodes):
            u = inter_nodes[potential_vertex]

            # resolve ecxess flow from u.
            pred_distance = self.distance[u]
            self._discharge(u)

            # checks whether te vertex was relabled
            if self.distance[u] > pred_distance:

                # move to front selection rule
                # inserts the vertex to the front and set the search back to 0
                inter_nodes.insert(0, inter_nodes.pop(potential_vertex))
                potential_vertex = 0

            else:
                potential_vertex += 1

        return sum(self.flow[origin])

    def _push(self, u, v):
        '''
        objective: pushes the excess to a viable next vertex
        parameters :
            self - object
            v - int, index of an overflowing vertex
            u - int, index of a potential neighbor to move excess to

        output
            none
        '''
        # caculates the viable transferable flow, residual or the full excess
        delta_flow = min(self.excess[u], (self.capacity[(u, v)] - self.flow[(u, v)]))

        # modify the flow and excess in both vertexes, and edges,
        # based on the delta in flow
        self.flow[(u, v)] += delta_flow
        self.flow[(v, u)] -= delta_flow

        self.excess[u] -= delta_flow
        self.excess[v] += delta_flow

    def _relabel(self, u):
        '''
        objective : modifies a vertex distnce to enable push
            (to create d(u) < d(v))
        parameters :
            self - object
            u - int, index of the vertex to change the distance

        output
            none
        '''
        # initialize
        min_distance = float('inf')

        # finds the min distance possible and changes the given
        # vertex distance by this number
        for v in range(self.size):
            if (self.capacity[(u, v)] - self.flow[(u, v)]) > 0:
                min_distance = min(min_distance, self.distance[v])
                self.distance[u] = min_distance + 1

    def _discharge(self, u):
        '''
        objective: iterating on an active vertex with an excess until resolved
        parameters :
            self - object
            u - int, index of a vertex with an excess flow,
                keep pushing flow until it disactivates (= excess flow = 0)

        output
            none
        '''

        while self.excess[u] > 0:

            # iterating through all possibel vertexes
            if self.seen[u] < self.size:

                v = self.seen[u]

                # verifies the conditions to push: positive residual on the edge
                # and lower distance on the vertex the flow will be pushed to
                # pushes if viable or moves to the next vertex
                if (self.capacity[(u, v)] - self.flow[(u, v)] > 0) \
                        and (self.distance[u] > self.distance[v]):

                    self._push(u, v)

                else:
                    self.seen[u] += 1

            # if a push is not possible, relabel
            else:
                self._relabel(u)
                self.seen[u] = 0
