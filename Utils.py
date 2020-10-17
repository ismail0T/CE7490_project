import networkx as nx
import numpy as np
from collections import defaultdict



def get_nb_replicas(G, key):
    return len(list(x for x in G.nodes if G.nodes[x]["copy_of"] == key))


def get_largest_ID(G):
    max_in_original_dataset = 5000
    l = list(x for x in G.nodes)
    l.append(max_in_original_dataset)
    return max(l) if l else 0


def to_undirected(G):
    UG = G.to_undirected()
    for node in G:
        for ngbr in nx.neighbors(G, node):
            if node in nx.neighbors(G, ngbr):
                UG.edges[node, ngbr]['weight'] = (
                        G.edges[node, ngbr]['weight'] + G.edges[ngbr, node]['weight']
                )
    return UG


def has_local_replica(G, u, v):
    server_u = G.nodes[u]['server']
    server_v = G.nodes[v]['server']

    if server_u == server_v:
        return True
    for key in list(G.nodes):
        if G.nodes[key]["copy_of"] == u and G.nodes[key]["server"] == server_v:
            return True
    # print("no replica found for", u, "on", v)
    # print("server_u", server_u, "server_v", server_v)

    return False


def total_read(G):
    total=0
    for (u, v, wt) in G.edges.data('weight'):
        if not has_local_replica(G, u, v) and u != G.nodes[v]['copy_of']:
            total += wt
    print("total_read", total)
    return total


def total_write(G):
    total=0
    for (u, v, wt) in G.edges.data('weight'):
        if u == G.nodes[v]['copy_of']:
            total += wt
    print("total_write", total)
    return total


def add_node_std(G, copy_of, server):
    id_new = get_largest_ID(G)+ 1
    G.add_node(id_new, copy_of=copy_of, write=0, server=server)

    return id_new


def choose_best_config(cost_config_1, cost_config_2, cost_config_3, ratio_load_config1, ratio_load_config2, ratio_load_config3):
    best_cost = min(cost_config_1, cost_config_2, cost_config_3)
    second_best_cost = sorted((cost_config_1, cost_config_2, cost_config_3))[1]

    if cost_config_1 == best_cost:
        return 0
    else:
        best_load_ratio = min(ratio_load_config1, ratio_load_config2, ratio_load_config3)
        if cost_config_3 == best_cost:
            if ratio_load_config3 == best_load_ratio:
                return 2
            elif second_best_cost == cost_config_2 and ratio_load_config2 == best_load_ratio:
                return 1
            else:
                return 0
        else:
            if cost_config_2 == best_cost:
                if ratio_load_config2 == best_load_ratio:
                    return 1
                elif second_best_cost == cost_config_3 and ratio_load_config3 == best_load_ratio:
                    return 2
                else:
                    return 0


def computeReadWeight(rank):
    beta = 697.4468225
    alpha = -0.71569687
    read_weight_nid = beta * (rank ** alpha)
    return read_weight_nid


def add_weights(G):
    NeighbourCount = {}

    for nid in G.nodes:
        if nid not in NeighbourCount.keys():
            NeighbourCount[nid] = 0
        for neighbor_id in G.neighbors(nid):
            NeighbourCount[nid] = NeighbourCount[nid] + 1

    NeighbourCount_Sorted = sorted(NeighbourCount.items(), key=lambda NeighbourCount: NeighbourCount[1], reverse=True)

    # Adjacent users can have same number of friends
    # Hence multiple users can have same rank
    rank_nid_distribution = {}  # should integrate NID, RANK
    previousConnections = NeighbourCount_Sorted[0][1]  # Holds the number of connections of previous user
    rank = 1  # rank of 1 is the highest rank

    for i in range(G.order()):  # hard-coding the number of users here
        # get the nid at the {i}th position
        nid = NeighbourCount_Sorted[i][0]

        if previousConnections == NeighbourCount_Sorted[i][1]:  # NeighbourCount_Sorted [i] [1] spits out connections
            if nid not in rank_nid_distribution.keys():
                rank_nid_distribution[nid] = rank
        if previousConnections > NeighbourCount_Sorted[i][1]:
            previousConnections = NeighbourCount_Sorted[i][1]
            if nid not in rank_nid_distribution.keys():
                rank = rank + 1
                rank_nid_distribution[nid] = rank

    for nid in G.nodes:
        Neighbor_count = len(list(G.neighbors(nid)))
        nid_rank = rank_nid_distribution[nid]
        total_read_weight = computeReadWeight(nid_rank)
        nid_r_weight = int(total_read_weight / Neighbor_count) + 1
        # nid_r_weight = 1
        writeWeight = nid_r_weight * 10
        G.nodes[nid]["write"] = writeWeight

        for neighbor_id in G.neighbors(nid):

            G.add_weighted_edges_from([(nid, neighbor_id, nid_r_weight)])

    return G


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


def spar_inter_server_cost(dict_replicas):
    cost = 0
    for node_id, servers in dict_replicas.items():
        cost += len(servers)

    return cost


def spar_inter_server_traffic(G_dict, G_servers, G_replica):
    cost = 0
    for u in G_dict:
        for v in G_dict[u]["neighbors"]:
            u_orign_partition = G_servers[u]
            v_orign_partition = G_servers[v]
            if u_orign_partition != v_orign_partition:
                if u_orign_partition in G_replica[v] and v_orign_partition in G_replica[u]:
                    cost += 0
                else:
                    cost += int(G_dict[u]["neighbors"][v])

    return cost / 2


def rp_inter_server_traffic(G_dict, G_servers):
    cost = 0
    for u in G_dict:
        for v in G_dict[u]["neighbors"]:
            u_orign_partition = G_servers[u]
            v_orign_partition = G_servers[v]
            if u_orign_partition != v_orign_partition:
                cost += int(G_dict[u]["neighbors"][v])

    return cost / 2

