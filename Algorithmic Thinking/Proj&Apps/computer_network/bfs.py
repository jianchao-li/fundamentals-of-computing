"""
Project 2 - Connected components and graph resilience
Application 2 - Analysis of a computer network
"""

import gc
import time
import random
import matplotlib.pyplot as plt
from collections import deque

# Location for the network file
COMPUTER_NETWORK = 'G:/Resources/Courses/Algorithmic Thinking/Proj&Apps/computer_network/alg_rf7.txt'

# Types of attack
RANDOM_ATTACK = 0

def bfs_visited(ugraph, start_node):
    """
    Retursn all nodes that are visited by
    a BFS from start_node in ugraph.
    """
    to_visit = deque([start_node])
    visited = set([start_node])
    while len(to_visit) != 0:
        node = to_visit.popleft()
        for neigh in ugraph[node]:
            if neigh not in visited:
                visited.add(neigh)
                to_visit.append(neigh)
    return visited

def cc_visited(ugraph):
    """
    Returns all the connected components of
    ugraph.
    """
    remains = set(ugraph.keys())
    connected_comps = []
    while len(remains) != 0:
        node = random.choice(list(remains))
        connected_comp = bfs_visited(ugraph, node)
        connected_comps.append(connected_comp)
        for cc_node in connected_comp:
            remains.discard(cc_node)
    return connected_comps

def largest_cc_size(ugraph):
    """
    Returns the size of the largest connected
    component in ugraph.
    """
    largest_size = 0
    connected_comps = cc_visited(ugraph)
    for comp in connected_comps:
        if len(comp) > largest_size:
            largest_size = len(comp)
    return largest_size

def compute_resilience(ugraph, attack_order):
    """
    Compute the resilience of ugraph after removing
    nodes in attack_order.
    """
    resilience = [0] * (len(attack_order) + 1)
    resilience[0] = largest_cc_size(ugraph)
    for idx in range(len(attack_order)):
        del ugraph[attack_order[idx]]
        for node in ugraph.keys():
            ugraph[node].discard(attack_order[idx])
        resilience[idx + 1] = largest_cc_size(ugraph)
    return resilience

def er_random_graph(num_nodes, prob):
    """
    Generate random undirected graph of specified
    number of nodes and probability using the ER
    algorithm.
    """
    graph = {}
    for node in range(num_nodes):
        if node not in graph.keys():
            graph[node] = set([])
        for neigh in range(num_nodes):
            if neigh != node and random.random() <= prob:
                graph[node].add(neigh)
        for neigh in graph[node]:
            if neigh not in graph.keys():
                graph[neigh] = set([node])
            else:
                graph[neigh].add(node)
    return graph

def make_complete_ugraph(num_nodes):
    """
    Generate complete undirected graph with specified
    number of nodes.
    """
    ugraph = {}
    for node in range(num_nodes):
        neighbors = set([])
        for neigh in range(num_nodes):
            if neigh != node:
                neighbors.add(neigh)
        ugraph[node] = neighbors
    return ugraph

def upa_random_graph(num_nodes, num_neighbors):
    """
    Generate random undirected graphs of specified
    number of nodes and neighbors using the UPA
    algorithm.
    """
    graph = make_complete_ugraph(num_neighbors)
    candidates = [node for node in graph.keys() for dummy_idx in range(len(graph))]
    for node in range(num_neighbors, num_nodes):
        neighbors = set()
        for dummy_idx in range(num_neighbors):
            neighbors.add(random.choice(candidates))
        graph[node] = neighbors
        for neigh in neighbors:
            graph[neigh].add(node)
        candidates.append(node)
        for dummy_idx in range(len(neighbors)):
            candidates.append(node)
        candidates.extend(list(neighbors))
    return graph

def copy_graph(graph):
    """
    Return a copy of graph.
    """
    copy = {}
    for node in graph.keys():
        copy[node] = set(graph[node])
    return copy

def delete_node(ugraph, node):
    """
    Delete a node from an undirected graph.
    """
    neighbors = ugraph.pop(node)
    for neigh in neighbors:
        ugraph[neigh].remove(node)

def targeted_order(ugraph):
    """
    Compute a targeted attack order consisting
    of nodes of maximal degree.
    """
    copy = copy_graph(ugraph)
    order = []
    while len(copy) > 0:
        max_degree = -1
        for node in copy.keys():
            if len(copy[node]) > max_degree:
                max_degree = len(copy[node])
                target_node = node
        delete_node(copy, target_node)
        order.append(target_node)
    return order

def load_graph(file_name):
    """
    Load a graph from its file.
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

def node_count(graph):
    """
    Count number of nodes in graph.
    """
    return len(graph)

def edge_count(ugraph):
    """
    Count number of edges in undirected graph.
    """
    edges = 0
    for node in ugraph.keys():
        edges += len(ugraph[node])
    return edges / 2

def random_order(ugraph):
    """
    Ruturns nodes in random attack order.
    """
    nodes = ugraph.keys()
    random.shuffle(nodes)
    return nodes

def make_graphs():
    """
    Make the computer network, ER graph and UPA graph.
    """
    network = load_graph(COMPUTER_NETWORK)
    nodes = node_count(network)
    edges = edge_count(network)
    prob = float(edges) / (nodes * (nodes - 1))
    num_neighbors = int(edges / nodes) + 1
    er_graph = er_random_graph(nodes, prob)
    upa_graph = upa_random_graph(nodes, num_neighbors)
    return [network, er_graph, upa_graph]

def plot_random_resilience():
    """
    Plot curves of resilience after removing nodes
    randomly for the computer network, an ER graph
    and a UPA graph.
    """
    [network, er_graph, upa_graph] = make_graphs()
    num_remove_nodes = range(node_count(network) + 1)
    net_order = random_order(network)
    er_order = random_order(er_graph)
    upa_order = random_order(upa_graph)
    net_resilience = compute_resilience(network, net_order)
    er_resilience = compute_resilience(er_graph, er_order)
    upa_resilience = compute_resilience(upa_graph, upa_order)
    plt.plot(num_remove_nodes, net_resilience, 'r', label = 'Computer Network')
    plt.plot(num_remove_nodes, er_resilience, 'g', label = 'ER graph with p = 0.0020')
    plt.plot(num_remove_nodes, upa_resilience, 'b', label = 'UPA graph with m = 3')
    plt.grid(True)
    plt.xlabel('Number of Nodes Attacked Randomly')
    plt.ylabel('Network Resilience')
    plt.title('Network Resilience Curve Under Random Attack')
    plt.legend(loc = 'upper right')
    plt.show()

def fast_targeted_order(ugraph):
    """
    Fast version of targeted_order().
    """
    copy = copy_graph(ugraph)
    degrees = [set([]) for dummy_idx in xrange(len(ugraph))]
    for node in copy.keys():
        degrees[len(copy[node])].add(node)
    order = []
    for deg in range(len(ugraph) - 1, -1, -1):
        while len(degrees[deg]) != 0:
            node = degrees[deg].pop()
            for neigh in copy[node]:
                degrees[len(copy[neigh])].remove(neigh)
                degrees[len(copy[neigh]) - 1].add(neigh)
            order.append(node)
            delete_node(copy, node)
    return order

def time_targeted_order(nodes, num_neighbors):
    """
    Return the running time of targeted_order() and
    fast_targeted_order() under different number of
    nodes in the upa graph.
    """
    gc.disable()
    simple_timings = []
    fast_timings = []
    for num_nodes in nodes:
        upa_graph = upa_random_graph(num_nodes, num_neighbors)
        start = time.clock()
        simple_order = targeted_order(upa_graph)
        finish = time.clock()
        simple_timings.append(finish - start)
        start = time.clock()
        fast_order = fast_targeted_order(upa_graph)
        finish = time.clock()
        fast_timings.append(finish - start)
    gc.enable()
    return [simple_timings, fast_timings]

def compare_targeted_order():
    """
    Compare the running time of targeted_order()
    and fast_targeted_order().
    """
    nodes = range(10, 1000, 10)
    num_neighbors = 5
    [simple_timings, fast_timings] = time_targeted_order(nodes, num_neighbors)
    plt.plot(nodes, simple_timings, 'g', label = 'targeted_order()')
    plt.plot(nodes, fast_timings, 'b', label = 'fast_targeted_order()')
    plt.grid(True)
    plt.xlabel('Number of Nodes in UPA Graphs')
    plt.ylabel('Running Times')
    plt.legend(loc = 'upper right')
    plt.title('Timing Results for targeted_order() and fast_targeted_order() using Desktop Python')
    plt.show()

def plot_targeted_resilience():
    """
    Plot curves of resilience after targeted attack to the
    computer network, an ER graph and a UPA graph.
    """
    [network, er_graph, upa_graph] = make_graphs()
    num_remove_nodes = range(node_count(network) + 1)
    net_order = targeted_order(network)
    er_order = targeted_order(er_graph)
    upa_order = targeted_order(upa_graph)
    net_resilience = compute_resilience(network, net_order)
    er_resilience = compute_resilience(er_graph, er_order)
    upa_resilience = compute_resilience(upa_graph, upa_order)
    plt.plot(num_remove_nodes, net_resilience, 'r', label = 'Computer Network')
    plt.plot(num_remove_nodes, er_resilience, 'g', label = 'ER graph with p = 0.0020')
    plt.plot(num_remove_nodes, upa_resilience, 'b', label = 'UPA graph with m = 3')
    plt.grid(True)
    plt.xlabel('Number of Target Nodes Attacked')
    plt.ylabel('Network Resilience')
    plt.title('Network Resilience Curve Under Targeted Attack')
    plt.legend(loc = 'upper right')
    plt.show()

if __name__ == '__main__':
    # plot_random_resilience()
    compare_targeted_order()
    # plot_targeted_resilience()
