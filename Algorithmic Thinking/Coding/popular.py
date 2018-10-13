TEST_GRAPH0 = "./random10.txt"
TEST_GRAPH1 = "./random100.txt"
TEST_GRAPH2 = "./random1000.txt"
TEST_GRAPH3 = "./random10000.txt"

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

def average_degrees(graph):
    """
    Compute average degrees.
    """
    degrees = 0
    for node in graph.keys():
        degrees += len(graph[node])
    return degrees / len(graph.keys())

def compute_degrees(graph):
    """
    Compute degrees of nodes in graph.
    """
    degrees = {}
    for node in graph.keys():
        degrees[node] = len(graph[node])
    return degrees

def popular_nodes(graph):
    """
    Compute number of popular nodes in graphs.
    """
    # Compute average degrees
    popular = 0
    ave_deg = average_degrees(graph)
    degrees = compute_degrees(graph)
    for node in degrees:
        if degrees[node] > ave_deg:
            popular += 1
    return popular

if __name__ == '__main__':
    graph = load_graph(TEST_GRAPH0)
    print popular_nodes(graph)
    graph = load_graph(TEST_GRAPH1)
    print popular_nodes(graph)
    graph = load_graph(TEST_GRAPH2)
    print popular_nodes(graph)
    graph = load_graph(TEST_GRAPH3)
    print popular_nodes(graph)
