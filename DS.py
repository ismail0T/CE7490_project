import networkx as nx
import numpy as np
from collections import defaultdict

import Utils


def spar(G_orig, nb_partition_max=2, k_min=2):
    nb_replicated_nodes = 0
    G_new = nx.DiGraph()

    # arr = np.array([1, 2, 3, 4])
    # np.random.shuffle(arr)
    # new_arr = np.array_split(arr, nb_partition_max)

    for key in list(G_orig.nodes):
        # print(key, G_orig.nodes[key])
        # 1. Create node
        id_partition = get_low_replica(G_new, nb_partition_max)
        add_node_spar(G_new, key, label=G_orig.nodes[key]["label"], write=G_orig.nodes[key]["write"], copy_of=-1, server=id_partition)

        # 2. Create K replica
        partions_to_replicate_on = list(range(nb_partition_max))
        partions_to_replicate_on.remove(id_partition)
        np.random.shuffle(partions_to_replicate_on)
        for i in range(min(k_min, len(partions_to_replicate_on))):
            nb_replicated_nodes += 1
            id_new_node = G_orig.order() + nb_replicated_nodes
            add_node_spar(G_new, id_new_node, label=G_orig.nodes[key]["label"], write=0, copy_of=key, server=partions_to_replicate_on[i])

    # 3. Add edges
    for (u, v, wt) in G_orig.edges.data('weight'):
        add_edge_spar(G_new, u, v, wt)

    # 4. remove unnecessarily replica
    # for key in list(G_new.nodes):

    for key in list(G_new.nodes):
        print(key, G_new.nodes[key])

    return G_new


def get_low_replica(G, nb_partition_max):
    counts = np.zeros(nb_partition_max)
    for key in list(G.nodes):
        if G.nodes[key]["server"] != -1:  # only master replicas
            counts[G.nodes[key]["server"]] += 1

    return np.argmin(counts)


def add_node_spar(G, id_new, label, write, copy_of, server):
    G.add_node(id_new, label=label, copy_of=copy_of, write=write, server=server)

    return id_new


def add_edge_spar(G, u, v, weight):
    G.add_weighted_edges_from([(u, v, weight)])
    # check if: bother masters are on the same partition OR u has a replica on v's partition OR v has a replica on u's partition
    if G.nodes[u]["server"] != G.nodes[v]["server"]:
        if not Utils.has_local_replica(G, u, v) and not Utils.has_local_replica(G, v, u):
            #  Choose best configuration among the 3
            #  config 1
            if not Utils.has_local_replica(G, u, v):
                #  create replica for u on v's partition
                id_new = G.order() + 1
                add_node_spar(G, id_new, label=G.nodes[u]["label"], write=0, copy_of=u, server=G.nodes[v]["server"])

            if not Utils.has_local_replica(G, v, u):
                id_new = G.order() + 1
                add_node_spar(G, id_new, label=G.nodes[v]["label"], write=0, copy_of=v, server=G.nodes[u]["server"])

            pass
        # Do nothing beyond edge addition
        # G.add_weighted_edges_from([(u, v, weight)])

        else:  # do noting
            pass





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
                new_ID = Utils.add_node(G, label=G.nodes[key]["label"], copy_of=key, server=server_id)
                G.add_weighted_edges_from([(key, new_ID, G.nodes[key]["write"])])

    print("NB nodes: ", G.order())


