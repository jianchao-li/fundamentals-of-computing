"""
Example code for creating and visualizing
cluster of county-based cancer risk data

Note that you must download the file
http://www.codeskulptor.org/#alg_clusters_matplotlib.py
to use the matplotlib version of this code
"""

# Flavor of Python - desktop or CodeSkulptor
DESKTOP = True

import csv
import math
import random
import urllib2
import alg_cluster

# conditional imports
if DESKTOP:
    import alg_project3_solution      # desktop project solution
    import alg_clusters_matplotlib
else:
    #import userXX_XXXXXXXX as alg_project3_solution   # CodeSkulptor project solution
    import alg_clusters_simplegui
    import codeskulptor
    codeskulptor.set_timeout(30)


###################################################
# Code to load data tables

# URLs for cancer risk data tables of various sizes
# Numbers indicate number of counties in data table

DIRECTORY = "http://commondatastorage.googleapis.com/codeskulptor-assets/"
DATA_3108_URL = DIRECTORY + "data_clustering/unifiedCancerData_3108.csv"
DATA_896_URL = DIRECTORY + "data_clustering/unifiedCancerData_896.csv"
DATA_290_URL = DIRECTORY + "data_clustering/unifiedCancerData_290.csv"
DATA_111_URL = DIRECTORY + "data_clustering/unifiedCancerData_111.csv"


DATA_3108 = "./unifiedCancerData_3108.csv"
DATA_896 = "./unifiedCancerData_896.csv"
DATA_290 = "./unifiedCancerData_290.csv"
DATA_111 = "./unifiedCancerData_111.csv"


def load_data_table(data_url):
    """
    Import a table of county-based cancer risk data
    from a csv format file
    """
    data_file = urllib2.urlopen(data_url)
    data = data_file.read()
    data_lines = data.split('\n')
    print "Loaded", len(data_lines), "data points"
    data_tokens = [line.split(',') for line in data_lines]
    return [[tokens[0], float(tokens[1]), float(tokens[2]), int(tokens[3]), float(tokens[4])] 
            for tokens in data_tokens]

############################################################
# Code to load county-based cancer risk data from local files

def load_data_table_local(data_path):
    """
    Import a table of county-based cancer risk data
    from a local csv format file
    """
    data_table = []
    with open(data_path) as csv_f:
        csv_file = csv.reader(csv_f)
        headers = next(csv_file)
        for row in csv_file:
            data_table.append([row[0], float(row[1]), float(row[2]), int(row[3]), float(row[4])])
    return data_table


############################################################
# Code to create sequential clustering
# Create alphabetical clusters for county data

def sequential_clustering(singleton_list, num_clusters):
    """
    Take a data table and create a list of clusters
    by partitioning the table into clusters based on its ordering
    
    Note that method may return num_clusters or num_clusters + 1 final clusters
    """
    
    cluster_list = []
    cluster_idx = 0
    total_clusters = len(singleton_list)
    cluster_size = float(total_clusters)  / num_clusters
    
    for cluster_idx in range(len(singleton_list)):
        new_cluster = singleton_list[cluster_idx]
        if math.floor(cluster_idx / cluster_size) != \
           math.floor((cluster_idx - 1) / cluster_size):
            cluster_list.append(new_cluster)
        else:
            cluster_list[-1] = cluster_list[-1].merge_clusters(new_cluster)
            
    return cluster_list
                

def compute_distortion(cluster_list, data_table):
    """
    Code to compute the distortion of a clustering.
    """
    distortion = 0
    for cluster in cluster_list:
        distortion += cluster.cluster_error(data_table)
    return distortion


#####################################################################
# Code to load cancer data, compute a clustering and 
# visualize the results


def run_example():
    """
    Load a data table, compute a list of clusters and 
    plot a list of clusters

    Set DESKTOP = True/False to use either matplotlib or simplegui
    """
    #data_table = load_data_table(DATA_3108_URL)
    data_table = load_data_table_local(DATA_290)
    
    singleton_list = []
    for line in data_table:
        singleton_list.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))

    singleton_list_copy = [singleton.copy() for singleton in singleton_list]
        
    # cluster_list = sequential_clustering(singleton_list, 15)	
    # print "Displaying", len(cluster_list), "sequential clusters"

    hierarchical_distortions = []

    cluster_list = alg_project3_solution.hierarchical_clustering(singleton_list, 20)
    hierarchical_distortions.append(compute_distortion(cluster_list, data_table))
    for num_clusters in range(19, 5, -1):
        cluster_list = alg_project3_solution.hierarchical_clustering(cluster_list, num_clusters)
        hierarchical_distortions.append(compute_distortion(cluster_list, data_table))
    hierarchical_distortions.reverse()
    # print "Displaying", len(cluster_list), "hierarchical clusters"

    kmeans_distortions = []

    for num_clusters in range(6, 21):
        cluster_list = alg_project3_solution.kmeans_clustering(singleton_list_copy, num_clusters, 5)
        kmeans_distortions.append(compute_distortion(cluster_list, data_table))
    # print "Displaying", len(cluster_list), "k-means clusters"

    # code to compute distortion
    # distortion = compute_distortion(cluster_list, data_table)
    # print "distortion = " + str(distortion)
                
    # draw the clusters using matplotlib or simplegui
    # if DESKTOP:
        # alg_clusters_matplotlib.plot_clusters(data_table, cluster_list, True)
        #alg_clusters_matplotlib.plot_clusters(data_table, cluster_list, True)  #add cluster centers
    # else:
        # alg_clusters_simplegui.PlotClusters(data_table, cluster_list)   # use toggle in GUI to add cluster centers

    return [hierarchical_distortions, kmeans_distortions]

import matplotlib.pyplot as plt

if __name__ == '__main__':
    num_clusters = range(6, 21)
    [hierarchical_distortions, kmeans_distortions] = run_example()
    plt.plot(num_clusters, hierarchical_distortions, 'g', label = 'hierarchical clustering')
    plt.plot(num_clusters, kmeans_distortions, 'b', label = 'k-means clustering')
    plt.grid(True)
    plt.xlabel('Number of Output Clusters')
    plt.ylabel('Distortion of Output Clusters')
    plt.legend(loc= 'upper right')
    plt.title('Distortions of Two Clustering Methods on unifiedCancerData_290.csv')
    plt.show()




    





  
        






        




