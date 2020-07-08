
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




for burst_num_1 in background_dict:

    if int(burst_num_1) != 111:
        next
    else:

        for burst_num_2 in background_dict:

            if burst_num_1 != burst_num_2:

                t90_buffer_1 = float(dur_dict[burst_num_1]['t90']) * 0.25
                t90_buffer_2 = float(dur_dict[burst_num_2]['t90']) * 0.25

                time_1, burst_data_1, t90_start_1, t90_end_1 = get_burst_data(burst_num_1)
                time_2, burst_data_2, t90_start_2, t90_end_2 = get_burst_data(burst_num_2)

                burst_data_2 = remove_background(background_dict[burst_num_2],burst_data_2,time_2)
                burst_data_1 = remove_background(background_dict[burst_num_1],burst_data_1,time_1)
                
                t90_data_1 = burst_data_1[(time_1 > float(t90_start_1)) & (time_1 < float(t90_end_1))]
                t90_data_buffer_1 = burst_data_1[(time_1 > (float(t90_start_1)-t90_buffer_1)) & (time_1 < (float(t90_end_1)+t90_buffer_1))]
                t90_time_1 = time_1[(time_1 > float(t90_start_1)) & (time_1 < float(t90_end_1))]
                t90_time_buffer_1 = time_1[(time_1 > (float(t90_start_1)-t90_buffer_1)) & (time_1 < (float(t90_end_1)+t90_buffer_1))]

                t90_data_2= burst_data_2[(time_2 > float(t90_start_2)) & (time_2 < float(t90_end_2))]
                t90_data_buffer_2= burst_data_2[(time_2 > (float(t90_start_2)-t90_buffer_2)) & (time_2 < (float(t90_end_2)+t90_buffer_2))]
                t90_time_2 = time_2[(time_2 > float(t90_start_2)) & (time_2 < float(t90_end_2))]
                t90_time_buffer_2 = time_2[(time_2 > (float(t90_start_2)-t90_buffer_2)) & (time_2 < (float(t90_end_2)+t90_buffer_2))]

                # remove bursts that are 2 seconds or shorter
                if (len(t90_time_1) < 32) or (len(t90_time_2) < 32):
                    next
                else:

                    # remove bursts that have missing data
                    if (min(t90_data_1) == 0) or (min(t90_data_2) == 0):
                        next
                    else: 


                        if len(t90_time_1) < len(t90_time_2):
                            print('resampling burst 2')
                            # resampled_burst, resampled_time = signal.resample(t90_data_2, len(t90_time_1), t=time_2)
                            resampled_burst, resampled_time = signal.resample(t90_data_buffer_2, len(t90_time_buffer_1), t=time_2)
                            # other_burst, other_time = t90_data_1, t90_time_1
                            other_burst, other_time = t90_data_buffer_1, t90_time_buffer_1
                        elif len(t90_time_1) > len(t90_time_2):
                            print('resampling burst 1')
                            # resampled_burst, resampled_time = signal.resample(t90_data_1, len(t90_time_2), t=time_1)
                            resampled_burst, resampled_time = signal.resample(t90_data_buffer_1, len(t90_time_buffer_2), t=time_1)
                            # other_burst, other_time = t90_data_2, t90_time_2
                            other_burst, other_time = t90_data_buffer_2, t90_time_buffer_2
                        else:
                            next

                        corr = signal.correlate(norm_data(resampled_burst),norm_data(other_burst))



                        print('========================')
                        print('burst 1:',burst_num_1,'- burst 2',burst_num_2)
                        print('max corr:',max(corr))
                        print('========================')


                        print('length burst_data_1', len(burst_data_1))
                        print('length time_1', len(time_1))
                        print('length t90_time_1', len(t90_time_1))
                        print('min_time', background_dict[burst_num_1]['min_time'])
                        print('t90_start_1',t90_start_1)
                        print('t90_end_1',t90_end_1)
                        print('max_time',background_dict[burst_num_1]['max_time'])
                        print('------------')
                        print('length burst_data_2', len(burst_data_2))
                        print('length time_2', len(time_2))
                        print('length t90_time_2', len(t90_time_2))
                        print('min_time', background_dict[burst_num_2]['min_time'])
                        print('t90_start_2',t90_start_2)
                        print('t90_end_2',t90_end_2)
                        print('max_time',background_dict[burst_num_2]['max_time'])
                        print('------------')

                        plt.plot(norm_data(resampled_burst),'--')
                        plt.plot(norm_data(other_burst),'--')
                        plt.plot(norm_data(resampled_burst),'-')
                        plt.plot(np.arange(-len(other_burst),0)+np.argmax(corr),norm_data(other_burst),'-')
                        # plt.plot(corr)
                        plt.show()
                        # plt.plot(time_1,burst_data_1)

                        # if len(t90_time_1) < len(t90_time_2):
                        #     print('resampling burst 2')
                        #     resampled_burst, resampled_time = signal.resample(burst_data_2, int(len(burst_data_2)*(len(t90_time_1)/len(t90_time_2))), t=time_2)
                        #     burst_data_2, time_2 = signal.resample(burst_data_2, int(len(burst_data_2)*(len(t90_time_1)/len(t90_time_2))), t=time_2)
                        # elif len(t90_time_1) > len(t90_time_2):
                        #     print('resampling burst 1')
                        #     resampled_burst, resampled_time = signal.resample(burst_data_1, int(len(burst_data_1)*(len(t90_time_2)/len(t90_time_1))), t=time_1)
                        #     burst_data_1, time_1 = signal.resample(burst_data_1, int(len(burst_data_1)*(len(t90_time_2)/len(t90_time_1))), t=time_1)
                        # else:
                        #     next

                        # print('resampled_burst',resampled_burst)
                        # print('resampled_burst',len(resampled_burst))
                        # print('resampled_time',resampled_time)
                        # print('resampled_time',len(resampled_time))
                        # # plt.plot(resampled_time,resampled_burst)



                        # plt.plot(time_1,burst_data_1)
                        # plt.plot(time_2,burst_data_2)

                        # plt.plot(norm_time(resampled_time),norm_data(resampled_burst))
                        # plt.plot(norm_time(other_time),norm_data(other_burst))
                        # plt.show()

                # import sys
                # sys.exit()
        
        else:
            next

