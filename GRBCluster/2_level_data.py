
from scipy import stats
from grbpy.burst import Burst
import  matplotlib.pyplot as plt 
import csv
import os
import numpy as np


data_path = os.path.join('..','batse_data')

burst_dict = {}
with open(os.path.join('data','burst_info.csv'), newline='') as f:
    for row in csv.DictReader(f, delimiter=','):
        burst_dict[str(row['burst_num'])] = row

background_dict = {}
with open(os.path.join('data','background_table.csv'), newline='') as f:
    for row in csv.DictReader(f, delimiter=','):
        background_dict[str(row['burst_num'])] = row

for burst_num in background_dict:

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

    burst_data = burst_data[(time > float(background_dict[burst_num]['min_time'])) | (time < float(background_dict[burst_num]['max_time']))]
    time = time[(time > float(background_dict[burst_num]['min_time'])) | (time < float(background_dict[burst_num]['max_time']))]

    
    if float(background_dict[burst_num]['p_value']) < 0.05:
        plt.plot(time,burst_data)
        plt.plot(time,burst_data-float(background_dict[burst_num]['intercept'])-(time*float(background_dict[burst_num]['slope'])))
        plt.show()
    else:
        print(burst_num,'low p_value')