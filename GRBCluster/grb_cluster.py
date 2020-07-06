
from scipy import stats
from grbpy.burst import Burst
import  matplotlib.pyplot as plt 
import csv
import os
import numpy as np


def fix_background(burst_data,time,time_start,time_end,add_time):
    # burst_data = burst_data[(time < time_start) | (time > time_end)]
    # time = time[(time < time_start) | (time > time_end)]
    # time_fixed = time[burst_data > 0]
    # burst_fixed = burst_data[burst_data > 0]

    # burst_data = burst_data[((time > time_start-add_time) | (time < time_start)) | ((time > time_end) | (time < time_end+add_time))]
    burst_data = burst_data[((time > (time_start-add_time)) & (time < time_start)) | ((time > time_end) & (time < time_end+add_time))]
    time = time[((time > time_start-add_time) & (time < time_start))| ((time > time_end) & (time < time_end+add_time))]
    time_fixed = time[burst_data > 0]
    burst_fixed = burst_data[burst_data > 0]


    return burst_fixed,time_fixed


# burst_num = str(5545)
burst_num = str(1419)
# burst_num = str(8084)

add_time_mult = 0.25

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

add_time = float(dur_dict[burst_num]['t90'])*add_time_mult
time_start = float(dur_dict[burst_num]['t90_start'])-float(dur_dict[burst_num]['t90_err'])-add_time
time_end = float(dur_dict[burst_num]['t90_start'])+float(dur_dict[burst_num]['t90'])+add_time+float(dur_dict[burst_num]['t90_err'])


fixed_background, fixed_time = fix_background(burst_data,time,time_start,time_end,add_time)

slope, intercept, r_value, p_value, std_err = stats.linregress(fixed_time,fixed_background)
print('slope',slope)
print('intercept',intercept)
print('r_value',r_value)
print('p_value',p_value)
print('std_err',std_err)




print(meta_dict)
print(burst_dict[burst_num])
print(dur_dict[burst_num])
plt.plot(time,burst_data)
plt.plot(fixed_time,fixed_background)
plt.plot(time,burst_data-intercept-(time*slope))
# plt.plot(time,burst_data)
plt.show()
