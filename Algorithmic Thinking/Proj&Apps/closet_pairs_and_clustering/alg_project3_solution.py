"""
Project 3 - Closest pairs and clustering algorithms
"""

import math
import alg_cluster

def slow_closest_pair(cluster_list):
    """
    Brute-force closest pair method.
    """
    (dist, idx1, idx2) = tuple([float('inf'), -1, -1])
    for idxa in range(len(cluster_list)):
        for idxb in range(idxa + 1, len(cluster_list)):
            if cluster_list[idxa].distance(cluster_list[idxb]) < dist:
                dist = cluster_list[idxa].distance(cluster_list[idxb])
                idx1, idx2 = idxa, idxb
    return (dist, idx1, idx2)

def fast_closest_pair(cluster_list):
    """
    Divide-and-conquer closest pair method.
    """
    cluster_list.sort(key = lambda cluster : cluster.horiz_center())
    if len(cluster_list) <= 3:
        return slow_closest_pair(cluster_list)
    mid = len(cluster_list) / 2
    (dist_left, idx1_left, idx2_left) = fast_closest_pair(cluster_list[:mid])
    (dist_right, idx1_right, idx2_right) = fast_closest_pair(cluster_list[mid:])
    if dist_left < dist_right:
        (dist, idx1, idx2) = (dist_left, idx1_left, idx2_left)
    else:
        (dist, idx1, idx2) = (dist_right, idx1_right + mid, idx2_right + mid)
    horiz_center = (cluster_list[mid - 1].horiz_center() + cluster_list[mid].horiz_center()) / 2.0
    (dist_strip, idx1_strip, idx2_strip) = closest_pair_strip(cluster_list, horiz_center, dist)
    if dist_strip < dist:
        return (dist_strip, idx1_strip, idx2_strip)
    return (dist, idx1, idx2)

def closest_pair_strip(cluster_list, horiz_center, half_width):
    """
    Helper function for divide-and-conquer closest pair method.
    """
    cluster_strip = [idx for idx in range(len(cluster_list)) if abs(cluster_list[idx].horiz_center() - horiz_center) < half_width]
    cluster_strip.sort(key = lambda idx : cluster_list[idx].vert_center())
    (dist, idx1, idx2) = tuple([float('inf'), -1, -1])
    num_cluster = len(cluster_strip)
    for idxa in range(num_cluster - 1):
        for idxb in range(idxa + 1, min(idxa + 4, num_cluster)):
            if cluster_list[cluster_strip[idxa]].distance(cluster_list[cluster_strip[idxb]]) < dist:
                dist = cluster_list[cluster_strip[idxa]].distance(cluster_list[cluster_strip[idxb]])
                idx1 = min(cluster_strip[idxa], cluster_strip[idxb])
                idx2 = max(cluster_strip[idxa], cluster_strip[idxb])
    return (dist, idx1, idx2)

def hierarchical_clustering(cluster_list, num_clusters):
    """
    Hierarchical clustering.
    """
    while len(cluster_list) > num_clusters:
        (dummy_dist, idx1, idx2) = fast_closest_pair(cluster_list)
        cluster_list[idx2].merge_clusters(cluster_list[idx1])
        cluster_list.remove(cluster_list[idx1])
    return cluster_list

def kmeans_clustering(cluster_list, num_clusters, num_iterations):
    """
    K-means clustering.
    """
    cluster_copy = [cluster.copy() for cluster in cluster_list]
    cluster_copy.sort(key = lambda cluster : cluster.total_population(), reverse = True)
    centers = [cluster_copy[idx].copy() for idx in range(num_clusters)]
    for dummy_idx in range(num_iterations):
        clusters = [alg_cluster.Cluster(set([]), 0, 0, 0, 0) for dummy in range(num_clusters)]
        for idx in range(len(cluster_copy)):
            center_idx = -1
            center_dist = float('inf')
            for cidx in range(num_clusters):
                if cluster_copy[idx].distance(centers[cidx]) < center_dist:
                    center_dist = cluster_copy[idx].distance(centers[cidx])
                    center_idx = cidx
            clusters[center_idx].merge_clusters(cluster_copy[idx])
        for idx in range(num_clusters):
            centers[idx] = clusters[idx]
    return centers

# The following codes are added for the application module.

import gc
import time
import random
import matplotlib.pyplot as plt

def gen_random_clusters(num_clusters):
    """
    Generate specified number of random clusters
    with centers lie within the square with corners
    (+1, +1), (+1, -1), (-1, -1), (-1, +1).
    """
    cluster_list = []
    for idx in range(num_clusters):
        horiz_center = random.uniform(-1, 1)
        vert_center = random.uniform(-1, 1)
        cluster_list.append(alg_cluster.Cluster(set([]), horiz_center, vert_center, 0, 0))
    return cluster_list

def record_slow_fast_times():
    """
    Record running times for slow_closest_pair() and
    fast_closest_pair().
    """
    gc.disable()
    num_clusters = range(2, 201)
    slow_times = []
    fast_times = []
    for num_cluster in num_clusters:
        clusters = gen_random_clusters(num_cluster)
        start = time.clock()
        slow_closest_pair(clusters)
        finish = time.clock()
        slow_times.append(finish - start)
        start = time.clock()
        fast_closest_pair(clusters)
        finish = time.clock()
        fast_times.append(finish - start)
    gc.enable()
    return [num_clusters, slow_times, fast_times]

def plot_slow_fast_times():
    """
    Plot running times for slow_closest_pair() and
    fast_closest_pair().
    """
    [num_clusters, slow_times, fast_times] = record_slow_fast_times()
    plt.plot(num_clusters, slow_times, 'g', label = 'slow_closest_pair()')
    plt.plot(num_clusters, fast_times, 'b', label = 'fast_closest_pair()')
    plt.grid(True)
    plt.xlabel('Number of Random Clusters')
    plt.ylabel('Running Times')
    plt.legend(loc = 'upper right')
    plt.title('Timing Results for slow_closest_pair() and fast_closest_pair() using Desktop Python')
    plt.show()

if __name__ == '__main__':
    plot_slow_fast_times()
