import facebook, twitter

# load the network
my_graph = facebook.load_network()

print(my_graph.order())  # number of nodes
print(my_graph.size())   # number of edges

# Look at a node's features
print("feature: ", my_graph.nodes[0]['features'])

# 0: feature not present for this user
# 1: user does not have this feature
# 2: user does have this feature

# look at the features of the whole network
print("matrix", facebook.feature_matrix())


