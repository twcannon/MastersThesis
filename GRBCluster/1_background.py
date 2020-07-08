
from scipy import stats
from grbpy.burst import Burst
import  matplotlib.pyplot as plt 
import csv
import os
import numpy as np


def fix_background(burst_data,time,time_start,time_end,add_time):
    try:
        burst_data = burst_data[((time > (time_start-add_time*2)) & (time < time_start)) | ((time > time_end) & (time < (time_end+add_time*2)))]
    except:
        burst_data = burst_data[((time > min(time)) & (time < time_start)) | ((time > time_end) & (time < max(time)))]
    try:
        time = time[((time > (time_start-add_time*2)) & (time < time_start)) | ((time > time_end) & (time < (time_end+add_time*2)))]
    except:
        time = time[((time > min(time)) & (time < time_start)) | ((time > time_end) & (time < max(time)))]
    # time_fixed = time[burst_data > 0]
    # burst_fixed = burst_data[burst_data > 0]
    time_fixed = time
    burst_fixed = burst_data
    return burst_fixed,time_fixed



add_time_mult = 1

data_path = os.path.join('..','batse_data')

burst_dict = {}
with open(os.path.join('data','burst_info.csv'), newline='') as f:
    for row in csv.DictReader(f, delimiter=','):
        burst_dict[str(row['burst_num'])] = row

dur_dict = {}
with open(os.path.join('data','duration_table.csv'), newline='') as f:
    for row in csv.DictReader(f, delimiter=','):
        dur_dict[str(row['trig'])] = row



background_file = open(os.path.join('data','background_table.csv'), 'w', newline ='') 
with background_file:
    header = ['burst_num','slope','intercept','r_value','p_value','std_err','min_time','max_time'] 
    writer = csv.DictWriter(background_file, fieldnames = header) 
    writer.writeheader() 

    for burst_num in dur_dict:

        # remove shorts
        if float(dur_dict[burst_num]['t90']) < 2:
            next
        else:

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
                
                if float(dur_dict[burst_num]['t90']) < 4:
                    add_time = 8
                else:
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


                # remove bursts with missing data
                if min(fixed_background) == 0:
                    next
                else:

                    slope, intercept, r_value, p_value, std_err = stats.linregress(fixed_time,fixed_background)

                    if len(fixed_time > 5):

                        if str(slope) == 'nan':
                            print(burst_num,'slope = nan')
                        else:
                            writer.writerow({'burst_num':burst_num,'slope':slope,'intercept':intercept,'r_value':r_value,'p_value':p_value,'std_err':std_err,'min_time':min(fixed_time),'max_time':max(fixed_time)})
                            print(burst_num,'success')
                    else:
                        print(burst_num,'NOT enough points')

                    # plt.plot(time,burst_data)
                    # plt.plot(fixed_time,fixed_background)
                    # plt.plot(time,burst_data-intercept-(time*slope))
                    # plt.show()

            except Exception as err:
                print(burst_num,'FAILURE - burst:', err)
                next
            # sys.exit()