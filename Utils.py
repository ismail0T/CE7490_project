import networkx as nx
import numpy as np
from collections import defaultdict




def to_undirected(G):
    UG = G.to_undirected()
    for node in G:
        for ngbr in nx.neighbors(G, node):
            if node in nx.neighbors(G, ngbr):
                UG.edges[node, ngbr]['weight'] = (
                        G.edges[node, ngbr]['weight'] + G.edges[ngbr, node]['weight']
                )
    return UG


def has_local_replica(G, u, v):
    server_u = G.nodes[u]['server']
    server_v = G.nodes[v]['server']

    if server_u == server_v:
        return True
    for key in list(G.nodes):
        if G.nodes[key]["copy_of"] == v and G.nodes[key]["server"] == server_u:
            return True
    return False


def total_read(G):
    total=0
    for (u, v, wt) in G.edges.data('weight'):
        if not has_local_replica(G, u, v) and u != G.nodes[v]['copy_of']:
            total += wt
    print("total_read", total)
    return total


def total_write(G):
    total=0
    for (u, v, wt) in G.edges.data('weight'):
        if u == G.nodes[v]['copy_of']:
            total += wt
    print("total_write", total)
    return total


def add_node(G, label, copy_of, server):
    id_new = G.order() + 1
    G.add_node(id_new, label=label, copy_of=copy_of, write=0, server=server)

    return id_new



