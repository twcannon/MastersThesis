from scipy.stats import pearsonr
import matplotlib.pyplot as plt
import pickle
import numpy as np
import csv
import os,sys


# changeable inputs
# choices are: euclid, corr, dtw, and norm (for manhattan)
matrix_type = 'dtw'
no_buffer = False

# open linkage matrix
with open(os.path.join('data',matrix_type+'_linkage'+('_no_buffer' if no_buffer else '')+'.pkl'), 'rb') as f:
    linkage_matrix = pickle.load(f)

# parse in burst list
with open(os.path.join('data',matrix_type+'_burst_list'+('_no_buffer' if no_buffer else '')+'.pkl'), 'rb') as f:
    burst_list = pickle.load(f)

# open background table
background_dict = {}
with open(os.path.join('data','background_table.csv'), newline='') as f:
    for row in csv.DictReader(f, delimiter=','):
        background_dict[str(row['burst_num'])] = row

s_n_x  = []
dist_y = []
labels = []

for i in range(len(linkage_matrix)):
    try:
        if linkage_matrix[i][0] < len(burst_list):
            burst_num = burst_list[int(linkage_matrix[i][0])]
            labels.append(burst_num)
            s_n_x.append(float(background_dict[burst_num]['signal_to_noise']))
            dist_y.append(linkage_matrix[i][2])

        if linkage_matrix[i][1] < len(burst_list):
            burst_num = burst_list[int(linkage_matrix[i][1])]
            labels.append(burst_num)
            s_n_x.append(float(background_dict[burst_num]['signal_to_noise']))
            dist_y.append(linkage_matrix[i][2])
    except:
        next

print(pearsonr(np.log(s_n_x),np.log(dist_y)))

plt.plot(np.log(s_n_x),np.log(dist_y),'.')
plt.xlabel('log(Signal to Noise)')
plt.ylabel('log(Dendrogram Distance)')

plt.show()
