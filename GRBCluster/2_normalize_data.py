
from scipy import signal
import numpy as np
import dtw
from grbpy.burst import Burst
import  matplotlib.pyplot as plt 
import csv
import os
import pickle


data_path = os.path.join('..','batse_data')

matrix_type = 'norm'
no_buffer = True


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


    if int(burst_num_1) > 10000:
        next
    else:
        
        burst_list.append(background_dict[burst_num_1]['burst_num'])

        calc_matrix = []

        for burst_num_2 in background_dict:

            if int(burst_num_2) > 10000:
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

                    # print('========================')

                    if matrix_type == 'corr':
                        corr = signal.correlate(norm_resampled,norm_other)
                        calc = max(corr)
                        print('burst 1:',burst_num_1,'- burst 2',burst_num_2,'-',matrix_type,'dist:',calc)

                    elif matrix_type == 'corr_norm':
                        calc = (np.sum(norm_resampled*norm_other)/(np.sqrt(np.sum(norm_resampled*norm_resampled)*np.sum(norm_other*norm_other))))+1
                        print('burst 1:',burst_num_1,'- burst 2',burst_num_2,'-',matrix_type,'dist:',calc)

                    elif matrix_type == 'euclid':
                        calc = np.linalg.norm(norm_resampled-norm_other)
                        print('burst 1:',burst_num_1,'- burst 2',burst_num_2,'-',matrix_type,'dist:',calc)

                    elif matrix_type == 'norm':
                        calc = np.linalg.norm(norm_resampled-norm_other, ord=1)/len(resampled_burst)
                        print('burst 1:',burst_num_1,'- burst 2',burst_num_2,'-',matrix_type,'dist:',calc)

                    elif matrix_type == 'dtw':
                        DTW = dtw.dtw(norm_resampled,norm_other)
                        calc = DTW.normalizedDistance
                        print('burst 1:',burst_num_1,'- burst 2',burst_num_2,'-',matrix_type,'dist:',calc)

                    else:
                        print('unsupported matrix_type')

                    # print('========================')

                    distance_matrix.append(calc)

                    # print('length burst_data_1', len(burst_data_1))
                    # print('length time_1', len(time_1))
                    # print('length t90_time_1', len(t90_time_1))
                    # print('min_time', background_dict[burst_num_1]['min_time'])
                    # print('t90_start_1',t90_start_1)
                    # print('t90_end_1',t90_end_1)
                    # print('max_time',background_dict[burst_num_1]['max_time'])
                    # print('------------')
                    # print('length burst_data_2', len(burst_data_2))
                    # print('length time_2', len(time_2))
                    # print('length t90_time_2', len(t90_time_2))
                    # print('min_time', background_dict[burst_num_2]['min_time'])
                    # print('t90_start_2',t90_start_2)
                    # print('t90_end_2',t90_end_2)
                    # print('max_time',background_dict[burst_num_2]['max_time'])
                    # print('------------')


                    # if max_corr > 100:
                    # # if euclid > 10:
                    # if (int(burst_num_1) == 563) and (int(burst_num_2) == 658):
                    #     plt.plot(norm_resampled,'-')
                    #     plt.plot(norm_other,'-')
                    #     # plt.plot(corr)
                    #     plt.show()

        # distance_matrix.append(calc_matrix)


                    # import sys
                    # sys.exit()
        
# for row in distance_matrix:
#     print(len(row))

with open(os.path.join('data',matrix_type+'_burst_list'+('_no_buffer' if no_buffer else '')+'.pkl'), 'wb') as f:
    pickle.dump(burst_list, f)

# with open(os.path.join('data','inv_corr_matrix.pkl'), 'wb') as f:
# with open(os.path.join('data','norm_matrix.pkl'), 'wb') as f:
with open(os.path.join('data',matrix_type+'_matrix'+('_no_buffer' if no_buffer else '')+'.pkl'), 'wb') as f:
    pickle.dump(distance_matrix, f)


