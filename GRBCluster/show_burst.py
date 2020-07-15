from grbpy.burst import Burst
import  matplotlib.pyplot as plt 
# from scipy import stats
import csv
import os
import numpy as np


data_path = os.path.join('..','batse_data')


dur_dict = {}
with open(os.path.join('data','duration_table.csv'), newline='') as f:
    for row in csv.DictReader(f, delimiter=','):
        dur_dict[str(row['trig'])] = row


background_dict = {}
with open(os.path.join('data','background_table.csv'), newline='') as f:
    for row in csv.DictReader(f, delimiter=','):
        background_dict[str(row['burst_num'])] = row


burst_dict = {}
with open(os.path.join('data','burst_info.csv'), newline='') as f:
    for row in csv.DictReader(f, delimiter=','):
        burst_dict[str(row['burst_num'])] = row



def remove_background(background_dict,burst_data,time):
    return burst_data-float(background_dict['intercept'])-(time*float(background_dict['slope']))

def norm_time(time):
    return (time-min(time))/(max(time)-min(time))

def norm_data(data):
    return data/max(data)

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


with open(os.path.join('data','burst_info.csv'), newline='') as burstfile:
    base_path = os.path.join('..','batse_data')
    # burst_num,burst_path,single_emission

    # norm
    # if int(row[0]) < 3580:
    # burst_list = [2774,2945,6336,8112,3155] # canonical residual pulses
    # burst_list = [1709,7329] # double peak
    # burst_list = [1159,7599,1145,6870] # triple peak
    # burst_list = [249,6100,7987] # many peak
    # burst_list = [3301,5601,451,8111] # small bump / big bump
    # burst_list = [2443,3491,1717,5451] # broad first residual bump
    # burst_list = [2018,3320,3913] # three bumps on the rise, low s/n
    # burst_list = [6757,7581] # noisy pulse with small bump afterwards
    # burst_list = [467,7766] # tiny bump / fast rise / slow decay

    # euclid
    # burst_list = [918,2880,7987] # canonical singles
    # burst_list = [2254,6414] # canonical singles
    # burst_list = [451,8111] # very clean doubles
    # burst_list = [2980,4814,3294] # semi-noisy pyramid
    # burst_list = [2810,7992,2099] # noisy single
    # burst_list = [3866,7822] # ???? 
    # burst_list = [2458,4312] # triple peak
    # burst_list = [3870,3875,2087,409,5719] # canonical singles 
    # burst_list = [1733,4710] # ????
    # burst_list = [829,1472,1406,2709] # single with second bump
    # burst_list = [2919,3866,7822] # ????

    # opinion: norm is far better at finding unique characteristics than euclid

    # dtw
    # burst_list = [3765,3891] # bright residuals 
    # burst_list = [2611,7446] # bright / bump on decay
    # burst_list = [2431,8050,105] # ????
    # burst_list = [108,1396,2188] # ????
    # burst_list = [6619,1416,5305] # ????
    # burst_list = [6396,2430] # noisy single with bumps
    # burst_list = [6295,2061,3248] # ????



    # corr_norm
    # burst_list = [3248,2315,3091] # ????
    # burst_list = [3292,6295,5654] # ????
    # burst_list = [5716,8079] # singles
    # burst_list = [7187,7775,5711] # ????


    # corr_norm no buffer
    # burst_list = [5654,398]#,6295,1559] # double
    # burst_list = [3248,2709,7614,6039] # sharp / noisy singles
    # burst_list = [6205,7455] # short single
    # burst_list = [7496,973,5571] # ????
    # burst_list = [108,3286,1953] # short noisy double



    # dtw no buffer
    # does not work well with noisy bursts
    # burst_list = [7446,2611,7172] # clean single with trailing bump
    # burst_list = [2151,6904,503] # ????
    # burst_list = [3765,3891,3067,3178] # bright spike on top of other emission
    # burst_list = [3765,3891] # bright spike on top of other emission
    # burst_list = [6100,1085,6630] # bright?
    # burst_list = [2798,3523] # bright with bump
    # burst_list = [7805,8079,2924,7187] # ????
    # burst_list = [1709,8050] # ????
    # burst_list = [2329,7932,1122] # many spikes
    # burst_list = [2431,2799] # canonical residuals
    # burst_list = [5614,3242] # ????



    # norm no buffer
    # burst_list = [6113,6904,2151] # ????
    # burst_list = [7028,7781,7172,5470,2367] # ???? bright stuff
    # burst_list = [4814,6830] # single with cutout in middle
    # burst_list = [1982,3130,3649] # ????
    # burst_list = [467,7766] # sharp rise slow decay
    # burst_list = [7446,2611] # single with bump on back
    # burst_list = [7205,6204,2393,6090] # single with bump on front
    # burst_list = [8121,2603,1406] # canonical single
    # burst_list = [7822,3866,4312,2458] # PULSE EVOLUTION
    # burst_list = [3815,752] # single sharp fall
    # burst_list = [1472,829] # single with dip in middle
    


    # burst_list = [6030,3912,1038,2798] # 
    # burst_list = [5417,1883,5641,7701] # 
    # burst_list = [7671,7602,6182] # 
    # burst_list = [2993,7810,2383] # 
    # burst_list = [7810,2383] # 
    # burst_list = [647,257,7744] # ????
    ################################### burst_list = [7588,6303,7711,1467] # 
    burst_list = [1625,6440,2083] # 
        


    for row in csv.DictReader(burstfile, delimiter=','):
        burst_num = row['burst_num']
        if int(burst_num) in burst_list: 

            time, burst_data, t90_start, t90_end = get_burst_data(burst_num)

            plt.title('Raw Burst Data')
            
            burst_data = remove_background(background_dict[burst_num],burst_data,time)
            burst_data = norm_data(burst_data[(time > float(t90_start)) & (time < float(t90_end))])
            time = norm_time(time[(time > float(t90_start)) & (time < float(t90_end))])

            plt.title('Normalized Emissions')


            plt.plot(time,burst_data, label='Burst '+str(burst_num))
            plt.legend()


plt.show()
