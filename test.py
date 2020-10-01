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


xadj_0, adjncy_0, adjwgt = graph_to_adj_std(G)

print("xadj", xadj_0)
print("adjncy", len(adjncy_0), adjncy_0)

# np.random.seed(0)
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
adjwgt_1 = list()


def get_pairs(cmap, i):
    return list(np.argwhere(cmap == i).reshape(-1))


for i in range(0, max(cmap)+1):
    pairs = get_pairs(cmap, i)
    pair_1 = pairs[0]
    pair_2 = -1
    pair_2_neighbors = list()
    pair_1_neighbors = adjncy_0[xadj_0[pair_1]:xadj_0[pair_1+1]]
    # print(pair_1, pair_1_neighbors)

    if len(pairs) < 2: # only one element
        for n1 in pair_1_neighbors:
            adjncy_1.insert(xadj_1[i + 1], cmap[n1])
            for tt in range(i + 1, len(xadj_1)):
                xadj_1[tt] += 1
    else:
        pair_2 = pairs[1]
        pair_2_neighbors = adjncy_0[xadj_0[pair_2]:xadj_0[pair_2 + 1]]
        pair_2_neighbors.remove(pair_1)
        pair_1_neighbors.remove(pair_2)
        # # 1. Shared neighbors
        # shared_neighbors = list(set(pair_1_neighbors).intersection(pair_2_neighbors))
        #
        # # 2. non shared neighbors
        # pair_1_neighbors = [x for x in pair_1_neighbors if x not in shared_neighbors]
        # pair_2_neighbors = [x for x in pair_2_neighbors if x not in shared_neighbors]

        for n1 in pair_1_neighbors:
            n1_new_pair_id = cmap[n1]
            for n2 in pair_2_neighbors:
                n2_new_pair_id = cmap[n2]
                curr_i_neighbors = adjncy_1[xadj_1[i]:xadj_1[i + 1]]

                if n1_new_pair_id == n2_new_pair_id:
                    if cmap[n1] not in curr_i_neighbors:
                        if i == 0:
                            print(i, n1, n2, "inserting_A",  cmap[n1], "at", xadj_1[i + 1])

                        # create edge between i and cmap[n1}
                        adjncy_1.insert(xadj_1[i + 1], cmap[n1])
                        for tt in range(i + 1, len(xadj_1)):
                            xadj_1[tt] += 1

                        # sum edges weights (pair_1, n1) & (pair_2, n2)

        for n1 in pair_1_neighbors:
            n1_new_pair_id = cmap[n1]
            for n2 in pair_2_neighbors:
                n2_new_pair_id = cmap[n2]
                curr_i_neighbors = adjncy_1[xadj_1[i]:xadj_1[i + 1]]

                if n1_new_pair_id != n2_new_pair_id:
                    if cmap[n1] not in curr_i_neighbors:
                        if i == 0:
                            print(i, n1, n2, "inserting_B", cmap[n1], "at", xadj_1[i + 1])
                            print("curr_i_neighbors", curr_i_neighbors)
                            print("xadj", xadj_1)
                        # create edge between i and cmap[n1}
                        adjncy_1.insert(xadj_1[i + 1], cmap[n1])
                        for tt in range(i + 1, len(xadj_1)):
                            xadj_1[tt] += 1
                    if cmap[n2] not in curr_i_neighbors:
                        if i == 0:
                            print(i, n2, "inserting_C", cmap[n1], "at", xadj_1[i + 1])

                        # create edge between i and cmap[n2}
                        adjncy_1.insert(xadj_1[i + 1], cmap[n2])
                        for tt in range(i + 1, len(xadj_1)):
                            xadj_1[tt] += 1


# x = (np.argwhere(cmap == 1)).reshape(-1)
# print(x.tolist())
# print(list(np.where(cmap == 1)))

print(xadj_1)
print(adjncy_1)
# print(len(adjwgt), adjwgt)
# # print(vwgt)











