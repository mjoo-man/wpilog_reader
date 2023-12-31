from fileOps import getFilePath, getCSVFiles
from updater import update_progress
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
import sys 

def getHeaderstoPlot(simple_headers, des_headers):
    idx_of_des_headers = []
    for h in des_headers:
        try:
            idx_of_des_headers.append(simple_headers.index(h))

        except ValueError as e:
            print("ERROR: ", e)
            continue
    return idx_of_des_headers

def findEnableDisable(data):
    cycles = []
    s = data['NT:/FMSInfo/FMSControlData']
    cycles.append(s.idxmax())
    while True:
        if len(cycles)%2 == 0 and len(cycles)>1:
            cycles.append(s[cycles[-1]::].idxmax())
        else:
            cycles.append(s[cycles[-1]::].idxmin())
         
        if (cycles[-1] == cycles[-2]) and (len(cycles)>=3):
            # if the find thing starts repeating, we're done pop the last element and move on
            cycles.pop(-1)
            break 
    
    return cycles

def getNumPlots(cycles):
    n = len(cycles)
    numPlots = 0
    if n%2>0:
        numPlots = n//2 +1
    else:
        numPlots = n//2
    return numPlots

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
               
        des_headers_drive = ['Drive Angle', 'Commanded Drive Velocity', 'Drive Velocity']
        des_headers_pipe = ['Pipe Angle', 'Pend Angle', 'Commanded Steer Position']

        # read data in the enabled disabled
        run_data = pd.read_csv(file, index_col=0) # timestamp is the index
        # TODO: parse for data i want and plot them together
        index_enable = findEnableDisable(run_data)
        numPlots = getNumPlots(index_enable)
        press_index = simple_headers.index('Ball Pressure (psi)')

        for d in [des_headers_drive, des_headers_pipe]:
            idx_plot_headrs = getHeaderstoPlot(simple_headers, d)

            # plot desired curves
            for i in range(numPlots):
                plt.figure()
                for p in idx_plot_headrs: # for each data stream
                    try:
                        run_data[headers[p]][index_enable[2*i]:index_enable[2*i+1]].plot(label=simple_headers[p])
                    except IndexError:
                        # if index happens to be out of range, plot the remainder of the file
                        run_data[headers[p]][index_enable[2*i]::].plot(label=simple_headers[p])
                try:
                    runPressure = round(run_data[headers[press_index]][index_enable[2*i]:index_enable[2*i+1]].mean(), 2)
                except IndexError:
                    runPressure = round(run_data[headers[press_index]][index_enable[2*i]::].mean(), 2)
                plt.title(f"Response at {runPressure} psi")
                plt.grid()
                plt.legend()
        
        # old code for checking
        plt.figure(99)
        for p in headers:
            run_data[p].plot(label=p.replace("NT:/SmartDashboard/", ""))
        plt.legend()
        plt.show()
        # TODO: crop the data to desirable ranges, plot and save it to combine
        # with the theoretical results
        
        