import subprocess
import numpy as np
import networkx as nx
import pymetis

import Utils
from collections import defaultdict

network = nx.Graph()
network.add_node(0, write="20")
network.add_node(1, write="40")
network.add_node(2, write="25")
network.add_node(3, write="30")
network.add_node(4, write="60")
network.add_node(5, write="30")
network.add_node(6, write="40")
network.add_node(7, write="40")
network.add_node(8, write="40")

network.add_weighted_edges_from([(0, 1, 2)])
network.add_weighted_edges_from([(0, 3, 2)])
network.add_weighted_edges_from([(1, 2, 2)])
network.add_weighted_edges_from([(1, 4, 2)])
network.add_weighted_edges_from([(2, 5, 2)])
network.add_weighted_edges_from([(3, 4, 2)])
network.add_weighted_edges_from([(3, 6, 2)])
network.add_weighted_edges_from([(4, 5, 2)])
network.add_weighted_edges_from([(4, 7, 2)])
network.add_weighted_edges_from([(5, 8, 2)])
network.add_weighted_edges_from([(6, 7, 2)])
network.add_weighted_edges_from([(7, 8, 2)])



# network.add_weighted_edges_from([(0, 1, 20), (1, 0, 25)])
# network.add_weighted_edges_from([(0, 2, 25), (2, 0, 40)])
# network.add_weighted_edges_from([(0, 3, 20), (3, 0, 45)])
# network.add_weighted_edges_from([(0, 5, 30), (5, 0, 50)])
# network.add_weighted_edges_from([(3, 2, 50), (2, 3, 20)])
# network.add_weighted_edges_from([(5, 1, 30), (1, 5, 25)])
# network.add_weighted_edges_from([(1, 2, 30), (2, 1, 10)])
# network.add_weighted_edges_from([(1, 6, 40), (6, 1, 20)])
# network.add_weighted_edges_from([(2, 4, 30), (4, 2, 45)])

# network.add_weighted_edges_from([(1, 2, 20), (2, 1, 25)])
# network.add_weighted_edges_from([(1, 3, 25), (3, 1, 40)])
# network.add_weighted_edges_from([(1, 4, 20), (4, 1, 45)])
# network.add_weighted_edges_from([(1, 6, 30), (6, 1, 50)])
# network.add_weighted_edges_from([(4, 3, 50), (3, 4, 20)])
# network.add_weighted_edges_from([(6, 2, 30), (2, 6, 25)])
# network.add_weighted_edges_from([(2, 3, 30), (3, 2, 10)])
# network.add_weighted_edges_from([(2, 7, 40), (7, 2, 20)])
# network.add_weighted_edges_from([(3, 5, 30), (5, 3, 45)])

G = network  #  Utils.to_undirected(network)

vwgt = [int(G.nodes[key]["write"]) for key in G.nodes]


def graph_to_adj_std(G):
    res = list()
    xadj = list()
    xadj.append(0)
    adjncy = list()
    adjwgt = list()

    A = nx.adjacency_matrix(G)
    np_matrix = A.todense()
    # print(np_matrix)
    array_matrix = list(np.array(np_matrix))
    for i in range(len(array_matrix)):
        for j in range(len(array_matrix[i])):
            if array_matrix[i][j] > 0:
                adjncy.append(j)
                adjwgt.append(int(array_matrix[i][j]))
        xadj.append(len(adjncy))
        # res.append(new_row)
    return xadj, adjncy, adjwgt


xadj, adjncy, adjwgt = graph_to_adj_std(G)

print("xadj", xadj)
print("adjncy", len(adjncy), adjncy)

# np.random.seed(0)
match = -(np.ones(G.order(), dtype=np.int))
cmap = -(np.ones(G.order(), dtype=np.int))

vertices = list(range(G.order()))

# np.random.shuffle(vertices)
print("vertices", vertices)

for i in vertices:
    if match[i] == -1:
        neighbors = adjncy[xadj[i]:xadj[i+1]]
        for j in neighbors:
            if match[j] == -1:
                match[i] = j
                match[j] = i
                break
        if match[i] == -1:
            match[i] = i

k=0
for i in vertices:
    if cmap[i] == -1:
        neighbors = adjncy[xadj[i]:xadj[i+1]]
        for j in neighbors:
            if cmap[j] == -1:
                cmap[i] = k
                cmap[j] = k
                k += 1
                break
        if cmap[i] == -1:
            cmap[i] = k
            k += 1
print("match", match)
print("cmap", cmap)

# print(len(adjwgt), adjwgt)
# # print(vwgt)
#
# n_cuts, membership = pymetis.part_graph(2, xadj=xadj, adjncy=adjncy, eweights=adjwgt, vweights=vwgt)
# print(n_cuts)
# print(membership)
#
# print("kkk")

# k=0
# for i in vertices:
#     if match[i] == -1:
#         neighbors = adjncy[xadj[i]:xadj[i+1]]
#         for j in neighbors:
#             if match[j] == -1:
#                 match[i] = k
#                 match[j] = k
#                 k += 1
#                 break
#         if match[i] == -1:
#             match[i] = k
#             k += 1