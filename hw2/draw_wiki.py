#!/usr/bin/env python3

import argparse
import json

import networkx as nx
import matplotlib.pyplot as plt


def main():
    parser = argparse.ArgumentParser(description="Draw Wiki graph")
    parser.add_argument("--json", required=True, help="Path to json file")
    parser.add_argument(
        "--output",
        default="wiki_graph.png",
        help="Output file",
    )
    args = parser.parse_args()

    with open(args.json, "r", encoding="utf-8") as f:
        data = json.load(f)

    G = nx.DiGraph()
    G.add_nodes_from(data["nodes"])
    G.add_edges_from(data["edges"])

    print(f"Graph loaded: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")

    plt.figure(figsize=(20, 20))
    pos = nx.spring_layout(G, k=0.15, iterations=20, seed=42)
    nx.draw_networkx_nodes(G, pos, node_size=50, node_color="skyblue", alpha=0.8)
    nx.draw_networkx_edges(
        G, pos, edge_color="gray", alpha=0.3, arrows=True, arrowsize=10
    )
    if G.number_of_nodes() <= 50:
        nx.draw_networkx_labels(G, pos, font_size=8, font_family="sans-serif")

    plt.title("Wikipedia Graph", fontsize=20)
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(args.output, dpi=150)
    plt.show()
    print(f"Graph image saved to {args.output}")


if __name__ == "__main__":
    main()
