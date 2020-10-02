import numpy as np
import networkx as nx


def coarse(G, nb_levels=1):
    xadj_1, adjncy_1, weight_1 = graph_to_adj_std(G)
    xadj = list()
    adjncy = list()
    weight = list()
    match = list()
    cmap = list()

    for i in range(nb_levels):
        xadj_1, adjncy_1, weight_1, match_1, cmap_1 = coarse_one(xadj_1, adjncy_1, weight_1)
        xadj.append(xadj_1)
        adjncy.append(adjncy_1)
        weight.append(weight_1)
        match.append(list(match_1))
        cmap.append(list(cmap_1))

    return xadj, adjncy, weight, match, cmap


def graph_to_adj_std(G):
    xadj = list([0])
    adjncy = list()
    adjwgt = list()

    A = nx.adjacency_matrix(G)
    np_matrix = A.todense()
    array_matrix = list(np.array(np_matrix))
    for i in range(len(array_matrix)):
        for j in range(len(array_matrix[i])):
            if array_matrix[i][j] > 0:
                adjncy.append(j)
                adjwgt.append(int(array_matrix[i][j]))
        xadj.append(len(adjncy))
        # res.append(new_row)
    return xadj, adjncy, adjwgt


def coarse_one(xadj_0, adjncy_0, weight_0):
    nb_V = len(xadj_0)-1
    match = -(np.ones(nb_V, dtype=np.int))
    cmap = -(np.ones(nb_V, dtype=np.int))
    vertices = list(range(nb_V))

    for i in vertices:
        if match[i] == -1:
            neighbors = adjncy_0[xadj_0[i]:xadj_0[i + 1]]
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
            neighbors = adjncy_0[xadj_0[i]:xadj_0[i + 1]]
            for j in neighbors:
                if cmap[j] == -1:
                    cmap[i] = k
                    cmap[j] = k
                    k += 1
                    break
            if cmap[i] == -1:
                cmap[i] = k
                k += 1

    xadj_1 = list(np.zeros(max(cmap) + 2, dtype=np.int))
    adjncy_1 = list()
    weight_1 = list()
    new_Vs = list(range(0, max(cmap) + 1))

    for k, i in enumerate(new_Vs):
        pairs_i = list(np.argwhere(cmap == i).reshape(-1))
        pair_i_1 = pairs_i[0]
        pair_i_1_neighbors = adjncy_0[xadj_0[pair_i_1]:xadj_0[pair_i_1 + 1]]
        if len(pairs_i) < 2:  # only one element
            for j in new_Vs:
                pairs_j = list(np.argwhere(cmap == j).reshape(-1))
                pair_j_1 = pairs_j[0]
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

    return xadj_1, adjncy_1, weight_1, match, cmap





