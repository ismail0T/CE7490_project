import networkx as nx
import numpy as np
from collections import defaultdict

import Utils

np.random.seed(1)


def random_partition(G, nb_partition=2):
    for key in G.nodes:
        server_id = np.random.randint(0, nb_partition)
        G.nodes[key]["server"] = server_id

    return G


def selective_replicate(G, nb_partition=2):
    sum_in = defaultdict(lambda: np.zeros(nb_partition))
    for (u, v, wt) in G.edges.data('weight'):
        if G.nodes[u]['server'] != G.nodes[v]['server']:
            sum_in[v][G.nodes[u]['server']] += wt
    print(len(sum_in))
    # sum_in ==>  3: array([90.,  0.]) ==> server 0 (first index in array) read 90 from user 3 (C) which is on different server
    # action to do: replicate user 3 (C) on server 0

    for none, key in enumerate(sum_in):
        # print(key, sum_in[key], G.nodes[key]["write"])
        for server_id, read_weight in enumerate(sum_in[key]):
            # print(server_id, G.nodes[key]["write"], read_weight)
            if G.nodes[key]["write"] < read_weight:  # Do replication
                new_ID = Utils.add_node_std(G, copy_of=key, server=server_id)
                G.add_weighted_edges_from([(key, new_ID, G.nodes[key]["write"])])

    # print("NB nodes: ", Utils.get_largest_ID(G))
    return G


pathhack = "/home/ismail/Dev/Ego_Facebook"
G_0 = nx.read_edgelist("%s/facebook_combined.txt" % (pathhack,), create_using=nx.Graph(), nodetype=int).to_directed()
G = Utils.add_weights(G_0)
nb_master_replica = G.order()

nb_partition_max = 2
G = random_partition(G, nb_partition=nb_partition_max)
G = selective_replicate(G, nb_partition=nb_partition_max)
nb_slave_replica = G.order() - nb_master_replica


G = Utils.to_undirected(G)
G_dict = Utils.nx_to_dict(G)
# cost_spar_traffic = spar_inter_server_traffic(G_dict, G_servers, G_replica)

print("nb_slave_replica:", nb_slave_replica)





