
import numpy as np
import os
import pickle
import  matplotlib.pyplot as plt 
from scipy.cluster.hierarchy import dendrogram, linkage
import sys
sys.setrecursionlimit(10000)


with open(os.path.join('data','euclid_matrix.pkl'), 'rb') as f:
# with open(os.path.join('data','inv_corr_matrix.pkl'), 'rb') as f:
    distance_matrix = pickle.load(f)

with open(os.path.join('data','euclid_burst_list.pkl'), 'rb') as f:
# with open(os.path.join('data','burst_list.pkl'), 'rb') as f:
    burst_list = pickle.load(f)


# distance_matrix = 1/np.asarray(distance_matrix)

distance_matrix = [0 if x < 0 else x for x in distance_matrix]

# print(distance_matrix)

Z = linkage(distance_matrix, 'single')
# Z = linkage(distance_matrix, 'single',optimal_ordering=True)

# print(burst_list[0])
# print(burst_list[-1])
print(len(Z))
print(Z)
print(len(Z[0]))
print(Z[0])

fig = plt.figure(figsize=(25, 10))
# dn = dendrogram(Z, labels = burst_list)
dn = dendrogram(Z, labels = burst_list, truncate_mode='lastp')
dn = dendrogram(Z, labels = burst_list, truncate_mode='level')
plt.show()