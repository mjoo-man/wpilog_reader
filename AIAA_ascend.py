import os 
from plotOps import findEnableDisable, getNumPlots, getHeaderstoPlot
from fileOps import getFilePath, getCSVFiles
from updater import update_progress
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def align_yaxis(ax1, v1, ax2, v2):
    """adjust ax2 ylimit so that v2 in ax2 is aligned to v1 in ax1"""
    _, y1 = ax1.transData.transform((0, v1))
    _, y2 = ax2.transData.transform((0, v2))
    inv = ax2.transData.inverted()
    _, dy = inv.transform((0, 0)) - inv.transform((0, y1-y2))
    miny, maxy = ax2.get_ylim()
    ax2.set_ylim(miny+dy, maxy+dy)

def drive_Ang_Speed():
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
               
        des_headers_drive = ['Drive Angle', 'Drive Velocity']
        

        run_data = pd.read_csv(file, index_col=0) # timestamp is the index
        
        print(simple_headers)
        # first plot frive angle 
        

        fig, ax1 = plt.subplots()
        ax2 = ax1.twinx()

        ax1.plot(run_data.index, run_data[headers[3]]*180/np.pi, color='black', label='Pendulum Angle')
        ax2.plot(run_data.index, run_data[headers[4]] , color='blue', label='Robot Speed') # from rad/s to mph
        
        
        plt.title(f"High Speed Robot Driving")
        ax1.set_ylabel("Angle (deg)")
        ax1.set_ylim(-90,90)
        ax2.set_ylabel("Robot Speed (mph)")
        ax1.set_xlabel("time (s)")
        # plt.xticks(np.linspace(0, index_enable[2*i+1]-index_enable[2*i], n))
        plt.grid()
        ax1.legend(loc=2)
        ax2.legend(loc=1)
        align_yaxis(ax1, 0, ax2, 0)
        plt.show()