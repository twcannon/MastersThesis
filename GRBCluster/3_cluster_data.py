
import os
import pickle
import  matplotlib.pyplot as plt 
from scipy.cluster.hierarchy import dendrogram, linkage


with open(os.path.join('data','inv_corr_matrix.pkl'), 'rb') as f:
    distance_matrix = pickle.load(f)

with open(os.path.join('data','burst_list.pkl'), 'rb') as f:
    burst_list = pickle.load(f)


Z = linkage(distance_matrix, 'single')
# Z = linkage(distance_matrix, 'single',optimal_ordering=True)
fig = plt.figure(figsize=(25, 10))
dn = dendrogram(Z, labels = burst_list)
plt.show()