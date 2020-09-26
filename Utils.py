import networkx as nx
import numpy as np
from collections import defaultdict



def get_nb_replicas(G, key):
    return len(list(x for x in G.nodes if G.nodes[x]["copy_of"] == key))


def get_largest_ID(G):
    return max(x for x in G.nodes)


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


def add_node_std(G, label, copy_of, server):
    id_new = G.order() + 1
    G.add_node(id_new, label=label, copy_of=copy_of, write=0, server=server)

    return id_new


def choose_best_config(cost_config_1, cost_config_2, cost_config_3, ratio_load_config1, ratio_load_config2, ratio_load_config3):
    best_cost = min(cost_config_1, cost_config_2, cost_config_3)
    second_best_cost = sorted((cost_config_1, cost_config_2, cost_config_3))[1]

    if cost_config_1 == best_cost:
        return 0
    else:
        best_load_ratio = min(ratio_load_config1, ratio_load_config2, ratio_load_config3)
        if cost_config_3 == best_cost:
            if ratio_load_config3 == best_load_ratio:
                return 2
            elif second_best_cost == cost_config_2 and ratio_load_config2 == best_load_ratio:
                return 1
            else:
                return 0
        else:
            if cost_config_2 == best_cost:
                if ratio_load_config2 == best_load_ratio:
                    return 1
                elif second_best_cost == cost_config_3 and ratio_load_config3 == best_load_ratio:
                    return 2
                else:
                    return 0

