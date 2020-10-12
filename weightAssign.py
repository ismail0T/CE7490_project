import subprocess
import numpy as np
import networkx as nx
import matplotlib as plt
from numpy import random

G = nx.read_edgelist("facebook_combined.txt", create_using=nx.Graph(), nodetype=int).to_directed()

for nid in G.nodes:
    
    #find writeWeight for node nid
    # Need a zipfs function
    writeWeight = 3    
    G.nodes [nid] ["write"] = writeWeight
    
    #now we proceed to assign the read weight for each neighbour
    for neighbor_id in G.neighbors(nid):
        #find readWeight for NID=key from NID=v
        readWeight = 4
        
        #args are from NID-1 to NID-2, the weight, multiple assignments possible.
        #FG.add_weighted_edges_from([(1, 2, 0.125), (1, 3, 0.75), (2, 4, 1.2), (3, 4, 0.375)])
        G.add_weighted_edges_from([(nid, neighbor_id, readWeight)])

#beta and alpha are parameters that fit the dataset into a Zipfs Dist.
def computeReadWeight(rank) :
    beta = 697.4468225
    alpha = -0.71569687
    read_weight_nid = beta * ( rank ** alpha)
    return read_weight_nid

def computeRank (nid):
    return rank_nid_distribution[nid]


# NeighbourCount contains the number of edges(friends) a node(user) has in decending order.
NeighbourCount = {}

for nid in G.nodes:
    if nid not in NeighbourCount.keys():
        NeighbourCount[nid] = 0
    for neighbor_id in G.neighbors(nid):
        NeighbourCount [nid] = NeighbourCount [nid] + 1

NeighbourCount_Sorted = sorted(NeighbourCount.items(), key=lambda NeighbourCount: NeighbourCount[1], reverse=True) 

# Adjecent users can have same number of friends
# Hence multiple users can have same rank
rank_nid_distribution = {} #should integrate NID, RANK 
previousConnections = NeighbourCount_Sorted [0] [1] #Holds the number of connections of previous user
rank = 1 #rank of 1 is the highest rank
for i in range (4039): #hardcoding the number of users here
    
    #get the nid at the {i}th position
    nid = NeighbourCount_Sorted [i] [0]
    
    if previousConnections == NeighbourCount_Sorted [i] [1] : #NeighbourCount_Sorted [i] [1] spits out connections
        if nid not in rank_nid_distribution.keys():
            rank_nid_distribution [nid] = rank
    if previousConnections >  NeighbourCount_Sorted [i] [1] :
        previousConnections = NeighbourCount_Sorted [i] [1]
        if nid not in rank_nid_distribution.keys():
            rank = rank + 1
            rank_nid_distribution [nid] = rank

    
read_weight_nid_distribution = {}

for i in range (4039):
    # i will iterate through all NIDs
    nid_rank = computeRank (i)
    nid_weight= computeReadWeight(nid_rank)
    read_weight_nid_distribution [i] = nid_weight
