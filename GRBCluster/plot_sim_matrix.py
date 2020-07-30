import matplotlib.pyplot as plt
import pickle
import numpy as np
import csv
import os,sys


# changeable inputs
# choices are: euclid, corr, dtw, and norm (for manhattan)
matrix_type = 'dtw'
no_buffer = False

# open similarity matrix
with open(os.path.join('data',matrix_type+'_matrix'+('_no_buffer' if no_buffer else '')+'.pkl'), 'rb') as f:
    similarity_matrix = pickle.load(f)


# open burst list
with open(os.path.join('data',matrix_type+'_burst_list'+('_no_buffer' if no_buffer else '')+'.pkl'), 'rb') as f:
    burst_list = pickle.load(f)
# print(len(similarity_matrix))
# print(np.array([None]*(len(similarity_matrix)+len(burst_list))))
# print(len(np.array([None]*(len(similarity_matrix)+len(burst_list)))))
similarity_matrix = np.append(similarity_matrix,
    np.array([0]*(len(similarity_matrix)+len(burst_list))))

ut_sim_matrix = []
for i in range(1,len(burst_list)-1):
    row = np.asarray(([0]*(i-1))+list(similarity_matrix[ (len(burst_list)*(i-1))+i : (len(burst_list)*i) ]))
    ut_sim_matrix.append(np.log(row))

ut_sim_matrix = np.asarray(ut_sim_matrix)


print(ut_sim_matrix[0])
print(ut_sim_matrix[-1])

# print(ut_sim_matrix)
# print(len(ut_sim_matrix))
print(np.shape(ut_sim_matrix))


fig, ax = plt.subplots(figsize=(20,20))
cax = ax.matshow(ut_sim_matrix, interpolation='nearest')
ax.grid(True)
plt.title('GRB Emission Similarity Matrix')
# plt.xticks(range(33), burst_list, rotation=90);
# plt.yticks(range(33), burst_list);
fig.colorbar(cax, ticks=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, .75,.8,.85,.90,.95,1])
plt.show()