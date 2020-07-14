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



        # corr_norm
        # if int(row['burst_num']) in [3248,2315,3091]: # ????
        # if int(row['burst_num']) in [3292,6295,5654]: # ????
        # if int(row['burst_num']) in [5716,8079]: # singles
        # if int(row['burst_num']) in [7187,7775,5711]: # ????


        # corr_norm no buffer
        # if int(row['burst_num']) in [5654,398]#,6295,1559]: # double
        # if int(row['burst_num']) in [3248,2709,7614,6039]: # sharp / noisy singles
        # if int(row['burst_num']) in [6205,7455]: # short single
        # if int(row['burst_num']) in [7496,973,5571]: # ????
        # if int(row['burst_num']) in [108,3286,1953]: # short noisy double



        # dtw no buffer
        # does not work well with noisy bursts
        # if int(row['burst_num']) in [7446,2611,7172]: # clean single with trailing bump
        # if int(row['burst_num']) in [2151,6904,503]: # ????
        # if int(row['burst_num']) in [3765,3891,3067,3178]: # bright spike on top of other emission
        #    if int(row['burst_num']) in [3765,3891]: # bright spike on top of other emission
        # if int(row['burst_num']) in [6100,1085,6630]: # bright?
        # if int(row['burst_num']) in [2798,3523]: # bright with bump
        # if int(row['burst_num']) in [7805,8079,2924,7187]: # ????
        # if int(row['burst_num']) in [1709,8050]: # ????
        # if int(row['burst_num']) in [2329,7932,1122]: # many spikes
        # if int(row['burst_num']) in [2431,2799]: # canonical residuals
        # if int(row['burst_num']) in [5614,3242]: # ????



        # norm no buffer
        # if int(row['burst_num']) in [6113,6904,2151]: # ????
        # if int(row['burst_num']) in [7028,7781,7172,5470,2367]: # ???? bright stuff
        # if int(row['burst_num']) in [4814,6830]: # single with cutout in middle
        # if int(row['burst_num']) in [1982,3130,3649]: # ????
        # if int(row['burst_num']) in [467,7766]: # sharp rise slow decay
        # if int(row['burst_num']) in [7446,2611]: # single with bump on back
        # if int(row['burst_num']) in [7205,6204,2393,6090]: # single with bump on front
        # if int(row['burst_num']) in [8121,2603,1406]: # canonical single
        # if int(row['burst_num']) in [7822,3866,4312,2458]: # PULSE EVOLUTION
        # if int(row['burst_num']) in [3815,752]: # single sharp fall
        if int(row['burst_num']) in [1472,829]: # single with dip in middle
            file_path = os.path.join(base_path,row['burst_file'])
            print(file_path)

            grb = Burst(file_path)
            grb.parse_batse_file()

            burst_data = grb.sum_chan_data

            plt.plot(burst_data)
plt.show()
