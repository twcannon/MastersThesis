from grbpy.burst import Burst
import  matplotlib.pyplot as plt 
import csv
import os

with open(os.path.join('data','burst_info.csv'), newline='') as burstfile:
    base_path = os.path.join('..','batse_data')
    for row in csv.DictReader(burstfile, delimiter=','):
        # burst_num,burst_path,single_emission

        # if int(row[0]) < 3580:
        # if int(row['burst_num']) in [1709,7329]: # double peak
        # if int(row['burst_num']) in [1159,7599,1145,6870]: # triple peak
        # if int(row['burst_num']) in [249,6100,7987]: # many peak
        # if int(row['burst_num']) in [3301,5601,451,8111]: # small bump / big bump
        # if int(row['burst_num']) in [2443,3491,1717,5451]: # broad first residual bump
        # if int(row['burst_num']) in [2018,3320,3913]: # three bumps on the rise, low s/n
        if int(row['burst_num']) in [6757,7581]: # noisy pulse with small bump afterwards
            file_path = os.path.join(base_path,row['burst_file'])
            print(file_path)

            grb = Burst(file_path)
            grb.parse_batse_file()

            burst_data = grb.sum_chan_data

            plt.plot(burst_data)
plt.show()
