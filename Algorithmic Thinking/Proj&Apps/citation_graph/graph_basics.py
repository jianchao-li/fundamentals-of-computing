"""
Project and Application of Module One
"""

import math
import random
import matplotlib.pyplot as plt

EX_GRAPH0 = {0: ([1, 2]),
             1: ([]),
             2: ([])}
EX_GRAPH1 = {0: ([1, 4, 5]),
             1: ([2, 6]),
             2: ([3]),
             3: ([0]),
             4: ([1]),
             5: ([2]),
             6: ([])}
EX_GRAPH2 = {0: ([1, 4, 5]),
             1: ([2, 6]),
             2: ([3, 7]),
             3: ([7]),
             4: ([1]),
             5: ([2]),
             6: ([]),
             7: ([3]),
             8: ([1, 2]),
             9: ([0, 3, 4, 5, 6, 7])}

CITATION_GRAPH = 'G:/Resources/Courses/Algorithmic Thinking/Proj&Apps/citation_graph/alg_phys-cite.txt'


def make_complete_graph(num_nodes):
    """
    Generate complete graphs of specidied number of nodes.
    """
    graph = {}
    for node in range(num_nodes):
        neighbors = set([])
        for neigh in range(num_nodes):
            if neigh != node:
                neighbors.add(neigh)
        graph[node] = neighbors
    return graph

def er_random_digraph(num_nodes, prob):
    """
    Generate random directed graphs of specified number of nodes and probability using the ER algorithm.
    """
    digraph = {}
    for node in range(num_nodes):
        neighbors = set([])
        for neigh in range(num_nodes):
            if neigh != node and random.random() <= prob:
                neighbors.add(neigh)
        digraph[node] = neighbors
    return digraph

def dpa_random_digraph(num_nodes, num_neighbors):
    """
    Generate random directed graphs of specified number of nodes and neighbours using the DPA algorithm.
    """
    digraph = make_complete_graph(num_neighbors)
    candidates = [node for node in digraph.keys() for dummy_idx in range(len(digraph))]
    for node in range(num_neighbors, num_nodes):
        neighbors = set()
        for dummy_idx in range(num_neighbors):
            neighbors.add(random.choice(candidates))
        digraph[node] = neighbors
        candidates.append(node)
        candidates.extend(list(neighbors))
    return digraph

def compute_in_degrees(digraph):
    """
    Compute in-degrees of directed graphs.
    """
    degrees = {}
    for node in digraph.keys():
        if not node in degrees.keys():
            degrees[node] = 0
        neighbors = digraph[node]
        for neigh in neighbors:
            if neigh in degrees.keys():
                degrees[neigh] += 1
            else:
                degrees[neigh] = 1
    return degrees

def compute_out_degrees(digraph):
    """
    Compute out-degrees of directed graphs.
    """
    degrees = {}
    for node in digraph.keys():
        degrees[node] = len(digraph[node])
    return degrees

def in_degree_distribution(digraph):
    """
    Compute in-degree distribution of directed graphs.
    """
    degrees = compute_in_degrees(digraph)
    distribution = {}
    for node in degrees.keys():
        degree = degrees[node]
        if degree in distribution.keys():
            distribution[degree] += 1
        else:
            distribution[degree] = 1
    return distribution

def load_graph(file_name):
    """
    Load graphs.
    """
    graph = {}
    graph_file = open(file_name, 'r')
    for line in graph_file:
        line = line.split()
        node = int(line[0])
        neighbors = set([])
        for neigh in line[1:]:
            neighbors.add(int(neigh))
        graph[node] = neighbors
    return graph

def run_app_q1():
    """
    Question 1 of Application of Module 1.
    """
    graph = load_graph(CITATION_GRAPH)
    distribution = in_degree_distribution(graph)
    for degree in distribution.keys():
        distribution[degree] /= float(len(graph))
    plt.loglog(distribution.keys(), distribution.values(), 'g^', basex=10, basey=10)
    plt.grid(True)
    plt.xlabel("In-Degrees")
    plt.ylabel("Normalized Fraction of Nodes")
    plt.title("LOG/LOG Point Plot of Normalized In-Degree Distribution of Citation Graph")
    plt.show()

def run_app_q2():
    """
    Question 2 of Application of Module 1.
    """
    digraph = er_random_digraph(1000, 0.4)
    distribution = in_degree_distribution(digraph)
    for degree in distribution.keys():
        distribution[degree] /= float(len(digraph))
    plt.plot(distribution.keys(), distribution.values(), 'g^')
    plt.grid(True)
    plt.xlabel("In-Degrees")
    plt.ylabel("Normalized Fraction of Nodes")
    plt.title("Linear Point Plot of Normalized In-Degree Distribution of Directed ER Graph")
    plt.show()

def run_app_q3():
    """
    Question 3 of Application of Module 1.
    """
    graph = load_graph(CITATION_GRAPH)
    num_nodes = len(graph)
    degrees = compute_out_degrees(graph)
    num_neighbors = int(math.ceil(sum(degrees.values()) / float(len(graph))))
    print "n =", num_nodes, "m =", num_neighbors
    return [num_nodes, num_neighbors]

def run_app_q4():
    """
    Question 4 of Application of Module 1.
    """
    num_nodes, num_neighbors = run_app_q3()
    digraph = dpa_random_digraph(num_nodes, num_neighbors)
    print len(digraph)
    distribution = in_degree_distribution(digraph)
    for degree in distribution.keys():
        distribution[degree] /= float(len(digraph))
    plt.loglog(distribution.keys(), distribution.values(), 'g^', basex=10, basey=10)
    plt.grid(True)
    plt.xlabel("In-Degrees")
    plt.ylabel("Normalized Fraction of Nodes")
    plt.title("LOG/LOG Point Plot of Normalized In-Degree Distribution of DPA Graph")
    plt.show()

if __name__ == '__main__':
    run_app_q4()
