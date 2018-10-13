"""
Graph coloring
"""

GRAPH1 = {0: set([1, 2]),
          1: set([0, 2]),
          2: set([0, 1])}

GRAPH2 = {0: set([1, 2, 3]),
          1: set([0, 2, 3]),
          2: set([0, 1, 3]),
          3: set([0, 1, 2])}

GRAPH3 = {0: set([1, 2, 4, 5]),
          1: set([0, 2, 3, 5]),
          2: set([0, 1, 3, 4]),
          3: set([1, 2, 4, 5]),
          4: set([0, 2, 3, 5]),
          5: set([0, 1, 3, 4])}

GRAPH4 = {1: set([2, 8]),
          2: set([1, 3, 4, 6, 8]), 
          3: set([2, 4]), 
          4: set([2, 3, 5, 6, 8]), 
          5: set([4, 6]), 
          6: set([2, 4, 5, 7, 8]), 
          7: set([6, 8]), 
          8: set([1, 2, 4, 6, 7])}

def subsets(s):
    """
    Generate all subsets of s.
    """
    res = []
    res.append(set([]))
    for elem in s:
        n = len(res)
        for idx in range(n):
            temp = list(res[idx])
            temp.append(elem)
            res.append(set(temp))
    return res

def no_edges(graph, nodes):
    """
    Return whether there are edges between nodes in graph.
    """
    for node in nodes:
        for neighbor in graph[node]:
            if neighbor in nodes:
                return False
    return True

def three_colorable(graph):
    """
    Return whether the graph is 3-colorable.
    """
    nodes = set(graph.keys())
    nodes_set = subsets(nodes)
    for red in nodes_set:
        if no_edges(graph, red):
            remain_nodes = nodes.difference(red)
            remain_nodes_set = subsets(remain_nodes)
            for green in remain_nodes_set:
                if no_edges(graph, green):
                    blue = nodes.difference(red.union(green))
                    if no_edges(graph, blue):
                        return True
    return False

print three_colorable(GRAPH1)
print three_colorable(GRAPH2)
print three_colorable(GRAPH3)
print three_colorable(GRAPH4)