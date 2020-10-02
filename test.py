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

# network.add_weighted_edges_from([(0, 1, 2)])
# network.add_weighted_edges_from([(0, 3, 2)])
# network.add_weighted_edges_from([(1, 2, 5)])
# network.add_weighted_edges_from([(1, 3, 7)])
# network.add_weighted_edges_from([(1, 4, 3)])
# network.add_weighted_edges_from([(2, 4, 2)])
# network.add_weighted_edges_from([(2, 5, 2)])
# network.add_weighted_edges_from([(3, 6, 2)])
# network.add_weighted_edges_from([(4, 5, 2)])
# network.add_weighted_edges_from([(4, 7, 20)])
# network.add_weighted_edges_from([(5, 8, 2)])
# network.add_weighted_edges_from([(6, 7, 2)])
# network.add_weighted_edges_from([(7, 8, 2)])



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
    xadj = list([0])
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


xadj_0, adjncy_0, weight_0 = graph_to_adj_std(G)

print("xadj_0", xadj_0)
print("adjncy_0", len(adjncy_0), adjncy_0)
print("adjwgt_0", weight_0)
# np.random.seed(0)

print(G.order(), len(xadj_0)-1)

match = -(np.ones(G.order(), dtype=np.int))
cmap = -(np.ones(G.order(), dtype=np.int))

vertices = list(range(G.order()))

# np.random.shuffle(vertices)
# print("vertices", vertices)

for i in vertices:
    if match[i] == -1:
        neighbors = adjncy_0[xadj_0[i]:xadj_0[i+1]]
        for j in neighbors:
            if match[j] == -1:
                match[i] = j
                match[j] = i
                break
        if match[i] == -1:
            match[i] = i
k = 0
for i in vertices:
    if cmap[i] == -1:
        neighbors = adjncy_0[xadj_0[i]:xadj_0[i+1]]
        for j in neighbors:
            if cmap[j] == -1:
                cmap[i] = k
                cmap[j] = k
                k += 1
                break
        if cmap[i] == -1:
            cmap[i] = k
            k += 1
print("\nmatch", match)
print("cmap", cmap)

xadj_1 = list(np.zeros(max(cmap)+2, dtype=np.int))
adjncy_1 = list()
weight_1 = list()


# def get_pairs(cmap, i):
#     return list(np.argwhere(cmap == i).reshape(-1))

new_Vs = list(range(0, max(cmap)+1))

for k, i in enumerate(new_Vs):
    pairs_i = list(np.argwhere(cmap == i).reshape(-1))
    pair_i_1 = pairs_i[0]
    pair_i_2 = -1
    pair_i_2_neighbors = list()
    pair_i_1_neighbors = adjncy_0[xadj_0[pair_i_1]:xadj_0[pair_i_1 + 1]]
    if len(pairs_i) < 2:  # only one element
        for j in new_Vs:
            pairs_j = list(np.argwhere(cmap == j).reshape(-1))
            pair_j_1 = pairs_j[0]
            pair_j_2 = -1
            pair_j_2_neighbors = list()
            pair_j_1_neighbors = adjncy_0[xadj_0[pair_j_1]:xadj_0[pair_j_1 + 1]]
            edges_to_collapse = list()
            if len(pairs_j) < 2:  # only one element
                pass
            else:
                pair_j_2 = pairs_j[1]
                pair_j_2_neighbors = adjncy_0[xadj_0[pair_j_2]:xadj_0[pair_j_2 + 1]]
                pair_j_2_neighbors.remove(pair_j_1)
                pair_j_1_neighbors.remove(pair_j_2)

                if pair_i_1 in pair_j_1_neighbors:
                    edges_to_collapse.append((pair_i_1, pair_j_1))
                if pair_i_1 in pair_j_2_neighbors:
                    edges_to_collapse.append((pair_i_1, pair_j_2))

            if len(edges_to_collapse) > 0:
                wt_total = 0
                for edge in edges_to_collapse:
                    u = edge[0]
                    v = edge[1]
                    l_wt1 = list(xadj_0[u] + np.argwhere(
                        np.asarray(adjncy_0)[xadj_0[u]:xadj_0[u + 1]] == v).reshape(-1))
                    wt_total += weight_0[l_wt1[0]]

                adjncy_1.insert(xadj_1[i + 1], j)
                weight_1.insert(xadj_1[i + 1], wt_total)
                for tt in range(i + 1, len(xadj_1)):
                    xadj_1[tt] += 1
    else:
        pair_i_2 = pairs_i[1]
        pair_i_2_neighbors = adjncy_0[xadj_0[pair_i_2]:xadj_0[pair_i_2 + 1]]
        pair_i_2_neighbors.remove(pair_i_1)
        pair_i_1_neighbors.remove(pair_i_2)

        for j in new_Vs:
            pairs_j = list(np.argwhere(cmap == j).reshape(-1))
            pair_j_1 = pairs_j[0]
            pair_j_2 = -1
            pair_j_2_neighbors = list()
            pair_j_1_neighbors = adjncy_0[xadj_0[pair_j_1]:xadj_0[pair_j_1 + 1]]
            edges_to_collapse = list()
            if len(pairs_j) < 2:  # only one element

                if pair_i_1 in pair_j_1_neighbors:
                    edges_to_collapse.append((pair_i_1, pair_j_1))
                if pair_i_2 in pair_j_1_neighbors:
                    edges_to_collapse.append((pair_i_2, pair_j_1))

            else:
                pair_j_2 = pairs_j[1]
                pair_j_2_neighbors = adjncy_0[xadj_0[pair_j_2]:xadj_0[pair_j_2 + 1]]
                pair_j_2_neighbors.remove(pair_j_1)
                pair_j_1_neighbors.remove(pair_j_2)

                if pair_i_1 in pair_j_1_neighbors:
                    edges_to_collapse.append((pair_i_1, pair_j_1))
                if pair_i_1 in pair_j_2_neighbors:
                    edges_to_collapse.append((pair_i_1, pair_j_2))
                if pair_i_2 in pair_j_1_neighbors:
                    edges_to_collapse.append((pair_i_2, pair_j_1))
                if pair_i_2 in pair_j_2_neighbors:
                    edges_to_collapse.append((pair_i_2, pair_j_2))

                # if i==1 and j==3:
                    # print(i, j)
                    # print(i, j, edges_to_collapse)
                # print(pair_j_1_neighbors, pair_j_2_neighbors)
            if len(edges_to_collapse) > 0:
                wt_total = 0
                for edge in edges_to_collapse:
                    u = edge[0]
                    v = edge[1]
                    l_wt1 = list(xadj_0[u] + np.argwhere(
                        np.asarray(adjncy_0)[xadj_0[u]:xadj_0[u + 1]] == v).reshape(-1))
                    wt_total += weight_0[l_wt1[0]]

                adjncy_1.insert(xadj_1[i + 1], j)
                weight_1.insert(xadj_1[i + 1], wt_total)
                for tt in range(i + 1, len(xadj_1)):
                    xadj_1[tt] += 1


# x = (np.argwhere(cmap == 1)).reshape(-1)
# print(x.tolist())
# print(list(np.where(cmap == 1)))

print("xadj_1", xadj_1)
print("adjncy_1", adjncy_1)
print("adjwgt_1", weight_1)
# print(len(adjwgt), adjwgt)
# # print(vwgt)











