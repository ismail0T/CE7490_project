import random
import sys
import Utils
import networkx as nx
import numpy as np
from collections import defaultdict


np.random.seed(1)

pathhack = "/home/ismail/Dev/Ego_Facebook"
G_0 = nx.read_edgelist("%s/facebook_combined.txt" % (pathhack,), create_using=nx.Graph(), nodetype=int).to_directed()
G_0 = Utils.add_weights(G_0)
G_0 = Utils.to_undirected(G_0)


G_dict = Utils.nx_to_dict(G_0)


def random_partition(G_dict, nb_partition=2):
    servers = defaultdict(lambda: -1)
    for u in G_dict:
        server_id = np.random.randint(0, nb_partition)
        servers[u] = server_id
    return servers


def selective_replica(G_dict, G_servers, nb_partition=2):
    sum_in = defaultdict(lambda: np.zeros(nb_partition))
    G_replica_0 = defaultdict(list)
    for u in G_dict:
        for v in G_dict[u]["neighbors"]:
            if G_servers[u] != G_servers[v]:
                sum_in[v][G_servers[u]] += G_dict[u]["neighbors"][v]
    # print(len(sum_in))
    for none, key in enumerate(sum_in):
        for server_id, read_weight in enumerate(sum_in[key]):
            if G_dict[key]["write"] < read_weight:  # Do replication
                G_replica_0[key].append(server_id)

    return G_replica_0


for nb_partition_max in [4, 8, 16, 32, 64, 128, 256]:
    G_servers = random_partition(G_dict, nb_partition=nb_partition_max)
    G_replica = selective_replica(G_dict, G_servers, nb_partition=nb_partition_max)

    cost_RPSR_replica = Utils.spar_inter_server_cost(G_replica)
    cost_RPSR_traffic = Utils.spar_inter_server_traffic(G_dict, G_servers, G_replica)

    print("\n"+str(nb_partition_max))
    print("cost_RPSR_replica=", cost_RPSR_replica)
    print("cost_RPSR_traffic=", cost_RPSR_traffic)


