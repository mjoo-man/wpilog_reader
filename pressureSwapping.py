import os 
from plotOps import findEnableDisable, getNumPlots, getHeaderstoPlot
from fileOps import getFilePath, getCSVFiles
from updater import update_progress
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

def align_yaxis(ax1, v1, ax2, v2):
    """adjust ax2 ylimit so that v2 in ax2 is aligned to v1 in ax1"""
    _, y1 = ax1.transData.transform((0, v1))
    _, y2 = ax2.transData.transform((0, v2))
    inv = ax2.transData.inverted()
    _, dy = inv.transform((0, 0)) - inv.transform((0, y1-y2))
    miny, maxy = ax2.get_ylim()
    ax2.set_ylim(miny+dy, maxy+dy)

def graphTankPress():
    # get the directory of the logs to be analyzed
    log_dir = getFilePath("Select Folder with the Logs to Plot")

    os.chdir(log_dir)

    filenames = getCSVFiles(log_dir)
    prog = 0
    for file in filenames:
        update_progress(f"Working on {file}", prog/len(filenames))
        prog+=1
        
        # just read the headers of each file 
        headers = pd.read_csv(file, index_col=0, nrows=0).columns.tolist()

        simple_headers = [headers[i].replace("NT:/SmartDashboard/", "") for i in range(len(headers))]
               
        des_headers_drive = ['Ball Pressure (psi)',	'Ball Pressure MPRLS (psi)', 'Tank Pressure (psi)']

        

        run_data = pd.read_csv(file, index_col=0) # timestamp is the index
        
        print(simple_headers)
        # first plot frive angle 
        

        fig, ax1 = plt.subplots()
        ax2 = ax1.twinx()

        # filter the tank pressure data
        fs = 1000  # Sampling frequency
        fc = 5  # Cut-off frequency of the filter
        w = fc / (fs / 2) # Normalize the frequency
        b, a = signal.butter(5, w, 'low')
        filt_tank = signal.filtfilt(b, a, run_data[headers[3]])
        shell_press = run_data[headers[1]].values

        ax1.plot(run_data.index.values, shell_press , color='black', label='Shell Pressure (psi)')
        ax2.plot(run_data.index.values, filt_tank, color='blue', label='Tank Pressure (psi)') # from rad/s to mph
        
        
        plt.title("Changing Ball and Tank Pressure")
        ax1.set_ylabel("Ball Pressure (psi)")
        ax1.set_ylim(0,6)
        ax2.set_ylabel("Tank Pressure (psi)")
        ax1.set_xlabel("time (s)")
        # plt.xticks(np.linspace(0, index_enable[2*i+1]-index_enable[2*i], n))
        plt.grid()
        ax1.legend(loc=2)
        ax2.legend(loc=1)
        align_yaxis(ax1, 0, ax2, 0)
        plt.show()