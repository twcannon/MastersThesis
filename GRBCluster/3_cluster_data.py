
import numpy as np
import os
import pickle
import  matplotlib.pyplot as plt 
from scipy.cluster.hierarchy import dendrogram, linkage
import sys
sys.setrecursionlimit(10000)

matrix_type = 'norm'
no_buffer = True

with open(os.path.join('data',matrix_type+'_matrix'+('_no_buffer' if no_buffer else '')+'.pkl'), 'rb') as f:
    distance_matrix = pickle.load(f)

with open(os.path.join('data',matrix_type+'_burst_list'+('_no_buffer' if no_buffer else '')+'.pkl'), 'rb') as f:
    burst_list = pickle.load(f)

# distance_matrix = 1/np.asarray(distance_matrix)

distance_matrix = [0 if x < 0 else x for x in distance_matrix]

# print(distance_matrix)

# Z = linkage(distance_matrix, 'single')
Z = linkage(distance_matrix, 'average',optimal_ordering=True)


fig = plt.figure(figsize=(25, 10))
dn = dendrogram(Z, p=200, labels = burst_list, distance_sort='descending')
# dn = dendrogram(Z, p=200, labels = burst_list,distance_sort='descending', truncate_mode='lastp')
# dn = dendrogram(Z, labels = burst_list, truncate_mode='lastp')
# dn = dendrogram(Z, labels = burst_list, truncate_mode='level')
plt.show()