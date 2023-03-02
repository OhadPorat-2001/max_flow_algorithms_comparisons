from draw import draw_graph
from graph import load_graph
from utils import PrintTime
from edmondKarp.edmond_karp import edmond_karp
from dinic.DinicGraph import canonical_graph_2_dinic_format_graph
from pushRelabel.pushRelabelGraph import Graph as PR_Graph


def main():
    # loading the graph
    G_canonical, G, capacity_matrix = load_graph()
    G_dinic = canonical_graph_2_dinic_format_graph(G_canonical.copy())
    G_push_relabel = PR_Graph(capacity_matrix)

    with PrintTime("Edmond Karp"):
        flow, ek_flow = edmond_karp(G_canonical, "source", "sink")

    with PrintTime("Dinic's"):
        dinic_flow = G_dinic.DinicMaxflow("source", "sink")

    with PrintTime("Push Relabel"):
        push_relabel_flow = G_push_relabel.push_relable(origin=0, goal=50)

    print("flow found")
    print(f"Edmond Karp: {ek_flow}")
    print(f"Dinic's: {dinic_flow}")
    print(f"Push Relabel: {push_relabel_flow}")

    print("graph:")
    draw_graph(G)


if __name__ == '__main__':
    main()
