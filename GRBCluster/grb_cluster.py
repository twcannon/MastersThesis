import scipy
from grbpy.burst import Burst
import  matplotlib.pyplot as plt 
import csv
print('works')

with open('/home/thomas/data/batse/ascii_data/64ms/burst_files.csv', newline='') as burstfile:
    base_path = '/home/thomas/data/batse/ascii_data/64ms/'
    for row in csv.reader(burstfile, delimiter=' ', quotechar='|'):
        file_path = base_path+row[1]
        print(file_path)

        grb = Burst(file_path)
        grb.parse_batse_file()

        burst_data = grb.burst_data

        plt.plot(burst_data)
        plt.show()
