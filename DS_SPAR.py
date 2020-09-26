import networkx as nx
import numpy as np
from collections import defaultdict

import Utils


def spar(G_orig, nb_partition_max=2, k_min=2):
    nb_replicated_nodes = 0
    G_new = nx.DiGraph()

    # arr = np.array([1, 2, 3, 4])
    # np.random.shuffle(arr)
    # new_arr = np.array_split(arr, nb_partition_max)

    for key in list(G_orig.nodes):
        # print(key, G_orig.nodes[key])
        # 1. Create node
        id_partition = get_low_replica(G_new, nb_partition_max)
        add_node_spar(G_new, key, label=G_orig.nodes[key]["label"], write=G_orig.nodes[key]["write"], copy_of=-1,
                      server=id_partition)

        # 2. Create K replica
        partions_to_replicate_on = list(range(nb_partition_max))
        partions_to_replicate_on.remove(id_partition)
        np.random.shuffle(partions_to_replicate_on)
        for i in range(min(k_min, len(partions_to_replicate_on))):
            nb_replicated_nodes += 1
            id_new_node = Utils.get_largest_ID(G_orig) + nb_replicated_nodes
            add_node_spar(G_new, id_new_node, label=G_orig.nodes[key]["label"], write=0, copy_of=key,
                          server=partions_to_replicate_on[i])

    # 3. Add edges
    for (u, v, wt) in G_orig.edges.data('weight'):
        add_edge_spar(G_new, u, v, wt)

    # 4. remove unnecessarily replica
    # for key in list(G_new.nodes):

    # for key in list(G_new.nodes):
    #     print(key, G_new.nodes[key])

    return G_new


def get_low_replica(G, nb_partition_max):
    counts = np.zeros(nb_partition_max)
    for key in list(G.nodes):
        if G.nodes[key]["server"] != -1:  # only master replicas
            counts[G.nodes[key]["server"]] += 1

    return np.argmin(counts)


# def add_node_spar(G, id_new, label, write, copy_of, server):
#     G.add_node(id_new, label=label, copy_of=copy_of, write=write, server=server)
#
#     return id_new


def add_edge_spar(G, u, v, weight, K_min=2):
    # G.add_weighted_edges_from([(u, v, weight)])
    # check if: bother masters are on the same partition OR u has a replica on v's partition OR v has a replica on u's partition
    if G.nodes[u]["server"] != G.nodes[v]["server"]:
        if Utils.has_local_replica(G, u, v) and Utils.has_local_replica(G, v, u):
            # do noting
            pass

        else:
            #  Choose best configuration among the 3
            slave_replica = list(key for key in G.nodes if G.nodes[key]["copy_of"]!=-1)  # get slave replica only
            # print(slave_replica)

            #  config 1: status quo
            do_replica_for = [0, 0]
            if not Utils.has_local_replica(G, u, v):
                do_replica_for[0] = 1
            if not Utils.has_local_replica(G, v, u):
                do_replica_for[1] = 1
            cost_config_1 = sum(do_replica_for) + len(slave_replica)

            # config 2: the master of u go to v's master partition
            u_orign_partition = G.nodes[u]["server"]
            v_orign_partition = G.nodes[v]["server"]

            # id_new = Utils.get_largest_ID(G) + 1
            # add_node_spar(G, id_new, label=G.nodes[u]["label"], write=0, copy_of=u, server=G.nodes[u]["server"])  # create new slave replica on the current partition
            # G.nodes[u]["server"] = v_orign_partition  # move master replica
            u_neighbours_inside = list(x for x in G.neighbors(u) if G.nodes[x]["server"] == G.nodes[u]["server"])
            u_neighbours_outside = list(x for x in G.neighbors(u) if G.nodes[x]["server"] != G.nodes[u]["server"])
            u_neighbours_replica_to_delete = list()
            u_neighbours_to_replicate = u_neighbours_inside.copy()

            for neighbour_id_outside in u_neighbours_outside:
                to_delete = True
                for neighbour_id_inside in u_neighbours_inside:
                    if G.has_edge(neighbour_id_inside, neighbour_id_outside):  # this outside neighbour has another neighbour from the same partition as u, do not delete its replica
                        to_delete = False
                # check if there will still at least k replica for this node
                if to_delete:
                    to_delete = Utils.get_nb_replicas(G, neighbour_id_outside) > K_min
                if to_delete:
                    tmp = list(x for x in G.nodes if G.nodes[x]["copy_of"] == neighbour_id_outside and G.nodes[x]["server"] == G.nodes[u]["server"])
                    u_neighbours_replica_to_delete.append(tmp[0])

            # print("u_neighbours_inside", u_neighbours_inside)
            # print("u_neighbours_outside", u_neighbours_outside)
            # print("u_neighbours_to_replicate", u_neighbours_to_replicate)
            # print("u_neighbours_replica_to_delete", u_neighbours_replica_to_delete)

            for key in G.nodes:
                if G.nodes[key]["copy_of"] in u_neighbours_inside and G.nodes[key]["server"] == G.nodes[v]["server"] and G.nodes[key]["copy_of"] in u_neighbours_inside:
                    u_neighbours_to_replicate.remove(G.nodes[key]["copy_of"])

            for neighbour_id in u_neighbours_to_replicate:
                id_new = Utils.get_largest_ID(G) + 1
                # add_node_spar(G, id_new, label=G.nodes[neighbour_id]["label"], write=0, copy_of=neighbour_id, server=G.nodes[v]["server"])

            cost_config_2 = len(u_neighbours_to_replicate) - len(u_neighbours_replica_to_delete) + len(slave_replica) + (len(u_neighbours_inside)>0)  # the last term is for u to replicate itself on its old partition

            # config 3: the master of v go to u's master partition
            # id_new = Utils.get_largest_ID(G) + 1
            # add_node_spar(G, id_new, label=G.nodes[v]["label"], write=0, copy_of=v, server=G.nodes[v]["server"])
            # G.nodes[v]["server"] = u_orign_partition
            v_neighbours_inside = list(x for x in G.neighbors(v) if G.nodes[x]["server"] == G.nodes[v]["server"])
            v_neighbours_outside = list(x for x in G.neighbors(v) if G.nodes[x]["server"] != G.nodes[v]["server"])
            v_neighbours_replica_to_delete = list()
            v_neighbours_to_replicate = v_neighbours_inside.copy()

            for neighbour_id_outside in v_neighbours_outside:
                to_delete = True
                for neighbour_id_inside in v_neighbours_inside:
                    if G.has_edge(neighbour_id_inside,
                                  neighbour_id_outside):  # this outside neighbour has another neighbour from the same partition as u, do not delete its replica
                        to_delete = False
                # check if there will still at least k replica for this node
                if to_delete:
                    to_delete = Utils.get_nb_replicas(G, neighbour_id_outside) > K_min
                if to_delete:
                    tmp = list(x for x in G.nodes if G.nodes[x]["copy_of"] == neighbour_id_outside and G.nodes[x]["server"] == G.nodes[v]["server"])
                    v_neighbours_replica_to_delete.append(tmp[0])

            # print("\nv_neighbours_inside", v_neighbours_inside)
            # print("v_neighbours_outside", v_neighbours_outside)
            # print("v_neighbours_to_replicate", v_neighbours_to_replicate)
            # print("v_neighbours_replica_to_delete", v_neighbours_replica_to_delete)

            for key in G.nodes:
                if G.nodes[key]["copy_of"] in v_neighbours_inside and G.nodes[key]["server"] == G.nodes[u]["server"] and G.nodes[key]["copy_of"] in v_neighbours_inside:
                    v_neighbours_to_replicate.remove(G.nodes[key]["copy_of"])

            for neighbour_id in v_neighbours_to_replicate:
                id_new = Utils.get_largest_ID(G) + 1
                # add_node_spar(G, id_new, label=G.nodes[neighbour_id]["label"], write=0, copy_of=neighbour_id, server=G.nodes[u]["server"])

            cost_config_3 = len(v_neighbours_to_replicate) - len(v_neighbours_replica_to_delete) + len(slave_replica) + (len(v_neighbours_inside)>0)  # the last term is for v to replicate itself on its old partition

            # print("\ncost_config", cost_config_1, cost_config_2, cost_config_3)

            # expected new balance
            expected_new_load_config1 = G.graph["load"].copy()
            expected_new_load_config2 = G.graph["load"].copy()
            expected_new_load_config2[u_orign_partition] -= 1
            expected_new_load_config2[v_orign_partition] += 1
            expected_new_load_config3 = G.graph["load"].copy()
            expected_new_load_config3[v_orign_partition] -= 1
            expected_new_load_config3[u_orign_partition] += 1

            ratio_load_config1 = (max(expected_new_load_config1)-min(expected_new_load_config1))/sum(expected_new_load_config1)
            ratio_load_config2 = (max(expected_new_load_config2)-min(expected_new_load_config2))/sum(expected_new_load_config2)
            ratio_load_config3 = (max(expected_new_load_config3)-min(expected_new_load_config3))/sum(expected_new_load_config3)

            # print("expected_new_load 1", expected_new_load_config1, ratio_load_config1)
            # print("expected_new_load 2", expected_new_load_config2, ratio_load_config2)
            # print("expected_new_load 3", expected_new_load_config3, ratio_load_config3)

            do_config = Utils.choose_best_config(cost_config_1, cost_config_2, cost_config_3, ratio_load_config1, ratio_load_config2, ratio_load_config3)
            if do_config == 0:
                G.add_weighted_edges_from([(u, v, weight)])
                if do_replica_for[0]:  # create replica for u on v's partition
                    id_new = Utils.get_largest_ID(G) + 1
                    add_node_spar(G, id_new, label=G.nodes[u]["label"], write=0, copy_of=u, server=G.nodes[v]["server"])
                if do_replica_for[1]:  # create replica for v on u's partition
                    id_new = Utils.get_largest_ID(G) + 1
                    add_node_spar(G, id_new, label=G.nodes[v]["label"], write=0, copy_of=v, server=G.nodes[u]["server"])

            elif do_config == 1:
                # 1. replicate
                for key in u_neighbours_to_replicate:
                    id_new = Utils.get_largest_ID(G) + 1
                    add_node_spar(G, id_new, label=G.nodes[key]["label"], write=0, copy_of=key, server=G.nodes[v]["server"])
                    # print("adding node", key, "with id", id_new)

                # 2. delete unnecessary replicas
                for key in u_neighbours_replica_to_delete:
                    G.remove_node(key)

                # 3. move master replica and create new slave replica on the current partition
                if len(u_neighbours_inside)>0:
                    id_new = Utils.get_largest_ID(G) + 1
                    add_node_spar(G, id_new, label=G.nodes[u]["label"], write=0, copy_of=u, server=G.nodes[u]["server"])
                G.nodes[u]["server"] = v_orign_partition  # move master replica
                G.graph["load"][u_orign_partition] -= 1
                G.graph["load"][v_orign_partition] += 1

            elif do_config == 2:
                # 1. replicate
                for key in v_neighbours_to_replicate:
                    id_new = Utils.get_largest_ID(G) + 1
                    add_node_spar(G, id_new, label=G.nodes[key]["label"], write=0, copy_of=key,
                                  server=G.nodes[u]["server"])

                # 2. delete unnecessary replicas
                for key in v_neighbours_replica_to_delete:
                    G.remove_node(key)

                # 3. move master replica and create new slave replica on the current partition
                if len(v_neighbours_inside)>0:
                    id_new = Utils.get_largest_ID(G) + 1
                    add_node_spar(G, id_new, label=G.nodes[v]["label"], write=0, copy_of=v, server=G.nodes[v]["server"])
                G.nodes[v]["server"] = u_orign_partition  # move master replica
                G.graph["load"][v_orign_partition] -= 1
                G.graph["load"][u_orign_partition] += 1
        # Do nothing beyond edge addition
        # G.add_weighted_edges_from([(u, v, weight)])

        # else:  # do noting
        #     pass


def add_node_spar(G, id_new, label, copy_of, write, server):
    G.add_node(id_new, label=label, copy_of=copy_of, write=write, server=server)
    if copy_of==-1:
        G.graph["load"][server] += 1


