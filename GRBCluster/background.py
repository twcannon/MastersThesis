
from scipy import stats
from grbpy.burst import Burst
import  matplotlib.pyplot as plt 
import csv
import os
import numpy as np


def fix_background(burst_data,time,time_start,time_end,add_time):
    try:
        burst_data = burst_data[((time > (time_start-add_time)) & (time < time_start)) | ((time > time_end) & (time < (time_end+add_time)))]
    except:
        burst_data = burst_data[((time > min(time)) & (time < time_start)) | ((time > time_end) & (time < max(time)))]
    try:
        time = time[((time > (time_start-add_time)) & (time < time_start)) | ((time > time_end) & (time < (time_end+add_time)))]
    except:
        time = time[((time > min(time)) & (time < time_start)) | ((time > time_end) & (time < max(time)))]
    time_fixed = time[burst_data > 0]
    burst_fixed = burst_data[burst_data > 0]
    return burst_fixed,time_fixed



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



background_file = open('background.csv', 'w', newline ='') 
with background_file:
    header = ['burst_num','slope','intercept','r_value','p_value','std_err'] 
    writer = csv.DictWriter(background_file, fieldnames = header) 
    writer.writeheader() 

    for burst_num in dur_dict:

        try:
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
            try:
                time_start = (float(dur_dict[burst_num]['t90_start'])-float(dur_dict[burst_num]['t90_err'])-add_time)
            except:
                time_start = min(time) + ((dur_dict[burst_num]['t90_start'] - min(time))/2)
            
            try:
                time_end = (float(dur_dict[burst_num]['t90_start'])+float(dur_dict[burst_num]['t90'])+add_time+float(dur_dict[burst_num]['t90_err']))
            except:
                time_start = max(time) - ((max(time) - dur_dict[burst_num]['t90_end'])/2)


            fixed_background, fixed_time = fix_background(burst_data,time,time_start,time_end,add_time)

            if len(fixed_time > 5):

                slope, intercept, r_value, p_value, std_err = stats.linregress(fixed_time,fixed_background)

                if str(slope) == 'nan':
                    print(burst_num,'slope = nan')
                elif p_value == 0.0:
                    print(burst_num,'p_value = 0.0')
                else:
                    writer.writerow({'burst_num':burst_num,'slope':slope,'intercept':intercept,'r_value':r_value,'p_value':p_value,'std_err':std_err})
                    print(burst_num,'success - burst:')

            else:
                print(burst_num,'NOT enough points - burst:')
        except Exception as err:
            print(burst_num,'FAILURE - burst:', err)
            next
        # sys.exit()