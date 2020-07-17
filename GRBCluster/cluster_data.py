
import numpy as np
import os
import pickle
import  matplotlib.pyplot as plt 
from scipy.cluster.hierarchy import dendrogram, linkage
import sys


# changeable inputs
# choices are: euclid, corr, dtw, and norm (for manhattan)
matrix_type = 'norm'
no_buffer = False


# lots of recursion in clustering. need to set it higher
sys.setrecursionlimit(10000)


# parse in distance matrix
with open(os.path.join('data',matrix_type+'_matrix'+('_no_buffer' if no_buffer else '')+'.pkl'), 'rb') as f:
    distance_matrix = pickle.load(f)

# parse in burst list
with open(os.path.join('data',matrix_type+'_burst_list'+('_no_buffer' if no_buffer else '')+'.pkl'), 'rb') as f:
    burst_list = pickle.load(f)


# ensures there are no negative values in the distance matrix (obsolete)
distance_matrix = [0 if x < 0 else x for x in distance_matrix]


# build the cluster
Z = linkage(distance_matrix, 'average',optimal_ordering=True)

# plot the dendrogram
fig = plt.figure(figsize=(25, 10))
dn = dendrogram(Z, p=200, labels = burst_list, distance_sort='descending')
plt.title('Dendrogram of DTW Matrix')
plt.show()