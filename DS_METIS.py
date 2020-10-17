import subprocess
import numpy as np
import networkx as nx
import Utils
from collections import defaultdict

# network = nx.DiGraph()
# network.add_node(1, write="20")
# network.add_node(2, write="40")
# network.add_node(3, write="25")
# network.add_node(4, write="30")
# network.add_node(5, write="60")
# network.add_node(6, write="30")
# network.add_node(7, write="40")
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
#
#
# G0 = Utils.to_undirected(network)


def add_weights(G, read, write):
    # 1. order by rank
    list_ranks = list()
    for key in G.nodes:
        list_ranks.append(len(list(G.neighbors(key))))

    list_ranks_sorted_by_index = np.argsort(-np.asarray(list_ranks))

    # 2. add weights
    i = 0
    for u in list_ranks_sorted_by_index:
        G.nodes[u]["write"] = write[i]
        for v in G.neighbors(u):
            G.add_weighted_edges_from([(u, v, read[i])])
        i += 1


def to_graph_file(G, D, file_name, fmt="011"):
    f = open("%s" % file_name, "w")
    n = len(D)
    m = int(sum([len(D[x]) for x in D])/2)
    line = str(n) + " " + str(m) + " " + str(fmt)
    f.write(line+"\n")

    for i, u in enumerate(D):
        line = str(int(G.nodes[u]["write"]))
        # print("rank of %d:"%u, len(D[u]))
        for v in D[u]:
            line += " " + str(v)
            line += " " + str(int(D[u][v]))
        f.write(line)

        if i != len(D) - 1:
            f.write("\n")

    f.close()


pathhack = "/home/ismail/Dev/Ego_Facebook"
G = nx.read_edgelist("%s/facebook_combined.txt" % (pathhack,), create_using=nx.Graph(), nodetype=int).to_directed()
G = Utils.add_weights(G)
G = Utils.to_undirected(G)

# network = nx.DiGraph()
# network.add_node(1, write="20")
# network.add_node(2, write="40")
# network.add_node(3, write="25")
# network.add_node(4, write="30")
# network.add_node(5, write="60")
# network.add_node(6, write="35")
# network.add_node(7, write="40")
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
#
# G = Utils.to_undirected(network)


def nx_to_dict(G):
    m_dict = defaultdict(lambda: {})
    i=0
    for n, nbrs in G.adj.items():
        # m_dict[n]["writesss"] = G.nodes[n]["write"]
        for nbr, eattr in nbrs.items():
            wt = eattr['weight']
            m_dict[n][nbr] = wt
        i += 1
        # print(m_dict[n])
        # if i > 10:
        #     return m_dict
    return m_dict


def generate_read_write(size, read_write_ratio):
    alpha = 3.5
    betta = 10**3
    x = list(range(1, size + 1))
    z = betta * np.power(x, (-alpha))
    r = z*read_write_ratio
    w = z*(1-read_write_ratio)
    return r, w


# r, w = generate_read_write(G.order(), 0.08)
# add_weights(G, r, w)
# G = Utils.to_undirected(G)

# m_dict = nx_to_dict(G)
# print(m_dict)
# to_graph_file(G, m_dict, "../test.txt")



# for key in m_dict:
#     if key > 3000:
#         print(key, len(m_dict[key]))
# print(m_dict)
def to_metis_file_start0(G, file_name, fmt="011"):
    f = open("%s" % file_name, "w")
    n = G.order()
    m = G.number_of_edges()
    line = str(n) + " " + str(m) + " " + str(fmt)
    f.write(line+"\n")

    A = nx.adjacency_matrix(G)
    np_matrix = A.todense()
    array_matrix = list(np.array(np_matrix))
    for i in range(len(array_matrix)):
        line = G.nodes[i+1]["write"] + " "
        for j in range(len(array_matrix[i])):
            if array_matrix[i][j] > 0:
                line += str(j+1) + " "  # +1 is added to start counting from 1
                line += str(np_matrix[i, j]) + " "
        f.write(line+"\n")

    f.close()


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
    output_text = subprocess.run(['gpmetis', file_name, str(nb_partition), '-nooutput'], stdout=subprocess.PIPE).stdout.decode('utf-8')

    for item in output_text.split("\n"):
        if "Edgecut" in item:
            read_traffic = [int(s) for s in item.replace(",", "").split() if s.isdigit()][0]
            # print(read_traffic)
    # print(output_text)
    return read_traffic


def get_read_traffic_v0(nb_partition=2):
    file_name = '../test.txt'
    to_metis_file(G, file_name)
    read_traffic = 0
    output_text = subprocess.run(['gpmetis', file_name, str(nb_partition), '-nooutput'], stdout=subprocess.PIPE).stdout.decode('utf-8')

    print(output_text)
    for item in output_text.split("\n"):
        if "Edgecut" in item:
            read_traffic = [int(s) for s in item.replace(",", "").split() if s.isdigit()][0]
            # print(read_traffic)
    return read_traffic


nb_partition_max = 4
print(nb_partition_max, get_read_traffic(G, nb_partition=nb_partition_max))

# for nb_partition_max in [4, 8, 16, 32, 64, 128]:
#     print(nb_partition_max, get_read_traffic(G, nb_partition=nb_partition_max))



