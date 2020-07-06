
from scipy import stats
from scipy import signal
from grbpy.burst import Burst
import  matplotlib.pyplot as plt 
import csv
import os
import numpy as np


data_path = os.path.join('..','batse_data')


def get_burst_data(burst_num):

    burst_info = burst_dict[burst_num]
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
    t_90_start = float(dur_dict[burst_num]['t90_start'])
    t_90_end = float(dur_dict[burst_num]['t90_start']) + float(dur_dict[burst_num]['t90'])

    return time, burst_data, t90_start, t_90_end



burst_dict = {}
with open(os.path.join('data','burst_info.csv'), newline='') as f:
    for row in csv.DictReader(f, delimiter=','):
        burst_dict[str(row['burst_num'])] = row

background_dict = {}
with open(os.path.join('data','background_table.csv'), newline='') as f:
    for row in csv.DictReader(f, delimiter=','):
        background_dict[str(row['burst_num'])] = row

dur_dict = {}
with open(os.path.join('data','duration_table.csv'), newline='') as f:
    for row in csv.DictReader(f, delimiter=','):
        dur_dict[str(row['trig'])] = row


for burst_num_1 in background_dict:

    for burst_num_2 in background_dict:

        if burst_num_1 != burst_num_2:
            time_1, burst_data_1, t_90_start_1, t_90_end_1 = get_burst_data(burst_num_1)
            time_2, burst_data_2, t_90_start_2, t_90_end_2 = get_burst_data(burst_num_2)
        
        else:
            next

    burst_data_1 = burst_data_1[(time_1 > float(background_dict[burst_num]['min_time'])) | (time_1 < float(background_dict[burst_num]['max_time']))]
    time_1 = time_1[(time_1 > float(background_dict[burst_num]['min_time'])) | (time_1 < float(background_dict[burst_num]['max_time']))]

    burst_data_2= burst_data_2[(time_2 > float(background_dict[burst_num]['min_time'])) | (time_2 < float(background_dict[burst_num]['max_time']))]
    time_2 = time_2[(time_2 > float(background_dict[burst_num]['min_time'])) | (time_2 < float(background_dict[burst_num]['max_time']))]
