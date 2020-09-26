import random

import DS
import DS_SPAR
import Utils
import facebook, twitter
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
import sys

# # load the network
# my_graph = facebook.load_network()
#
# print(my_graph.order())  # number of nodes
# print(my_graph.size())   # number of edges
#
# # Look at a node's features
# print("feature: ", my_graph.nodes[0]['features'])
#
# # 0: feature not present for this user
# # 1: user does not have this feature
# # 2: user does have this feature
#
# # look at the features of the whole network
# print("matrix", facebook.feature_matrix())

import nxmetis



# network = nx.DiGraph()
# network.add_node(1, write="20")
# network.add_node(2, write="40")
# network.add_node(3, write="25")
# network.add_node(4, write="30")
# network.add_node(5, write="60")
# network.add_node(6, write="30")
# network.add_node(7, write="40")
#
# print("NB nodes: ", network.order())
#
# network.add_weighted_edges_from([(1, 2, 20), (2, 1, 25)])
# network.add_weighted_edges_from([(1, 3, 25), (3, 1, 40)])
# network.add_weighted_edges_from([(1, 4, 20), (4, 1, 45)])
# network.add_weighted_edges_from([(1, 6, 30), (6, 1, 50)])
# network.add_weighted_edges_from([(4, 3, 50), (3, 4, 20)])
# network.add_weighted_edges_from([(6, 2, 30), (2, 6, 25)])
# network.add_weighted_edges_from([(2, 3, 30), (3, 2, 10)])
# network.add_weighted_edges_from([(2, 7, 40), (7, 2, 20)])
# network.add_weighted_edges_from([(3, 5, 30), (5, 3, 45)])



# network = nx.DiGraph()
# attrs = {1: {"label": "A", "write": 10, "server": 1},
#          2: {"label": "B", "write": 20, "server": 1},
#          3: {"label": "C", "write": 30, "server": 1},
#          4: {"label": "D", "write": 80, "server": 1}}

# nx.set_node_attributes(network, attrs)

# network.add_node(1, label="A", copy_of=-1, write=10, server=0)
# network.add_node(2, label="B", copy_of=-1, write=20, server=0)
# network.add_node(3, label="C", copy_of=-1, write=30, server=0)
# network.add_node(4, label="D", copy_of=-1, write=80, server=0)
#
# network.add_weighted_edges_from([(1, 3, 90), (3, 1, 25)])
# network.add_weighted_edges_from([(1, 4, 100), (4, 1, 20)])
# network.add_weighted_edges_from([(2, 4, 5), (4, 2, 15)])
# network.add_weighted_edges_from([(3, 4, 10), (4, 3, 20)])

# print(dict(network.out_degree(weight='weight')))


network = nx.DiGraph()
nb_servers = 3
network.graph["load"] = np.zeros(nb_servers)

DS_SPAR.add_node_spar(network, 1, label="A", copy_of=-1, write=10, server=0)
DS_SPAR.add_node_spar(network, 2, label="B", copy_of=-1, write=20, server=0)
DS_SPAR.add_node_spar(network, 3, label="C", copy_of=-1, write=30, server=0)
DS_SPAR.add_node_spar(network, 4, label="D", copy_of=-1, write=80, server=0)
DS_SPAR.add_node_spar(network, 5, label="E", copy_of=-1, write=80, server=1)
DS_SPAR.add_node_spar(network, 6, label="F", copy_of=-1, write=80, server=2)

DS_SPAR.add_node_spar(network, 10, label="D", copy_of=5, write=80, server=0)
DS_SPAR.add_node_spar(network, 11, label="D", copy_of=1, write=80, server=1)
DS_SPAR.add_node_spar(network, 12, label="D", copy_of=6, write=80, server=1)
DS_SPAR.add_node_spar(network, 13, label="D", copy_of=5, write=80, server=2)

network.add_weighted_edges_from([(1, 2, 90)])
network.add_weighted_edges_from([(1, 3, 90)])
network.add_weighted_edges_from([(1, 4, 90)])
network.add_weighted_edges_from([(1, 5, 90)])
network.add_weighted_edges_from([(5, 6, 90)])



G = Utils.to_undirected(network)


# for n, nbrs in G.adj.items():
#    for nbr, eattr in nbrs.items():
#        wt = eattr['weight']
#        print(f"({n}, {nbr}, {wt:.3})")

# print(5, [x for x in G.neighbors(5)])
# print(6, [x for x in G.neighbors(6)])

# for (u, v, wt) in G.edges.data('weight'):
#     print(u, v, wt)

# for key in list(H.nodes):
#     print(key, H.nodes[key])
# print(1, network.nodes[1])

print(G.graph)


DS_SPAR.add_edge_spar(G, 1, 6, 10)
# for key in list(G.nodes):
#     print(key, G.nodes[key])


print(G.graph)

# Utils.total_read(network)
# Utils.total_write(network)



# DS.random_partition(network)
# DS.selective_replicate(network)
# Utils.total_read(network)
# Utils.total_write(network)
