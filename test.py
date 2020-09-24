import random

import facebook, twitter
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
import sys

# # load the network
# my_graph = facebook.load_network()
#
# print(my_graph.order())  # number of nodes
# print(my_graph.size())   # number of edges
#
# # Look at a node's features
# print("feature: ", my_graph.nodes[0]['features'])
#
# # 0: feature not present for this user
# # 1: user does not have this feature
# # 2: user does have this feature
#
# # look at the features of the whole network
# print("matrix", facebook.feature_matrix())

import nxmetis



# network = nx.DiGraph()
# network.add_node(1, write="20")
# network.add_node(2, write="40")
# network.add_node(3, write="25")
# network.add_node(4, write="30")
# network.add_node(5, write="60")
# network.add_node(6, write="30")
# network.add_node(7, write="40")
#
# print("NB nodes: ", network.order())
#
# network.add_weighted_edges_from([(1, 2, 20), (2, 1, 25)])
# network.add_weighted_edges_from([(1, 3, 25), (3, 1, 40)])
# network.add_weighted_edges_from([(1, 4, 20), (4, 1, 45)])
# network.add_weighted_edges_from([(1, 6, 30), (6, 1, 50)])
# network.add_weighted_edges_from([(4, 3, 50), (3, 4, 20)])
# network.add_weighted_edges_from([(6, 2, 30), (2, 6, 25)])
# network.add_weighted_edges_from([(2, 3, 30), (3, 2, 10)])
# network.add_weighted_edges_from([(2, 7, 40), (7, 2, 20)])
# network.add_weighted_edges_from([(3, 5, 30), (5, 3, 45)])



network = nx.DiGraph()
# attrs = {1: {"label": "A", "write": 10, "server": 1},
#          2: {"label": "B", "write": 20, "server": 1},
#          3: {"label": "C", "write": 30, "server": 1},
#          4: {"label": "D", "write": 80, "server": 1}}

# nx.set_node_attributes(network, attrs)

network.add_node(1, label="A", copy_of=-1, write=10, server=0)
network.add_node(2, label="B", copy_of=-1, write=20, server=0)
network.add_node(3, label="C", copy_of=-1, write=30, server=0)
network.add_node(4, label="D", copy_of=-1, write=80, server=0)

# print("NB nodes: ", network.order())
#
# sys.exit()

network.add_weighted_edges_from([(1, 3, 90), (3, 1, 25)])
network.add_weighted_edges_from([(1, 4, 100), (4, 1, 20)])
network.add_weighted_edges_from([(2, 4, 5), (4, 2, 15)])
network.add_weighted_edges_from([(3, 4, 10), (4, 3, 20)])

# print(dict(network.out_degree(weight='weight')))

def add_node(G, label, copy_of, server):
    id_new = G.order() + 1
    G.add_node(id_new, label=label, copy_of=copy_of, write=0, server=server)

    return id_new


def random_partition_old(G, nb_partition=2):
    arr = np.array([1, 2, 3, 4])
    np.random.shuffle(arr)
    new_arr = np.array_split(arr, nb_partition)
    G_list = {}

    for i, part_index in enumerate(new_arr, 0):
        new_G = nx.DiGraph()
        for node_id in part_index:
            new_G.add_node(node_id, write=G.nodes[node_id]['write'])
        G_list[i] = new_G

    print(new_arr)
    return G_list


def random_partition(G, nb_partition=2):
    arr = np.array([1, 2, 3, 4])
    # np.random.shuffle(arr)
    new_arr = np.array_split(arr, nb_partition)

    for i, part_index in enumerate(new_arr, 0):
        for node_id in part_index:
            G.nodes[node_id]['server'] = i

    # print(new_arr)
    # print(G.nodes[1])
    # print(G.nodes[2])
    # print(G.nodes[3])
    # print(G.nodes[4])


def selective_replicate(G, nb_partition=2):
    sum_in = defaultdict(lambda: np.zeros(nb_partition))

    for (u, v, wt) in G.edges.data('weight'):
        # print(u, v)
        if G.nodes[u]['server'] != G.nodes[v]['server']:
            sum_in[v][G.nodes[u]['server']] += wt
        # print(u, v, wt)
        # print(G.nodes[u]['server'])
    print(sum_in)
    # sum_in ==>  3: array([90.,  0.]) ==> server 0 (first index in array) read 90 from user 3 (C) which is on different server
    # action to do: replicate user 3 (C) on server 0

    for none, key in enumerate(sum_in):
        # print(key, sum_in[key], G.nodes[key]["write"])
        for server_id, read_weight in enumerate(sum_in[key]):
            # print(server_id, read_weight)
            if G.nodes[key]["write"] < read_weight:  # Do replication
                new_ID = add_node(G, label=G.nodes[key]["label"], copy_of=key, server=server_id)
                G.add_weighted_edges_from([(key, new_ID, G.nodes[key]["write"])])

    print("NB nodes: ", G.order())
        # if sum_in[key] > G.nodes[key]["write"]:
        #     print(key, sum_in[key], G.nodes[key]["write"])

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

# print(network.nodes[3]['write'])

random_partition(network)
selective_replicate(network)
total_read(network)
total_write(network)
# for n, nbrs in network.adj.items():
#    for nbr, eattr in nbrs.items():
#        wt = eattr['weight']
#        print("n", nbr, "\t",  wt)

# print(network[3][1])


# for (u, v, wt) in network.edges.data('weight'):
#         print(u, v, wt)


