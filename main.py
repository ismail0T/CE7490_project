import random

import DS
import DS_SPAR
import Utils
import facebook, twitter
import networkx as nx
import numpy as np
# import matplotlib.pyplot as plt
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

# import nxmetis



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
nb_partition_max = 3
network.graph["load"] = np.zeros(nb_partition_max)
network.graph["nb_partition_max"] = nb_partition_max
network.graph["k_min"] = 1

G = Utils.to_undirected(network)

print(G.graph["load"])


id_A = DS_SPAR.add_node_spar(G, Utils.get_largest_ID(G) + 1, label="A", copy_of=-1, write=10, server=-1)
id_B = DS_SPAR.add_node_spar(G, Utils.get_largest_ID(G) + 1, label="B", copy_of=-1, write=20, server=-1)
DS_SPAR.add_edge_spar(G, id_A, id_B, 10)
id_C = DS_SPAR.add_node_spar(G, Utils.get_largest_ID(G) + 1, label="C", copy_of=-1, write=30, server=-1)
DS_SPAR.add_edge_spar(G, id_A, id_C, 10)
id_D = DS_SPAR.add_node_spar(G, Utils.get_largest_ID(G) + 1, label="D", copy_of=-1, write=80, server=-1)
DS_SPAR.add_edge_spar(G, id_A, id_D, 10)
id_E = DS_SPAR.add_node_spar(G, Utils.get_largest_ID(G) + 1, label="E", copy_of=-1, write=80, server=-1)
DS_SPAR.add_edge_spar(G, id_A, id_E, 10)
id_F = DS_SPAR.add_node_spar(G, Utils.get_largest_ID(G) + 1, label="F", copy_of=-1, write=80, server=-1)

DS_SPAR.add_edge_spar(G, id_E, id_F, 10)
DS_SPAR.add_edge_spar(G, id_A, id_F, 10)

# DS_SPAR.add_node_spar(G, 10, label="D", copy_of=5, write=80, server=-1)
# DS_SPAR.add_node_spar(G, 11, label="D", copy_of=1, write=80, server=-1)
# DS_SPAR.add_node_spar(G, 12, label="D", copy_of=6, write=80, server=-1)
# DS_SPAR.add_node_spar(G, 13, label="D", copy_of=5, write=80, server=-1)

# G.add_weighted_edges_from([(1, 2, 90)])
# G.add_weighted_edges_from([(1, 3, 90)])
# G.add_weighted_edges_from([(1, 4, 90)])
# G.add_weighted_edges_from([(1, 5, 90)])
# G.add_weighted_edges_from([(5, 6, 90)])


# DS_SPAR.add_edge_spar(G, 1, 6, 10)
for key in list(G.nodes):
    print(key, G.nodes[key])


print(G.graph["load"])

# Utils.total_read(network)
# Utils.total_write(network)



# DS.random_partition(network)
# DS.selective_replicate(network)
# Utils.total_read(network)
# Utils.total_write(network)
