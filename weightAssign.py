import subprocess
import numpy as np
import networkx as nx
import matplotlib as plt
from numpy import random

# G = nx.read_edgelist("facebook_combined.txt", create_using=nx.Graph(), nodetype=int).to_directed()

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

G = network
# beta and alpha are parameters that fit the dataset into a Zipfs Dist.
def computeReadWeight(rank):
    beta = 697.4468225
    alpha = -0.71569687
    read_weight_nid = beta * (rank ** alpha)
    return read_weight_nid


def computeRank(nid):
    return rank_nid_distribution[nid]


# NeighbourCount contains the number of edges(friends) a node(user) has in descending order.
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

for i in range(G.order()):  # hardcoding the number of users here

    #get the nid at the {i}th position
    nid = NeighbourCount_Sorted[i][0]
    
    if previousConnections == NeighbourCount_Sorted[i][1]:  # NeighbourCount_Sorted [i] [1] spits out connections
        if nid not in rank_nid_distribution.keys():
            rank_nid_distribution[nid] = rank
    if previousConnections > NeighbourCount_Sorted[i][1]:
        previousConnections = NeighbourCount_Sorted[i][1]
        if nid not in rank_nid_distribution.keys():
            rank = rank + 1
            rank_nid_distribution[nid] = rank

    
read_weight_nid_distribution = {}

for nid in G.nodes:
    # It is impossible to find write weight based on this dataset.
    # We need to assign write weights randomly or by a different strategy
    writeWeight = 3    
    G.nodes[nid]["write"] = writeWeight
    
    # First we need to compute how many friends a user(node) has
    Neighbor_count = len(list(G.neighbors(nid)))
    
    for neighbor_id in G.neighbors(nid):
        nid_rank = rank_nid_distribution[nid]
        nid_r_weight = computeReadWeight(nid_rank) / Neighbor_count
                
        G.add_weighted_edges_from([(nid, neighbor_id, nid_r_weight)])
        # print(nid_r_weight)


for n, nbrs in G.adj.items():
   for nbr, eattr in nbrs.items():
       wt = eattr['weight']

       print(f"({n}, {nbr}, {wt:.3})")






