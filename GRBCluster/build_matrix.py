
from scipy import signal
import numpy as np
import dtw
from grbpy.burst import Burst
import  matplotlib.pyplot as plt 
import csv
import os
import pickle


data_path = os.path.join('..','batse_data')

# select the matrix type
matrix_type = 'corr'

# adds a 25% buffer tot eh t90 time when False
no_buffer = True


# this is just a placeholder if one wants to truncate 
# the matrix build to only a few bursts. good for testing
begin_with_burst = 999999


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
    t90_start = float(dur_dict[burst_num]['t90_start'])
    t90_end = float(dur_dict[burst_num]['t90_start']) + float(dur_dict[burst_num]['t90'])

    return time, burst_data, t90_start, t90_end


def remove_background(background_dict,burst_data,time):
    return burst_data-float(background_dict['intercept'])-(time*float(background_dict['slope']))

def norm_time(time):
    return (time-min(time))/(max(time)-min(time))

def norm_data(data):
    return data/max(data)



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


distance_matrix = []
burst_list = []

for burst_num_1 in background_dict:


    if int(burst_num_1) > begin_with_burst:
        next
    else:
        
        burst_list.append(background_dict[burst_num_1]['burst_num'])

        calc_matrix = []

        for burst_num_2 in background_dict:

            if int(burst_num_2) > begin_with_burst:
                next
            else:

                if int(burst_num_2) > int(burst_num_1):

                    t90_buffer_1 = float(dur_dict[burst_num_1]['t90']) * 0.25
                    t90_buffer_2 = float(dur_dict[burst_num_2]['t90']) * 0.25

                    time_1, burst_data_1, t90_start_1, t90_end_1 = get_burst_data(burst_num_1)
                    time_2, burst_data_2, t90_start_2, t90_end_2 = get_burst_data(burst_num_2)

                    burst_data_2 = remove_background(background_dict[burst_num_2],burst_data_2,time_2)
                    burst_data_1 = remove_background(background_dict[burst_num_1],burst_data_1,time_1)
                    

                    len_t90_time_1 = len(time_1[(time_1 > float(t90_start_1)) & (time_1 < float(t90_end_1))])
                    len_t90_time_2 = len(time_2[(time_2 > float(t90_start_2)) & (time_2 < float(t90_end_2))])
                    
                    if no_buffer:
                        t90_data_1 = burst_data_1[(time_1 > float(t90_start_1)) & (time_1 < float(t90_end_1))]
                        t90_time_1 = time_1[(time_1 > float(t90_start_1)) & (time_1 < float(t90_end_1))]
                        t90_data_2= burst_data_2[(time_2 > float(t90_start_2)) & (time_2 < float(t90_end_2))]
                        t90_time_2 = time_2[(time_2 > float(t90_start_2)) & (time_2 < float(t90_end_2))]
                    else:
                        t90_data_buffer_1 = burst_data_1[(time_1 > (float(t90_start_1)-t90_buffer_1)) & (time_1 < (float(t90_end_1)+t90_buffer_1))]
                        t90_time_buffer_1 = time_1[(time_1 > (float(t90_start_1)-t90_buffer_1)) & (time_1 < (float(t90_end_1)+t90_buffer_1))]
                        t90_data_buffer_2= burst_data_2[(time_2 > (float(t90_start_2)-t90_buffer_2)) & (time_2 < (float(t90_end_2)+t90_buffer_2))]
                        t90_time_buffer_2 = time_2[(time_2 > (float(t90_start_2)-t90_buffer_2)) & (time_2 < (float(t90_end_2)+t90_buffer_2))]


                    if len_t90_time_1 < len_t90_time_2:
                        if no_buffer:
                            resampled_burst, resampled_time = signal.resample(t90_data_2, len(t90_time_1), t=time_2)
                            other_burst, other_time = t90_data_1, t90_time_1
                        else:
                            resampled_burst, resampled_time = signal.resample(t90_data_buffer_2, len(t90_time_buffer_1), t=time_2)
                            other_burst, other_time = t90_data_buffer_1, t90_time_buffer_1

                    elif len_t90_time_1 > len_t90_time_2:
                        if no_buffer:
                            resampled_burst, resampled_time = signal.resample(t90_data_1, len(t90_time_2), t=time_1)
                            other_burst, other_time = t90_data_2, t90_time_2
                        else:
                            resampled_burst, resampled_time = signal.resample(t90_data_buffer_1, len(t90_time_buffer_2), t=time_1)
                            other_burst, other_time = t90_data_buffer_2, t90_time_buffer_2
                    else:
                        next

                    norm_resampled = norm_data(resampled_burst)
                    norm_other     = norm_data(other_burst)


                    if matrix_type == 'corr':
                        norm_resampled = (norm_resampled - np.mean(norm_resampled)) / (np.std(norm_resampled))
                        norm_other = (norm_other - np.mean(norm_other)) / (np.std(norm_other))
                        corr = signal.correlate(norm_resampled,norm_other) / max(len(norm_resampled), len(norm_other))
                        calc = max(corr)
                        
                    # elif matrix_type == 'corr_norm':
                    #     calc = (np.sum(norm_resampled*norm_other)/(np.sqrt(np.sum(norm_resampled*norm_resampled)*np.sum(norm_other*norm_other))))+1

                    elif matrix_type == 'euclid':
                        calc = np.linalg.norm(norm_resampled-norm_other)

                    elif matrix_type == 'norm':
                        calc = np.linalg.norm(norm_resampled-norm_other, ord=1)/len(resampled_burst)

                    elif matrix_type == 'dtw':
                        DTW = dtw.dtw(norm_resampled,norm_other)
                        calc = DTW.normalizedDistance

                    else:
                        print('unsupported matrix_type')
                        next

                    print('burst 1:',burst_num_1,'- burst 2',burst_num_2,'-',matrix_type,'dist:',calc)

                    distance_matrix.append(calc)


with open(os.path.join('data',matrix_type+'_burst_list'+('_no_buffer' if no_buffer else '')+'.pkl'), 'wb') as f:
    pickle.dump(burst_list, f)

with open(os.path.join('data',matrix_type+'_matrix'+('_no_buffer' if no_buffer else '')+'.pkl'), 'wb') as f:
    pickle.dump(distance_matrix, f)