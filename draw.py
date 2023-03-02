import networkx as nx
import pandas as pd
from matplotlib import pyplot as plt


def draw_graph(G):
    nx.draw(G, pos=get_all_state_positions(), with_labels=True)
    plt.show()


def get_all_state_positions():
    pos_lat_lon = pd.read_csv("data/statelatlong.csv")
    pos = {state: [lon, lat] for i, (state, lat, lon, city) in pos_lat_lon.iterrows()}
    return pos
