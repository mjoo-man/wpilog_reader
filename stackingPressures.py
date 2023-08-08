from fileOps import getFilePath, getCSVFiles
from updater import update_progress
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
from plotOps import findEnableDisable, getNumPlots


def stackPressures():
    # get the directory of the logs to be analyzed
    log_dir = getFilePath("Select Folder with the Logs to Plot")

    os.chdir(log_dir)

    filenames = getCSVFiles(log_dir)
    prog = 0

    allData = {}
    colors = ['r', 'y', 'g', 'b', ]
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
        # steering.append(simple_headers.index('Pend Angle'))
        # steering.append(simple_headers.index('Ball Pressure (psi)'))
        # steering.append(simple_headers.index('Commanded Steer Position'))
                
        # steering.append(simple_headers.index('NT:/FMSInfo/FMSControlData'))
    
        # read data in the enabled disabled
        run_data = pd.read_csv(file, index_col=0) # timestamp is the index
        # TODO: parse for data i want and plot them together
        
        index_enable = findEnableDisable(run_data)
        numPlots = getNumPlots(index_enable)
        press_index = simple_headers.index('Ball Pressure (psi)')
        
        # pull data from each run each plot is a run
        for i in range(numPlots):
            
            try:
                n = run_data['NT:/SmartDashboard/Pipe Angle'][index_enable[2*i]:index_enable[2*i+1]].to_numpy()
                ntime = np.linspace(0,index_enable[2*i+1] - index_enable[2*i], len(n))

                nPress = round(run_data[headers[press_index]][index_enable[2*i]:index_enable[2*i+1]].mean(), 2)
                allData[nPress] = [n, ntime]
            except IndexError:
                # if index happens to be out of range, plot the remainder of the file
                n= run_data['NT:/SmartDashboard/Pipe Angle'][index_enable[2*i]::].to_numpy()
                ntime = np.linspace(0,run_data.last_valid_index() - index_enable[2*i], len(n))

                nPress = round(run_data[headers[press_index]][index_enable[2*i]::].mean(), 2)
                allData[nPress] = [n, ntime]

    plt.figure(1)
    ax = plt.axes()
    colors = plt.cm.jet(np.linspace(0,1,len(allData.keys())))
    for i in range(len(allData.keys())):
        n = list(allData.keys())[i]
        t = allData[n][1]
        data = allData[n][0]
        plt.plot(t, data/data[0], color=colors[i], label=str(n)+' psi')
    plt.legend()
    ax.set_facecolor('gray')
    # ax.xaxis.set_major_formatter(lambda x, pos: str(x/200))
    plt.ylabel("Angle / Starting Angle")
    plt.title("Pipe Response at Different Pressures")
    plt.xlabel("time (s)")
    plt.grid()

    # plt.figure(2)
    # ax = plt.axes()
    # des_press = [0.98, 1.48, 2.04, 2.96, 3.47, 4.99, 5.46]
    # colors = plt.cm.jet(np.linspace(0,1,len(des_press)))
    # for i in range(len(des_press)):
    #     n = des_press[i]
    #     plt.plot(allData[n]/allData[n][0], color=colors[i], label=str(n)+' psi')
    # plt.legend()
    # ax.set_facecolor('gray')
    # # ax.xaxis.set_major_formatter(lambda x, pos: str(x/200))
    # plt.grid()
    # plt.ylabel("Angle / Starting Angle")
    # plt.title("Pipe Response at Different Pressures")
    # plt.xlabel("Sample")
    plt.show()

        