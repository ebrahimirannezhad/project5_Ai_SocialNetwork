import gzip
import random
import urllib.request

import networkx as nx

# part 1
# Download the dataset
url = "https://snap.stanford.edu/data/soc-sign-epinions.txt.gz"
dataset_path = "soc-sign-epinions.txt.gz"
urllib.request.urlretrieve(url, dataset_path)

# Extract the dataset
with gzip.open(dataset_path, "rb") as file_in:
    with open("soc-sign-epinions.txt", "wb") as file_out:
        file_out.write(file_in.read())

# Read the dataset and generate the graph
graph = nx.read_edgelist("soc-sign-epinions.txt", create_using=nx.DiGraph(), nodetype=int, data=(('weight', int),))

# Print some basic information about the graph
print("Number of nodes:", graph.number_of_nodes())
print("Number of edges:", graph.number_of_edges())

##############################
##############################
##############################
##############################
##############################
# 47 Calculate the count and fraction of triads of each type in this network.

triads = nx.triadic_census(graph)

for triad_type, count in triads.items():
    fraction = count / sum(triads.values())
    print(f"Triad Type {triad_type}: Count={count}, Fraction={fraction}")

##############################
##############################
##############################
##############################
##############################
# 48 Calculate the fraction of positive and negative edges in the graph. Let the fraction
# of positive edges be p. Assuming that each edge of a triad will independently be
# assigned a positive sign with probability p and a negative sign with probability
# 1 − p, calculate the probability of each type of triad.

# Calculate the fraction of positive and negative edges
positive_edges = [edge for edge in graph.edges if graph.edges[edge]['weight'] == 1]
negative_edges = [edge for edge in graph.edges if graph.edges[edge]['weight'] == -1]
fraction_positive_edges = len(positive_edges) / len(graph.edges)
fraction_negative_edges = len(negative_edges) / len(graph.edges)

print("Fraction of positive edges:", fraction_positive_edges)
print("Fraction of negative edges:", fraction_negative_edges)

# Calculate the probability of each type of triad
triads = nx.triadic_census(graph)
total_triads = sum(triads.values())

triad_probabilities = {}
for triad_type, count in triads.items():
    probability = (fraction_positive_edges ** count['+'] * fraction_negative_edges ** count['-']) / (2 ** count['-+'])
    triad_probabilities[triad_type] = probability

for triad_type, probability in triad_probabilities.items():
    print("Triad Type", triad_type, ": Probability =", probability)


##############################
##############################
##############################
##############################
##############################
# 49 Now, analyse a simple generative model of signed networks by running simulations of the dynamic process on small networks in the following manner. Create a
# complete network on 10 nodes. For each edge, choose a sign with uniform probability. Run this dynamic process for a million iterations. Repeat this process 100 times.
# What fraction of these networks are balanced?

def is_balanced(graph):
    for node in graph.nodes:
        positive_neighbors = sum(1 for neighbor in graph.neighbors(node) if graph.edges[node, neighbor]['weight'] == 1)
        negative_neighbors = sum(1 for neighbor in graph.neighbors(node) if graph.edges[node, neighbor]['weight'] == -1)
        if positive_neighbors != negative_neighbors:
            return False
    return True


num_iterations = 1000000
num_repetitions = 20
num_balanced_networks = 0

for _ in range(num_repetitions):
    balanced = True
    for _ in range(num_iterations):
        graph = nx.complete_graph(10)
        for edge in graph.edges:
            sign = random.choice([-1, 1])
            graph.edges[edge]['weight'] = sign

        for _ in range(num_iterations):
            node1, node2 = random.choice(list(graph.edges))
            sign1 = graph.edges[node1, node2]['weight']
            sign2 = graph.edges[node2, node1]['weight']
            new_sign1 = random.choice([-1, 1])
            new_sign2 = random.choice([-1, 1])

            if sign1 == sign2:
                graph.edges[node1, node2]['weight'] = new_sign1
                graph.edges[node2, node1]['weight'] = new_sign1
            else:
                graph.edges[node1, node2]['weight'] = new_sign1
                graph.edges[node2, node1]['weight'] = new_sign2

            if not is_balanced(graph):
                balanced = False
                break
        if not balanced:
            break

    if balanced:
        num_balanced_networks += 1

fraction_balanced_networks = num_balanced_networks / num_repetitions
print("Fraction of balanced networks:", fraction_balanced_networks)
