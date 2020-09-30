import random
import sys
import Utils
import networkx as nx
import numpy as np
from collections import defaultdict


def nx_to_dict(G):
    m_dict = defaultdict(lambda: {})
    i = 0
    for n, nbrs in G.adj.items():
        m_dict[n]["write"] = G.nodes[n]["write"]
        dict_nebr = defaultdict()
        for nbr, eattr in nbrs.items():
            wt = eattr['weight']
            dict_nebr[nbr] = wt
        m_dict[n]["neighbors"] = dict_nebr
        i += 1
    return m_dict


def generate_read_write(size):
    r = np.ones(size)
    w = r * 10
    return r, w


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


def add_node_spar(u):
    id_partition = int(np.argmin(load))
    G_servers[u] = id_partition
    load[id_partition] += 1
    if len(G_replica[u]) == 0:  # add slave replica for first time
        partions_to_replicate_on = list(range(nb_partition_max))
        partions_to_replicate_on.remove(id_partition)
        # np.random.shuffle(partions_to_replicate_on)
        for i in range(min(k_min, len(partions_to_replicate_on))):
            # if partions_to_replicate_on[i] in G_replica[u]:
            #     print("already there", partions_to_replicate_on[i])
            G_replica[u].append(partions_to_replicate_on[i])


def add_edge_spar(u, v, wt):
    u_orign_partition = G_servers[u]
    v_orign_partition = G_servers[v]
    if u_orign_partition != v_orign_partition:
        if u_orign_partition in G_replica[v] and v_orign_partition in G_replica[u]:
            # do noting
            pass

        else:
            #  Choose best configuration among the 3
            total_nb_slave_replica = sum(len(G_replica[x]) for x in G_replica)

            # 1.-- config 1: status quo
            do_replica_for = [0, 0]
            if v_orign_partition not in G_replica[u]:
                do_replica_for[0] = 1
            if u_orign_partition not in G_replica[v]:
                do_replica_for[1] = 1
                # print("already_3_1", u, v, "--", u_orign_partition, G_replica[v], v_orign_partition)

            cost_config_1 = sum(do_replica_for) + total_nb_slave_replica

            # 2.-- config 2: the master of u go to v's master partition

            u_neighbours_inside = list()
            u_neighbours_outside = list()
            for x in G_dict[u]["neighbors"]:
                if G_servers[x] == G_servers[u]:
                    u_neighbours_inside.append(x)
                else:
                    u_neighbours_outside.append(x)

            u_neighbours_replica_to_delete = list()
            u_neighbours_to_replicate = u_neighbours_inside.copy()

            for neighbour_id_outside in u_neighbours_outside:
                to_delete = True
                for neighbour_id_inside in u_neighbours_inside:
                    if neighbour_id_outside in G_dict[neighbour_id_inside]["neighbors"]:  # this outside neighbour has another neighbour from the same partition as u, do not delete its replica
                        to_delete = False
                # check if there will still at least k replica for this node
                if to_delete:
                    to_delete = len(G_replica[neighbour_id_outside]) > k_min
                # check if there is a replica for this neighbor on local server
                if to_delete:
                    if u_orign_partition not in G_replica[neighbour_id_outside]:
                        to_delete = False
                if to_delete:
                    # G_replica[neighbour_id_outside].remove(u_orign_partition)
                    u_neighbours_replica_to_delete.append(neighbour_id_outside)

            for neighbour_id_inside in u_neighbours_inside:
                if v in G_replica[neighbour_id_inside]:
                    # print(u, v)
                    u_neighbours_to_replicate.remove(neighbour_id_inside)

            cost_config_2 = len(u_neighbours_to_replicate) - len(u_neighbours_replica_to_delete) + total_nb_slave_replica + (len(
                u_neighbours_inside) > 0)  # the last term is for u to replicate itself on its old partition

            # 3.-- config 3: the master of v go to u's master partition
            v_neighbours_inside = list()
            v_neighbours_outside = list()
            for x in G_dict[u]["neighbors"]:
                if G_servers[x] == G_servers[u]:
                    v_neighbours_inside.append(x)
                else:
                    v_neighbours_outside.append(x)

            v_neighbours_replica_to_delete = list()
            v_neighbours_to_replicate = v_neighbours_inside.copy()

            for neighbour_id_outside in v_neighbours_outside:
                to_delete = True
                for neighbour_id_inside in v_neighbours_inside:
                    if neighbour_id_outside in G_dict[neighbour_id_inside]["neighbors"]:  # this outside neighbour has another neighbour from the same partition as u, do not delete its replica
                        to_delete = False
                # check if there will still at least k replica for this node
                if to_delete:
                    to_delete = len(G_replica[neighbour_id_outside]) > k_min
                    # check if there is a replica for this neighbor on local server
                if to_delete:
                    if v_orign_partition not in G_replica[neighbour_id_outside]:
                        to_delete = False
                if to_delete:
                    # G_replica[neighbour_id_outside].remove(u_orign_partition)
                    v_neighbours_replica_to_delete.append(neighbour_id_outside)

            for neighbour_id_inside in v_neighbours_inside:
                if v in G_replica[neighbour_id_inside]:
                    # print(u, v)
                    v_neighbours_to_replicate.remove(neighbour_id_inside)

            cost_config_3 = len(v_neighbours_to_replicate) - len(v_neighbours_replica_to_delete) + total_nb_slave_replica + (len(v_neighbours_inside) > 0)  # the last term is for u to replicate itself on its old partition

            # print("\ncost_config", cost_config_1, cost_config_2, cost_config_3)

            # expected new balance
            expected_new_load_config1 = load.copy()
            expected_new_load_config2 = load.copy()
            expected_new_load_config3 = load.copy()
            expected_new_load_config2[u_orign_partition] -= 1
            expected_new_load_config2[v_orign_partition] += 1
            expected_new_load_config3[v_orign_partition] -= 1
            expected_new_load_config3[u_orign_partition] += 1

            ratio_load_config1 = (max(expected_new_load_config1) - min(expected_new_load_config1)) / sum(
                expected_new_load_config1)
            ratio_load_config2 = (max(expected_new_load_config2) - min(expected_new_load_config2)) / sum(
                expected_new_load_config2)
            ratio_load_config3 = (max(expected_new_load_config3) - min(expected_new_load_config3)) / sum(
                expected_new_load_config3)

            do_config = Utils.choose_best_config(cost_config_1, cost_config_2, cost_config_3, ratio_load_config1,
                                                 ratio_load_config2, ratio_load_config3)

            if do_config == 0:
                if do_replica_for[0]:  # create replica for u on v's partition
                    G_replica[u].append(v_orign_partition)
                if do_replica_for[1]:  # create replica for v on u's partition
                    G_replica[v].append(u_orign_partition)

            elif do_config == 1:  # config 2: the master of u go to v's master partition
                # 1. replicate (to v's server)
                for key in u_neighbours_to_replicate:
                    G_replica[key].append(v_orign_partition)
                # 2. delete unnecessary replicas (from u)
                for key in u_neighbours_replica_to_delete:
                    G_replica[key].remove(u_orign_partition)

                # 3. move master replica and create new slave replica on the current partition
                if len(u_neighbours_inside)>0:
                    G_replica[u].append(G_servers[u])
                G_servers[u] = v_orign_partition  # move master replica
                load[u_orign_partition] -= 1
                load[v_orign_partition] += 1

            elif do_config == 2:  # config 3: the master of v go to u's master partition
                # 1. replicate (to u's server)
                for key in v_neighbours_to_replicate:
                    G_replica[key].append(u_orign_partition)

                # 2. delete unnecessary replicas
                for key in v_neighbours_replica_to_delete:
                    G_replica[key].remove(v_orign_partition)

                # 3. move master replica and create new slave replica on the current partition
                if len(v_neighbours_inside)>0:
                    G_replica[v].append(G_servers[v])
                G_servers[v] = u_orign_partition  # move master replica
                load[v_orign_partition] -= 1
                load[u_orign_partition] += 1


pathhack = "/home/ismail/Dev/Ego_Facebook"
G_0 = nx.read_edgelist("%s/facebook_combined.txt" % (pathhack,), create_using=nx.Graph(), nodetype=int).to_directed()

r, w = generate_read_write(G_0.order())
add_weights(G_0, r, w)
G_0 = Utils.to_undirected(G_0)

G_dict = nx_to_dict(G_0)
G_servers = defaultdict(lambda: -1)
G_replica = defaultdict(list)

nb_partition_max = 16
k_min = 2
load = np.zeros(nb_partition_max)


def SPAR():
    for u in G_dict:
        print(u)
        if G_servers[u] == -1:  # no server assigned yet
            add_node_spar(u)

        for v in G_dict[u]["neighbors"]:
            wt_edge = G_dict[u]["neighbors"][v]
            if G_servers[v] == -1:  # no server assigned yet
                add_node_spar(v)
            add_edge_spar(u, v, wt_edge)


SPAR()
print(len(G_dict), len(G_replica))
# print(G_dict[1]["neighbors"])
# for k in G_dict[1]["neighbors"]:
#     print(G_dict[1]["neighbors"][k])
# print(G_replica[1])
