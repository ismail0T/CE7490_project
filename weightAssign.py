import subprocess
import numpy as np
import networkx as nx
import Utils
from collections import defaultdict
import matplotlib as plt

G = nx.read_edgelist("facebook_combined.txt", create_using=nx.Graph(), nodetype=int).to_directed()

for key in G.nodes:
    #find writeWeight for NID=key
    writeWeight = 3
    G.nodes [key] ["write"] = writeWeight
    #now we proceed to assign the read weight for each neighbour
    for v in G.neighbors(key):
        #find readWeight for NID=key from NID=v
        readWeight = 4
        #args are from NID1 to NID2, weight.
        #G.nodes [(key)] ["read"] = writeWeight
        #G.add_weighted_edges_from([key,v,readWeight])
        G.add_weighted_edges_from([(key, v, readWeight)])  
