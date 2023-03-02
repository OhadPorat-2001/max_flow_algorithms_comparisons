import networkx as nx
import csv

import numpy as np

source_index = 0
sink_index = 50


def load_graph(fname='data/contiguous-usa.csv'):
    uniform_capacity = 16
    source_state = "CA"
    uniform_sink = 1
    source_demand = -48  # -num_sinks
    number_state_dictionary = {} # state <-> index dictionary

    G = nx.Graph()
    with open(fname, newline='') as csvfile:
        links = csv.reader(csvfile, delimiter=',')
        for s1, s2 in links:
            G.add_edge(s1, s2)

    for index, state in enumerate(G.nodes()):
        number_state_dictionary[state] = index + 1
        if state != source_state:
            G.node[state]['demand'] = uniform_sink
    G.node[source_state]['demand'] = source_demand
    G = nx.DiGraph(G)
    capacity_matrix = np.zeros([G.number_of_nodes() + 2, G.number_of_nodes() + 2]) # adding 2 in order to include the 'source' and 'sink' nodes

    for (s1, s2) in G.edges():
        G.edge[s1][s2]['capacity'] = uniform_capacity
        capacity_matrix.itemset((number_state_dictionary[s1], number_state_dictionary[s2]), uniform_capacity)

    demand_satisfied = sum([(G.node[i])['demand'] for i in G.nodes()]) == 0
    if not demand_satisfied:
        raise nx.NetworkXUnfeasible('An error is thrown if there is no flow satisfying the demands.')

    # canonical is wih only one source and sink
    G_canonical = G.copy()

    all_nodes = G_canonical.nodes()
    G_canonical.add_node('source')
    G_canonical.add_node('sink')
    for n in all_nodes:
        demand = G_canonical.node[n]['demand']
        if demand < 0:
            G_canonical.add_edge('source', n, capacity=-demand)
            capacity_matrix.itemset((source_index, number_state_dictionary[n]), (source_demand * -1))
        else:
            G_canonical.add_edge(n, 'sink', capacity=demand)
            capacity_matrix.itemset((number_state_dictionary[n], sink_index), (uniform_sink))
    return G_canonical, G, capacity_matrix

