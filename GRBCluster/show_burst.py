from grbpy.burst import Burst
import  matplotlib.pyplot as plt 
import csv
import os

with open(os.path.join('data','burst_info.csv'), newline='') as burstfile:
    base_path = os.path.join('..','batse_data')
    for row in csv.DictReader(burstfile, delimiter=','):
        # burst_num,burst_path,single_emission

        # norm
        # if int(row[0]) < 3580:
        # if int(row['burst_num']) in [2774,2945,6336,8112,3155]: canonical residual pulses
        # if int(row['burst_num']) in [1709,7329]: # double peak
        # if int(row['burst_num']) in [1159,7599,1145,6870]: # triple peak
        # if int(row['burst_num']) in [249,6100,7987]: # many peak
        # if int(row['burst_num']) in [3301,5601,451,8111]: # small bump / big bump
        # if int(row['burst_num']) in [2443,3491,1717,5451]: # broad first residual bump
        # if int(row['burst_num']) in [2018,3320,3913]: # three bumps on the rise, low s/n
        # if int(row['burst_num']) in [6757,7581]: # noisy pulse with small bump afterwards
        # if int(row['burst_num']) in [467,7766]: # tiny bump / fast rise / slow decay

        # euclid
        # if int(row['burst_num']) in [918,2880,7987]: # canonical singles
        # if int(row['burst_num']) in [2254,6414]: # canonical singles
        # if int(row['burst_num']) in [451,8111]: # very clean doubles
        # if int(row['burst_num']) in [2980,4814,3294]: # semi-noisy pyramid
        # if int(row['burst_num']) in [2810,7992,2099]: # noisy single
        # if int(row['burst_num']) in [3866,7822]: # ???? 
        # if int(row['burst_num']) in [2458,4312]: # triple peak
        # if int(row['burst_num']) in [3870,3875,2087,409,5719]: # canonical singles 
        # if int(row['burst_num']) in [1733,4710]: # ????
        # if int(row['burst_num']) in [829,1472,1406,2709]: # single with second bump
        # if int(row['burst_num']) in [2919,3866,7822]: # ????

        # opinion: norm is far better at finding unique characteristics than euclid

        # dtw
        # if int(row['burst_num']) in [3765,3891]: # bright residuals 
        # if int(row['burst_num']) in [2611,7446]: # bright / bump on decay
        # if int(row['burst_num']) in [2431,8050,105]: # ????
        # if int(row['burst_num']) in [108,1396,2188]: # ????
        # if int(row['burst_num']) in [6619,1416,5305]: # ????
        # if int(row['burst_num']) in [6396,2430]: # noisy single with bumps
        # if int(row['burst_num']) in [6295,2061,3248]: # ????
        if int(row['burst_num']) in [2924,6205,1298]: # noisy single with bumps
            file_path = os.path.join(base_path,row['burst_file'])
            print(file_path)

            grb = Burst(file_path)
            grb.parse_batse_file()

            burst_data = grb.sum_chan_data

            plt.plot(burst_data)
plt.show()
