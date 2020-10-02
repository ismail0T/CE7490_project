for i in range(0, max(cmap)+1):
    pairs = list(np.argwhere(cmap == i).reshape(-1))
    pair_1 = pairs[0]
    pair_2 = -1
    pair_2_neighbors = list()
    pair_1_neighbors = adjncy_0[xadj_0[pair_1]:xadj_0[pair_1+1]]
    # print(pair_1, pair_1_neighbors)

    if len(pairs) < 2:  # only one element
        for n1 in pair_1_neighbors:
            adjncy_1.insert(xadj_1[i + 1], cmap[n1])
            l_wt = list(
                xadj_0[pair_1] + np.argwhere(np.asarray(adjncy_0)[xadj_0[pair_1]:xadj_0[pair_1 + 1]] == n1).reshape(-1))
            wt = adjwgt_0[l_wt[0]]
            adjwgt_1.insert(xadj_1[i + 1], wt)
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
                        # if i == 0:
                        #     print(i, n1, n2, "inserting_A",  cmap[n1], "at", xadj_1[i + 1])

                        # create edge between i and cmap[n1}
                        adjncy_1.insert(xadj_1[i + 1], cmap[n1])

                        l_wt1 = list(xadj_0[pair_1] + np.argwhere(
                            np.asarray(adjncy_0)[xadj_0[pair_1]:xadj_0[pair_1 + 1]] == n1).reshape(-1))
                        wt = adjwgt_0[l_wt1[0]]
                        l_wt2 = list(xadj_0[pair_2] + np.argwhere(
                            np.asarray(adjncy_0)[xadj_0[pair_2]:xadj_0[pair_2 + 1]] == n2).reshape(-1))
                        wt += adjwgt_0[l_wt2[0]]
                        adjwgt_1.insert(xadj_1[i + 1], wt)

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
                        # if i == 0:
                        #     print(i, n1, n2, "inserting_B", cmap[n1], "at", xadj_1[i + 1])
                        #     print("curr_i_neighbors", curr_i_neighbors)
                        #     print("xadj", xadj_1)
                        # create edge between i and cmap[n1}
                        adjncy_1.insert(xadj_1[i + 1], cmap[n1])
                        # print(i, n1, n2)
                        # print(pair_1, pair_2)
                        l_wt = list(xadj_0[pair_1]+np.argwhere(np.asarray(adjncy_0)[xadj_0[pair_1]:xadj_0[pair_1+1]] == n1).reshape(-1))
                        wt = adjwgt_0[l_wt[0]]
                        adjwgt_1.insert(xadj_1[i + 1], wt)
                        for tt in range(i + 1, len(xadj_1)):
                            xadj_1[tt] += 1
                    if cmap[n2] not in curr_i_neighbors:
                        # if i == 0:
                        #     print(i, n2, "inserting_C", cmap[n1], "at", xadj_1[i + 1])

                        # create edge between i and cmap[n2}
                        adjncy_1.insert(xadj_1[i + 1], cmap[n2])
                        l_wt = list(xadj_0[pair_2] + np.argwhere(
                            np.asarray(adjncy_0)[xadj_0[pair_2]:xadj_0[pair_2 + 1]] == n2).reshape(-1))
                        wt = adjwgt_0[l_wt[0]]
                        adjwgt_1.insert(xadj_1[i + 1], wt)
                        for tt in range(i + 1, len(xadj_1)):
                            xadj_1[tt] += 1