import numpy as np
import os
import pickle
from scipy import stats

'''calculate and print the similarity between each matrix'''


print('\n-----------------------')
with open(os.path.join('data','euclid_matrix_no_buffer.pkl'), 'rb') as f:
    euclid_matrix_no_buffer = pickle.load(f)
with open(os.path.join('data','corr_matrix.pkl'), 'rb') as f:
    euclid_matrix = np.asarray(pickle.load(f))
print('euclid matrix length',len(euclid_matrix))
print('euclid matrices norm',np.linalg.norm(euclid_matrix-euclid_matrix_no_buffer))
print('euclid pearson',stats.pearsonr(euclid_matrix,euclid_matrix_no_buffer))


print('\n-----------------------')
with open(os.path.join('data','corr_matrix_no_buffer.pkl'), 'rb') as f:
    corr_matrix_no_buffer = pickle.load(f)
with open(os.path.join('data','corr_matrix.pkl'), 'rb') as f:
    corr_matrix = np.asarray(pickle.load(f))
print('corr matrix length',len(corr_matrix))
print('corr matrices norm',np.linalg.norm(corr_matrix-corr_matrix_no_buffer))
print('corr pearson',stats.pearsonr(corr_matrix,corr_matrix_no_buffer))


print('\n-----------------------')
with open(os.path.join('data','dtw_matrix_no_buffer.pkl'), 'rb') as f:
    dtw_matrix_no_buffer = pickle.load(f)
with open(os.path.join('data','dtw_matrix.pkl'), 'rb') as f:
    dtw_matrix = np.asarray(pickle.load(f))
print('dtw matrix length',len(dtw_matrix))
print('dtw matrices norm',np.linalg.norm(dtw_matrix-dtw_matrix_no_buffer))
print('dtw pearson',stats.pearsonr(dtw_matrix,dtw_matrix_no_buffer))


print('\n-----------------------')
with open(os.path.join('data','norm_matrix_no_buffer.pkl'), 'rb') as f:
    norm_matrix_no_buffer = pickle.load(f)
with open(os.path.join('data','norm_matrix.pkl'), 'rb') as f:
    norm_matrix = np.asarray(pickle.load(f))
print('norm matrix length',len(norm_matrix))
print('norm matrices norm',np.linalg.norm(norm_matrix-norm_matrix_no_buffer))
print('norm pearson',stats.pearsonr(norm_matrix,norm_matrix_no_buffer))

