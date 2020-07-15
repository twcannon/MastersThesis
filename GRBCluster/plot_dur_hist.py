import  matplotlib.pyplot as plt 
import numpy as np
import csv
import sys, os

dur_list = []
with open(os.path.join('data','duration_table.csv'), newline='') as f:
    for row in csv.DictReader(f, delimiter=','):
    	dur_list.append(np.log(float(row['t90'])))
plt.hist(dur_list,bins=25)
plt.title('Bimodal distribution of GRB durations')
plt.xlabel('log(t90)')
# plt.plot(bins)
plt.show()
