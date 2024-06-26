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

    # handle a binary copy error
    done = False
    while not done: # rewrite any binary errors
        if s.loc[s.idxmax()] > 33:
            s.loc[s.idxmax()] = 32.0
        else:
            done = not done
    cycles.append(s.idxmax())
    while True:
        if len(cycles)%2 == 0 and len(cycles)>1:
            cycles.append(s[cycles[-1]::].idxmax())
        else:
            cycles.append(s[cycles[-1]::].idxmin())

        if (cycles[-1] == cycles[-2]) and (len(cycles)>=2):
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

def plotWPILog(saveData=False):
    # get the directory of the logs to be analyzed
    log_dir = getFilePath("Select Folder with the Logs to Plot")

    os.chdir(log_dir)

    data_for_csv = {}
    if saveData:
        save_dir = os.path.join(log_dir, "split_files")
        os.makedirs(save_dir, exist_ok=True)

    filenames = getCSVFiles(log_dir)
    prog = 0
    for file in filenames:
        update_progress(f"Working on {file}", prog/len(filenames))
        prog+=1
        
        # just read the headers of each file 
        headers = pd.read_csv(file, index_col=0, nrows=0).columns.tolist()

        simple_headers = [headers[i].replace("NT:/SmartDashboard/", "") for i in range(len(headers))]
               
        des_headers_drive = ['Commanded Drive Velocity', 'Drive Velocity']
        des_headers_pipe = ['Pipe Angle']

        run_data = pd.read_csv(file, index_col=0) # timestamp is the index

        run_data['NT:/SmartDashboard/Pipe Angle'] = run_data['NT:/SmartDashboard/Pipe Angle'] * 180 / np.pi

        index_enable = findEnableDisable(run_data)
        numPlots = getNumPlots(index_enable)
        press_index = simple_headers.index('Ball Pressure (psi)')

        ax = run_data.plot()
        for d in [des_headers_drive, des_headers_pipe]:
            idx_plot_headrs = getHeaderstoPlot(simple_headers, d)

            # plot desired curves
            for i in range(numPlots):
                startTime = index_enable[2*i]
                plt.figure()
                for p in idx_plot_headrs: # for each data stream
                    # run_data[headers[p]] = -run_data[headers[p]] # flip the signs
                    # run_data[headers[p]] = 180/np.pi*run_data[headers[p]] # flip the signs
        
                    try:
                       new = pd.DataFrame(run_data[headers[p]][index_enable[2*i]:index_enable[2*i+1]])
                       new = new.set_index(new.index.values - startTime)
                       plt.plot(new, label=simple_headers[p])
                       data_for_csv[simple_headers[p]] = new.values
                       data_for_csv['time'] = new.index
                    except IndexError:
                        # if index happens to be out of range, plot the remainder of the file
                        new = pd.DataFrame(run_data[headers[p]][index_enable[2*i]::])
                        new.set_index(new.index.values - startTime)
                        plt.plot(new, label=simple_headers[p])
                        data_for_csv[simple_headers[p]] = new.values
                        data_for_csv['time'] = new.index
                try:
                    runPressure = round(run_data[headers[press_index]][startTime:index_enable[2*i+1]].mean(), 2)
                except IndexError:
                    runPressure = round(run_data[headers[press_index]][index_enable[2*i]::].mean(), 2)
                # plt.title(f"Response at {runPressure} psi")
                # n = len(run_data[headers[0]][index_enable[2*i]:index_enable[2*i+1]])
                # print(f"Response at {runPressure} psi")
                
                # ax = plt.axes()
                # ax.xaxis.set_major_formatter(lambda x, pos: x /2)
                

                plt.title(f"Robot Steering Reponse at {runPressure}psi")
                plt.ylabel("Angle (deg)")
                plt.xlabel("time (s)")
                # plt.xticks(np.linspace(0, index_enable[2*i+1]-index_enable[2*i], n))
                plt.grid()
                plt.legend()
        
        # old code for checking
        # plt.figure(99)
        # for p in headers:
        #     run_data[p].plot(label=p.replace("NT:/SmartDashboard/", ""))
        # plt.legend()

        # pd.DataFrame(data=data_for_csv, index=data_for_csv['time']).to_csv(f"data_for {runPressure}.csv")
        plt.show()
        
        