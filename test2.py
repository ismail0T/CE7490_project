import networkx as nx
import metis

# # G = metis.example_networkx()
# pathhack = "/home/ismail/Dev/Ego_Facebook"
# G = nx.read_edgelist("%s/facebook_combined.txt" % (pathhack,), create_using = nx.Graph(), nodetype=int)
import Utils

network = nx.Graph()
network.add_node(1, write="20")
network.add_node(2, write="40")
network.add_node(3, write="25")
network.add_node(4, write="30")
network.add_node(5, write="60")
network.add_node(6, write="30")
network.add_node(7, write="40")

network.add_weighted_edges_from([(1, 2, 45)])
network.add_weighted_edges_from([(1, 3, 65)])
network.add_weighted_edges_from([(1, 4, 65)])
network.add_weighted_edges_from([(1, 6, 80)])
network.add_weighted_edges_from([(4, 3, 70)])
network.add_weighted_edges_from([(6, 2, 55)])
network.add_weighted_edges_from([(2, 3, 40)])
network.add_weighted_edges_from([(2, 7, 60)])
network.add_weighted_edges_from([(3, 5, 75)])


G = network

# G = metis.example_networkx()
(edgecuts, parts) = metis.part_graph(G, 2)

print("parts", parts)

colors = ['red','blue','green']
for i, p in enumerate(parts):
    G.node[i+1]['color'] = colors[p]

print("edgecuts",edgecuts)
# for i, p in enumerate(parts):
#     print(i, p.node[i])
for key in list(G.node):
    print(key, G.node[key])

# for (u, v, wt) in G.edges.data('weight'):
#     print(u, v, wt)
#
# nx.nx_pydot.write_dot(G, 'example.dot')