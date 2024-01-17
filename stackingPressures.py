from pickle import FALSE
from fileOps import getFilePath, getCSVFiles
from updater import update_progress
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
from plotOps import findEnableDisable, getNumPlots

def find_risetime(data): # data is a list of form [data values, time]
    def find_nearest(array, value):
        array = np.asarray(array)
        idx = (np.abs(array - value)).argmin()
        return array[idx]
    
    t = list(data[1])
    x = list(data[0])
    end = t.index(find_nearest(t,15)) # crop data to ~15 seconds
    t = t[0:end]
    x = x[0:end]
    # find ss position of last ten values
    x0 = x[0]
    ss = np.average(x[-1])
    rise_val =  x0 - 0.95*(x0 - ss)
    
    
    rise_val = find_nearest(x, rise_val)
    return t[x.index(rise_val)], rise_val

def sortPressures(myDict):
    myKeys = list(myDict.keys())
    myKeys.sort()
    sorted_dict = {i: myDict[i] for i in myKeys}
    return sorted_dict

def stackPressures(return_data=False):
    # get the directory of the logs to be analyzed
    log_dir = getFilePath("Select Folder with the Logs to Plot")

    os.chdir(log_dir)

    filenames = getCSVFiles(log_dir)
    prog = 0

    allData = {}

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
    
    allData = sortPressures(allData)

    if (not return_data):
        plt.figure(1)
        ax = plt.axes()
        colors = plt.cm.jet(np.linspace(0,1,len(allData.keys())))
        for i in range(len(allData.keys())):
            n = list(allData.keys())[i]
            t = allData[n][1]
            data = allData[n][0]
            plt.plot(t, data, color=colors[i], label=str(n)+' psi')
            # x, y = find_risetime([data, t])
            # plt.scatter(x, y, color=colors[i])
        # plt.legend()
        ax.set_facecolor('gray')
        plt.ylabel("Angle")
        plt.title("Pipe Response at Different Pressures")
        plt.xlabel("time (s)")
        plt.grid()

        plt.figure(2)
        ax = plt.axes()
        for i in range(len(allData.keys())):
            n = list(allData.keys())[i]
            t = allData[n][1]
            data = allData[n][0]/allData[n][0][0]
            plt.plot(t, data, color=colors[i], label=str(n)+' psi')
            # x, y = find_risetime([data, t])
            # plt.scatter(x, y, color=colors[i])
        plt.legend()
        ax.set_facecolor('gray')
        plt.ylabel("Angle")
        plt.title("Normalized Pipe Response at Different Pressures")
        plt.xlabel("time (s)")
        plt.grid()
       
        plt.show()
    else:
        return allData
        