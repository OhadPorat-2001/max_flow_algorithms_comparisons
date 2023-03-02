# Adapted from https://www.codingninjas.com/codestudio/library/dinics-algorithm-for-maximum-flow

class Edge:
    def __init__(self, v, flow, C, rev):
        self.v = v
        self.flow = flow
        self.C = C
        self.rev = rev


class Graph:
    def __init__(self, G):
        self.V = G.number_of_nodes()
        self.number_state_dictionary = {}
        for index, value in enumerate(G.node):
            self.number_state_dictionary[value] = index
        # self.capacity_matrix =
        self.adj = [[] for i in range(self.V)]
        self.level = [0 for i in range(self.V)]
        # dictionary for indexing the states

    # add edge to the graph
    def addEdge(self, u, v, C):

        # Forward edge : 0 flow and C capacity
        a = Edge(v, 0, C, len(self.adj[self.number_state_dictionary[v]]))

        # Back edge : 0 flow and 0 capacity
        b = Edge(u, 0, 0, len(self.adj[self.number_state_dictionary[u]]))
        self.adj[self.number_state_dictionary[u]].append(a)
        self.adj[self.number_state_dictionary[v]].append(b)

    # Finds if more flow can be sent from source to target
    # Also assigns levels to nodes
    def BFS(self, source, target):
        for i in range(self.V):
            self.level[i] = -1

        # Level of source vertex
        self.level[source] = 0

        # Create a queue, enqueue source vertex
        # and mark source vertex as visited here
        # level[] array works as visited array also
        q = []
        q.append(source)
        while q:
            u = q.pop(0)
            for i in range(len(self.adj[u])):
                e = self.adj[u][i]
                try:
                    if self.level[self.number_state_dictionary[e.v]] < 0 and e.flow < e.C["capacity"]:
                        # Level of current vertex is
                        # level of parent + 1
                        self.level[self.number_state_dictionary[e.v]] = self.level[u] + 1
                        q.append(self.number_state_dictionary[e.v])
                except:
                    if self.level[self.number_state_dictionary[e.v]] < 0 and e.flow < e.C:
                        # Level of current vertex is
                        # level of parent + 1
                        self.level[self.number_state_dictionary[e.v]] = self.level[u] + 1
                        q.append(self.number_state_dictionary[e.v])

        # If we can not reach to the sink we
        # return False else True
        return False if self.level[target] < 0 else True

    def sendFlow(self, u, flow, sink, start):
        """
        A DFS based function to send flow after BFS has figured out that there is a possible flow and constructed levels.
        This functions called multiple times for a single call of BFS.
        Args:
            u:Current vertex
            flow: Current flow send by parent function call
            t: Sink
            start: To keep track of next edge to be explored start[i] stores count of edges explored from i

        Returns:

        """
        # Sink reached
        if u == sink:
            return flow

        # Traverse all adjacent edges one -by -one
        while start[u] < len(self.adj[u]):

            # Pick next edge from adjacency list of u
            e = self.adj[u][start[u]]
            try:
                if self.level[self.number_state_dictionary[e.v]] == self.level[u] + 1 and e.flow < e.C["capacity"]:

                    # find minimum flow from u to t
                    curr_flow = min(flow, e.C["capacity"] - e.flow)
                    temp_flow = self.sendFlow(self.number_state_dictionary[e.v], curr_flow, sink, start)

                    # flow is greater than zero
                    if temp_flow and temp_flow > 0:
                        # add flow to current edge
                        e.flow += temp_flow

                        # subtract flow from reverse edge
                        # of current edge
                        self.adj[self.number_state_dictionary[e.v]][e.rev].flow -= temp_flow
                        return temp_flow
            except:
                if self.level[self.number_state_dictionary[e.v]] == self.level[u] + 1 and e.flow < e.C:

                    # find minimum flow from u to t
                    curr_flow = min(flow, e.C - e.flow)
                    temp_flow = self.sendFlow(self.number_state_dictionary[e.v], curr_flow, sink, start)

                    # flow is greater than zero
                    if temp_flow and temp_flow > 0:
                        # add flow to current edge
                        e.flow += temp_flow

                        # subtract flow from reverse edge
                        # of current edge
                        self.adj[self.number_state_dictionary[e.v]][e.rev].flow -= temp_flow
                        return temp_flow
            start[u] += 1

    def DinicMaxflow(self, source, target):
        """
        Get source and target indexes and Returns maximum flow in graph
        Args:
            source: Source index
            target: Target index
        Returns: Maximum Flow

        """
        source_number = self.number_state_dictionary[source]
        target_number = self.number_state_dictionary[target]
        # Corner case
        if source_number == target_number:
            return -1

        # Initialize result
        total = 0

        # Augument the flow while there is path
        # from source to sink
        while self.BFS(source_number, target_number):

            # store how many edges are visited
            # from V { 0 to V }
            start = [0 for i in range(self.V + 1)]
            while True:
                flow = self.sendFlow(source_number, float('inf'), target_number, start)
                if not flow:
                    break
                # Add path flow to overall flow
                total += flow
        # return maximum flow
        return total


def canonical_graph_2_dinic_format_graph(G_canonical):
    g = Graph(G_canonical)
    # add edges
    for u, v in G_canonical.edges():
        capacity = G_canonical.edge[u][v]
        g.addEdge(u, v, capacity)
    return g
