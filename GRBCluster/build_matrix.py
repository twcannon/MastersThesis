
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
matrix_type = 'euclid'

# adds a 25% buffer tot eh t90 time when False
no_buffer = True


# this is just a placeholder if one wants to truncate 
# the matrix build to only a few bursts. good for testing
begin_with_burst = 999999


def get_burst_data(burst_num):
    '''this function is for parsing in burst data'''
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
    '''this function removes the background from a burst'''
    return burst_data-float(background_dict['intercept'])-(time*float(background_dict['slope']))

def norm_time(time):
    '''this function normalizes time of a burst'''
    return (time-min(time))/(max(time)-min(time))

def norm_data(data):
    '''this function normalizes data of a burst'''
    return data/max(data)



# parse in burst_info.csv
burst_dict = {}
with open(os.path.join('data','burst_info.csv'), newline='') as f:
    for row in csv.DictReader(f, delimiter=','):
        burst_dict[str(row['burst_num'])] = row

# parse in background_table.csv
background_dict = {}
with open(os.path.join('data','background_table.csv'), newline='') as f:
    for row in csv.DictReader(f, delimiter=','):
        background_dict[str(row['burst_num'])] = row

# parse in duration_table.csv
dur_dict = {}
with open(os.path.join('data','duration_table.csv'), newline='') as f:
    for row in csv.DictReader(f, delimiter=','):
        dur_dict[str(row['trig'])] = row


# inits 
distance_matrix = []
burst_list = []

# looping through bursts
for burst_num_1 in background_dict:

    if int(burst_num_1) > begin_with_burst:
        next
    else:
        
        # build burst list
        burst_list.append(background_dict[burst_num_1]['burst_num'])

        # inits
        calc_matrix = []

        # looping through bursts
        for burst_num_2 in background_dict:

            # convenient way to ensure an upper triangular matrix
            if int(burst_num_2) > begin_with_burst:
                next
            else:

                # convenient way to ensure an upper triangular matrix
                if int(burst_num_2) > int(burst_num_1):

                    # build buffers
                    t90_buffer_1 = float(dur_dict[burst_num_1]['t90']) * 0.25
                    t90_buffer_2 = float(dur_dict[burst_num_2]['t90']) * 0.25

                    # parse in burst data from file
                    time_1, burst_data_1, t90_start_1, t90_end_1 = get_burst_data(burst_num_1)
                    time_2, burst_data_2, t90_start_2, t90_end_2 = get_burst_data(burst_num_2)

                    # remove background
                    burst_data_2 = remove_background(background_dict[burst_num_2],burst_data_2,time_2)
                    burst_data_1 = remove_background(background_dict[burst_num_1],burst_data_1,time_1)
                    
                    # find the length of each burst vector for late use
                    len_t90_time_1 = len(time_1[(time_1 > float(t90_start_1)) & (time_1 < float(t90_end_1))])
                    len_t90_time_2 = len(time_2[(time_2 > float(t90_start_2)) & (time_2 < float(t90_end_2))])
                    
                    if no_buffer:
                        # build the t90 window for each bursts time and data
                        t90_data_1 = burst_data_1[(time_1 > float(t90_start_1)) & (time_1 < float(t90_end_1))]
                        t90_time_1 = time_1[(time_1 > float(t90_start_1)) & (time_1 < float(t90_end_1))]
                        t90_data_2= burst_data_2[(time_2 > float(t90_start_2)) & (time_2 < float(t90_end_2))]
                        t90_time_2 = time_2[(time_2 > float(t90_start_2)) & (time_2 < float(t90_end_2))]
                    else:
                        # build the t90+buffer window for each bursts time and data
                        t90_data_buffer_1 = burst_data_1[(time_1 > (float(t90_start_1)-t90_buffer_1)) & (time_1 < (float(t90_end_1)+t90_buffer_1))]
                        t90_time_buffer_1 = time_1[(time_1 > (float(t90_start_1)-t90_buffer_1)) & (time_1 < (float(t90_end_1)+t90_buffer_1))]
                        t90_data_buffer_2= burst_data_2[(time_2 > (float(t90_start_2)-t90_buffer_2)) & (time_2 < (float(t90_end_2)+t90_buffer_2))]
                        t90_time_buffer_2 = time_2[(time_2 > (float(t90_start_2)-t90_buffer_2)) & (time_2 < (float(t90_end_2)+t90_buffer_2))]


                    # This is a check to make sure the longer vector is the one that is resampled
                    if len_t90_time_1 < len_t90_time_2:
                        if no_buffer:
                            # resample the longer vector
                            resampled_burst, resampled_time = signal.resample(t90_data_2, len(t90_time_1), t=time_2)
                            # rename the other burst
                            other_burst, other_time = t90_data_1, t90_time_1
                        else:
                            # resample the longer vector
                            resampled_burst, resampled_time = signal.resample(t90_data_buffer_2, len(t90_time_buffer_1), t=time_2)
                            # rename the other burst
                            other_burst, other_time = t90_data_buffer_1, t90_time_buffer_1

                    elif len_t90_time_1 > len_t90_time_2:
                        if no_buffer:
                            # resample the longer vector
                            resampled_burst, resampled_time = signal.resample(t90_data_1, len(t90_time_2), t=time_1)
                            # rename the other burst
                            other_burst, other_time = t90_data_2, t90_time_2
                        else:
                            # resample the longer vector
                            resampled_burst, resampled_time = signal.resample(t90_data_buffer_1, len(t90_time_buffer_2), t=time_1)
                            # rename the other burst
                            other_burst, other_time = t90_data_buffer_2, t90_time_buffer_2
                    else:
                        next

                    # normalize the scale of each vector form 0 to 1 
                    norm_resampled = norm_data(resampled_burst)
                    norm_other     = norm_data(other_burst)

                    #################################
                    # Zero Normalized Cross Correlation
                    if matrix_type == 'corr':
                        norm_resampled = (norm_resampled - np.mean(norm_resampled)) / (np.std(norm_resampled))
                        norm_other = (norm_other - np.mean(norm_other)) / (np.std(norm_other))
                        corr = signal.correlate(norm_resampled,norm_other) / max(len(norm_resampled), len(norm_other))
                        calc = max(corr)

                    #################################
                    # Euclidean Norm
                    elif matrix_type == 'euclid':
                        calc = np.linalg.norm(norm_resampled-norm_other)

                    #################################
                    # Normalized Manhattan Distance
                    elif matrix_type == 'norm':
                        calc = np.linalg.norm(norm_resampled-norm_other, ord=1)/len(resampled_burst)

                    #################################
                    # Dynamic Time Warping
                    elif matrix_type == 'dtw':
                        DTW = dtw.dtw(norm_resampled,norm_other)
                        calc = DTW.normalizedDistance

                    else:
                        print('unsupported matrix_type')
                        next

                    print('burst 1:',burst_num_1,'- burst 2',burst_num_2,'-',matrix_type,'dist:',calc)

                    # append to the distance matrix
                    distance_matrix.append(calc)

# write out the matrix to a python pickle file
with open(os.path.join('data',matrix_type+'_burst_list'+('_no_buffer' if no_buffer else '')+'.pkl'), 'wb') as f:
    pickle.dump(burst_list, f)

# write out the burst list to a python pickle file
with open(os.path.join('data',matrix_type+'_matrix'+('_no_buffer' if no_buffer else '')+'.pkl'), 'wb') as f:
    pickle.dump(distance_matrix, f)