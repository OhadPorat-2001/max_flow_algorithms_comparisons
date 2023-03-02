def bfs(graph, source, sink):
    """
    :param graph: networkx.Digraph
    :param source: str, key for vertex in graph
    :param sink: str, key for vertex in graph
    :return: One of the shortest paths from source to sink
    """
    queue = [(source, [source])]
    visited = [source]
    while queue:
        u, path = queue.pop(0)
        relevant_neighbors = [v for v in graph[u].keys() if v not in path and v not in visited]
        for v in relevant_neighbors:
            visited.append(v)
            if v == sink:
                return path + [v]
            queue.append((v, path + [v]))


def get_residual_graph(graph, path):
    """
    finds the bottleneck induced by the added flow and returns the residual graph
    :param graph: networkx.Digraph
    :param path: list of edges from source to sink
    :return: the residual graph
    """
    bottleneck = min([graph[u][v]['capacity'] for u, v in path])
    for (u, v) in path:
        # reducing capacity and removing if capacity full
        graph.edge[u][v]['capacity'] -= bottleneck
        if graph.edge[u][v]['capacity'] == 0:
            graph.remove_edge(u, v)

        # since we've increased flow u->v, we can decrease it via increasing v->u flow
        if not graph.has_edge(v, u):
            graph.add_edge(v, u)
            graph.edge[v][u]['capacity'] = 0
        graph.edge[v][u]['capacity'] += bottleneck
    return graph


def edmond_karp(graph, source, sink):
    """ Run Edamond Karp
    :param graph: networkx.Digraph
    :param source: str, key for vertex in graph
    :param sink: str, key for vertex in graph
    :return: the residual graph after running EK
    """
    path = bfs(graph, source, sink)
    while path:
        path_used = list(zip(path[:-1], path[1:]))  # so [a, b, c] becomes [(a, b), (b, c), (c, d)]
        graph = get_residual_graph(graph, path_used)
        path = bfs(graph, source, sink)  # augmenting path

    # graph.adj["sink"] contains edges from sink, which for the last residual graph includes all vertices that gave flow
    flow_amount = sum(graph.adj["sink"][item]["capacity"] for item in graph.adj["sink"])
    return graph, flow_amount
