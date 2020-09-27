import numpy as np
import pymetis
import networkx as nx
import sys

import Utils

network = nx.DiGraph()
network.add_node(1, write="20")
network.add_node(2, write="40")
network.add_node(3, write="25")
network.add_node(4, write="30")
network.add_node(5, write="60")
network.add_node(6, write="30")
network.add_node(7, write="40")

network.add_weighted_edges_from([(1, 2, 20), (2, 1, 25)])
network.add_weighted_edges_from([(1, 3, 25), (3, 1, 40)])
network.add_weighted_edges_from([(1, 4, 20), (4, 1, 45)])
network.add_weighted_edges_from([(1, 6, 30), (6, 1, 50)])
network.add_weighted_edges_from([(4, 3, 50), (3, 4, 20)])
network.add_weighted_edges_from([(6, 2, 30), (2, 6, 25)])
network.add_weighted_edges_from([(2, 3, 30), (3, 2, 10)])
network.add_weighted_edges_from([(2, 7, 40), (7, 2, 20)])
network.add_weighted_edges_from([(3, 5, 30), (5, 3, 45)])


G = Utils.to_undirected(network)


def graph_to_adj_std(G):
    res = list()
    A = nx.adjacency_matrix(G)
    np_matrix = A.todense()
    array_matrix = list(np.array(np_matrix))
    for i in range(len(array_matrix)):
        new_row = list()
        for j in range(len(array_matrix[i])):
            if array_matrix[i][j] > 0:
                new_row.append(j)
        res.append(new_row)
    return res

def to_metis_file(G, fmt="011"):
    f = open("my_graph.txt", "w")
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
    print(n, m)

to_metis_file(G)

# print(A)

sys.exit()

















# network = nx.Graph()
# network.add_node(1, write="20")
# network.add_node(2, write="40")
# network.add_node(3, write="25")
# network.add_node(4, write="30")
# network.add_node(5, write="60")
# network.add_node(6, write="30")
# network.add_node(7, write="40")
#
# network.add_weighted_edges_from([(1, 2, 45)])
# network.add_weighted_edges_from([(1, 3, 65)])
# network.add_weighted_edges_from([(1, 4, 65)])
# network.add_weighted_edges_from([(1, 6, 80)])
# network.add_weighted_edges_from([(4, 3, 70)])
# network.add_weighted_edges_from([(6, 2, 55)])
# network.add_weighted_edges_from([(2, 3, 40)])
# network.add_weighted_edges_from([(2, 7, 60)])
# network.add_weighted_edges_from([(3, 5, 75)])
#
# G = network
# G.to
# A = nx.adjacency_matrix(G)

# np_matrix = A.todense()
# array_matrix = list(np.array(np_matrix))

# A = nx.to_numpy_matrix(G)

# print(type(A), "\n", A)


def graph_to_adj_std(G):
    res = list()
    A = nx.adjacency_matrix(G)
    np_matrix = A.todense()
    array_matrix = list(np.array(np_matrix))
    for i in range(len(array_matrix)):
        new_row = list()
        for j in range(len(array_matrix[i])):
            if array_matrix[i][j] > 0:
                new_row.append(j)
        res.append(new_row)
    return res


def graph_to_adjncy(G):
    adjncy = list()
    adjwgt = list()
    xadj = list()
    xadj.append(0)

    A = nx.adjacency_matrix(G)
    np_matrix = A.todense()
    # print(np_matrix[0,1])
    array_matrix = list(np.array(np_matrix))
    for i in range(len(array_matrix)):
        nb_adj=0
        for j in range(len(array_matrix[i])):
            if array_matrix[i][j] > 0:
                nb_adj +=1
                adjncy.append(j)
                adjwgt.append(np_matrix[i, j])
                # print(np_matrix[i, j])
        xadj.append(nb_adj)
    return adjncy, xadj, adjwgt


A_std = graph_to_adj_std(G)
adjncy, xadj, adjwgt = graph_to_adjncy(G)

# print(A_std)
print(adjncy)
print(xadj)
print(adjwgt)

# print(adjacency_list)
n_cuts, membership = pymetis.part_graph(2, adjncy=adjncy, xadj=xadj, eweights=adjwgt)
#
# nodes_part_0 = np.argwhere(np.array(membership) == 0).ravel() # [3, 5, 6]
# nodes_part_1 = np.argwhere(np.array(membership) == 1).ravel() # [0, 1, 2, 4]
#
print(n_cuts, membership)

