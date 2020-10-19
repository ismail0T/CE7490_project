import subprocess
import numpy as np
import networkx as nx
import Utils
from collections import defaultdict


pathhack = "/home/ismail/Dev/Ego_Facebook"
G = nx.read_edgelist("%s/facebook_combined.txt" % (pathhack,), create_using=nx.Graph(), nodetype=int).to_directed()
G = Utils.add_weights(G)
G = Utils.to_undirected(G)
G_dict = Utils.nx_to_dict(G)


def to_metis_file(G, file_name, fmt="011"):
    f = open("%s" % file_name, "w")
    n = G.order()
    m = G.number_of_edges()
    line = str(n) + " " + str(m) + " " + str(fmt)
    f.write(line+"\n")

    A = nx.adjacency_matrix(G)
    np_matrix = A.todense()
    array_matrix = list(np.array(np_matrix))
    for i in range(len(array_matrix)):
        line = str(G.nodes[i]["write"]) + " "
        for j in range(len(array_matrix[i])):
            if array_matrix[i][j] > 0:
                line += str(j+1) + " "  # +1 is added to start counting from 1
                line += str(np_matrix[i, j]) + " "
        f.write(line+"\n")

    f.close()


def get_read_traffic(G, nb_partition=2):
    file_name = '../test.txt'
    to_metis_file(G, file_name)
    read_traffic = 0
    output_text = subprocess.run(['gpmetis', file_name, str(nb_partition)], stdout=subprocess.PIPE).stdout.decode('utf-8')

    for item in output_text.split("\n"):
        if "Edgecut" in item:
            read_traffic = [int(s) for s in item.replace(",", "").split() if s.isdigit()][0]

    # print(output_text)
    return read_traffic


def selective_replica(G_dict, G_servers, nb_partition=2):
    sum_in = defaultdict(lambda: np.zeros(nb_partition))
    G_replica_0 = defaultdict(list)
    for u in G_dict:
        for v in G_dict[u]["neighbors"]:
            if G_servers[u] != G_servers[v]:
                sum_in[v][G_servers[u]] += G_dict[u]["neighbors"][v] / 2
    # print(len(sum_in))
    for none, key in enumerate(sum_in):
        for server_id, read_weight in enumerate(sum_in[key]):
            if G_dict[key]["write"] < read_weight:  # Do replication
                G_replica_0[key].append(server_id)

    return G_replica_0





for nb_partition_max in [4, 8, 16, 32, 64, 128, 256]:
    read_traffic_metis = get_read_traffic(G, nb_partition=nb_partition_max)
    G_servers = Utils.read_servers(nb_partition_max)
    G_replica = selective_replica(G_dict, G_servers, nb_partition=nb_partition_max)

    cost_METIS_SR_replica = Utils.spar_inter_server_cost(G_replica)
    cost_METIS_SR_traffic = Utils.metis_sr_inter_server_traffic(G_dict, G_servers, G_replica)

    print("\n"+str(nb_partition_max))
    print("cost_METIS_SR_replica=", cost_METIS_SR_replica)
    print("cost_METIS_SR_traffic=", cost_METIS_SR_traffic)


# print(nb_partition_max, read_traffic_metis, len(G_servers))

# for nb_partition_max in [4, 8, 16, 32, 64, 128]:
#     print(nb_partition_max, get_read_traffic(G, nb_partition=nb_partition_max))



