import numpy as np
import networkx as nx
import Coarse

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

G = network  # Utils.to_undirected(network)
coarse_max = 2
xadj, adjncy, weight, match, cmap = Coarse.coarse(G, coarse_max)
nb_new_Vs = len(cmap[-1])

print("match", match)
print("cmap", cmap)
print("xadj", xadj)
print("adjncy", adjncy)
print("adjwgt", weight)
print("nb_new_Vs=", nb_new_Vs)







