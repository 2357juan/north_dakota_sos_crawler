import random
from itertools import combinations
import matplotlib.pyplot as plt
import networkx as nx
import jsonlines


def create_graph(path):
    nodes = []
    edges = []
    with jsonlines.open(path) as reader:
        for obj in reader:
            names = obj["entities"]
            nodes.extend(names)
            if len(names) > 1:
                for c in combinations(names, 2):
                    edges.append((c[0], c[1]))
    G = nx.Graph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    print(G)
    print(nx.number_connected_components(G), "connected components")
    return G

def plot_graph(G,filename="names.png"):
    plt.figure(1, figsize=(8, 8))
    # layout graphs with positions using graphviz neato
    pos = nx.nx_agraph.graphviz_layout(G, prog="neato")
    # color nodes the same in each connected subgraph
    C = (G.subgraph(c) for c in nx.connected_components(G))
    for g in C:
        c = [random.random()] * nx.number_of_nodes(g)  # random color...
        nx.draw(
            g,
            pos,
            node_size=40,
            node_color=c,
            vmin=0.0,
            vmax=1.0,
            with_labels=True,
            font_size=8)
    plt.savefig(filename)

if __name__ == "__main__":
    random.seed(32687)
    G = create_graph("test_triple.jsonl")
    plot_graph(G,"names.png")
