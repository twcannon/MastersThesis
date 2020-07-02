import scipy
from grbpy.burst import Burst
import  matplotlib.pyplot as plt 
import csv
import os
import numpy as np


def fix_background(burst_data,time,t90_start,t90_end):
    # print(burst_data)
    # print(time)
    print('len(burst_data)',len(burst_data))
    burst_data = burst_data[(time < t90_start) | (time > t90_end)]
    print('len(time)',len(time))
    time = time[(time < t90_start) | (time > t90_end)]
    time_fixed = time[burst_data > 0]
    print('len(time_fixed)',len(time_fixed))
    burst_fixed = burst_data[burst_data > 0]
    print('len(burst_fixed)',len(burst_fixed))
    # plt.plot(time_fixed,burst_fixed,)
    # # plt.plot(time,burst_data)
    # plt.show()

    
    return burst_fixed,time_fixed


# burst_num = str(5545)
burst_num = str(1419)
# burst_num = str(8084)

data_path = os.path.join('..','batse_data')

burst_dict = {}
with open(os.path.join('data','burst_info.csv'), newline='') as f:
    for row in csv.DictReader(f, delimiter=','):
        burst_dict[str(row['burst_num'])] = row

dur_dict = {}
with open(os.path.join('data','duration_table.csv'), newline='') as f:
    for row in csv.DictReader(f, delimiter=','):
        dur_dict[str(row['trig'])] = row


burst_info = burst_dict[burst_num]
# burst_num,burst_path,single_emission

file_path = os.path.join(data_path,burst_info['burst_file'])

grb = Burst(file_path)
grb.parse_batse_file()

burst_data = grb.sum_chan_data
header_names = grb.header_names.split()
header_data = grb.header_data.split()

meta_dict = {}
for i in range(len(header_data)):
    meta_dict[header_names[i]] = int(header_data[i])

time = (np.arange(meta_dict['npts'])-meta_dict['nlasc'])*0.064

t90_start = float(dur_dict[burst_num]['t90_start'])-float(dur_dict[burst_num]['t90_err'])
t90_end = float(dur_dict[burst_num]['t90_start'])+float(dur_dict[burst_num]['t90'])+float(dur_dict[burst_num]['t90_err'])

print(t90_start)
print(t90_end)

fixed_background, fixed_time = fix_background(burst_data,time,t90_start,t90_end)



print(meta_dict)
print(burst_dict[burst_num])
print(dur_dict[burst_num])
plt.plot(time,burst_data)
plt.plot(fixed_time,fixed_background)
# plt.plot(time,burst_data)
plt.show()
