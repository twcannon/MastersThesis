from grbpy.burst import Burst
import  matplotlib.pyplot as plt 
import csv
import os

with open(os.path.join('data','burst_info.csv'), newline='') as burstfile:
    base_path = os.path.join('..','batse_data')
    for row in csv.DictReader(burstfile, delimiter=','):
        # burst_num,burst_path,single_emission

        # if int(row[0]) < 3580:
        if int(row['burst_num']) == 105 or int(row['burst_num']) == 658:
            file_path = os.path.join(base_path,row['burst_file'])
            print(file_path)

            grb = Burst(file_path)
            grb.parse_batse_file()

            burst_data = grb.sum_chan_data

            plt.plot(burst_data)
plt.show()
