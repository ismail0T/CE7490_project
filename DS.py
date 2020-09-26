import networkx as nx
import numpy as np
from collections import defaultdict

import Utils


def random_partition(G, nb_partition=2):
    arr = np.array([1, 2, 3, 4])
    # np.random.shuffle(arr)
    new_arr = np.array_split(arr, nb_partition)

    for i, part_index in enumerate(new_arr, 0):
        for node_id in part_index:
            G.nodes[node_id]['server'] = i


def selective_replicate(G, nb_partition=2):
    sum_in = defaultdict(lambda: np.zeros(nb_partition))
    for (u, v, wt) in G.edges.data('weight'):
        if G.nodes[u]['server'] != G.nodes[v]['server']:
            sum_in[v][G.nodes[u]['server']] += wt
    print(sum_in)
    # sum_in ==>  3: array([90.,  0.]) ==> server 0 (first index in array) read 90 from user 3 (C) which is on different server
    # action to do: replicate user 3 (C) on server 0

    for none, key in enumerate(sum_in):
        # print(key, sum_in[key], G.nodes[key]["write"])
        for server_id, read_weight in enumerate(sum_in[key]):
            # print(server_id, read_weight)
            if G.nodes[key]["write"] < read_weight:  # Do replication
                new_ID = Utils.add_node_std(G, label=G.nodes[key]["label"], copy_of=key, server=server_id)
                G.add_weighted_edges_from([(key, new_ID, G.nodes[key]["write"])])

    print("NB nodes: ", Utils.get_largest_ID(G))
