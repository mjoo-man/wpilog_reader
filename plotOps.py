from fileOps import getFilePath, getCSVFiles
from updater import update_progress
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np


def findEnableDisable(data):
    cycles = []
    s = data['NT:/FMSInfo/FMSControlData']
    # while True:
    #     try:
    #         cycles.append(s.idxmax())
    #         cycles.append[s[cycles[-1]::].idxmin()]
    #     except:
    #         break 
    firstenable = s.idxmax()
    return firstenable

def plotWPILog():
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

        simple_headers.index('Ball Pressure (psi)')
        #steering params
        steering = []
        steering.append(simple_headers.index('Pipe Angle'))
        steering.append(simple_headers.index('Pend Angle'))
        # steering.append(simple_headers.index('Commanded Steer Position'))
        # steering.append(simple_headers.index('Current Draw steerMotorB (amps)'))        
        # steering.append(simple_headers.index('NT:/FMSInfo/FMSControlData'))
    
        # read data in the enabled disabled
        run_data = pd.read_csv(file, index_col=0) # timestamp is the index
        # TODO: parse for data i want and plot them together
        
        index_enable = findEnableDisable(run_data)

        fig, ax = plt.subplots()
        for p in steering:
            run_data[headers[p]][index_enable::].plot(label=simple_headers[p])
        plt.legend()
        # ax2 = ax.twinx()
        # # ax2.plot(run_data[headers[simple_headers.index('Ball Pressure (psi)')]], 'r')
        # ax2.set_ylim((0, 6))
        
        plt.show()
        # TODO: crop the data to desirable ranges, plot and save it to combine
        # with the theoretical results
        
        