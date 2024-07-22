import numpy as np
from fileOps import getFilePath, getCSVFiles, update_progress
from plotOps import findEnableDisable, getNumPlots, getHeaderstoPlot
import os
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks, butter, filtfilt

# filter the tank pressure data
fs = 1000  # Sampling frequency
fc = 5  # Cut-off frequency of the filter
w = fc / (fs / 2)  # Normalize the frequency
b, a = butter(5, w, 'low')

def pressure_control_data():
    # get the directory of the logs to be analyzed
    log_dir = getFilePath("Select Folder with the Logs to Plot")

    os.chdir(log_dir)

    filenames = getCSVFiles(log_dir)
    for file in filenames:

        # just read the headers of each file
        headers = pd.read_csv(file, index_col=0, nrows=0).columns.tolist()

        simple_headers = [headers[i].replace("NT:/SmartDashboard/", "") for i in range(len(headers))]
        print(simple_headers)
        # des_headers = ['Commanded Drive Velocity', 'Drive Velocity', 'Drive Angle', 'Pitch Speed', 'NumPlates']
        des_headers = ['Ball Pressure (psi)', 'Tank Pressure (psi)', 'pressure setpoint']

        run_data = pd.read_csv(file, index_col=0)  # timestamp is the index


        index_enable = findEnableDisable(run_data)
        numPlots = getNumPlots(index_enable)

        ax = run_data.plot()

        list_fig_obj = []
        list_fig2_obj =[]
        list_ax1_obj = []
        list_ax2_obj = []

        # plot desired curves
        for i in range(numPlots):
            update_progress(f"Working on plot {i} of {numPlots} in file {file}", i/numPlots)

            startTime = index_enable[2 * i]

            fig, ax1 = plt.subplots()
            fig2, ax2 = plt.subplots()
            try:
                # Plot ball Pressure and setpoint on ax1
                idx = simple_headers.index(des_headers[0]) # index for ball pressure
                new = pd.DataFrame(run_data[headers[idx]][index_enable[2 * i]:index_enable[2 * i + 1]])
                new = new.set_index(new.index.values - startTime)
                ax1.plot(new, color='black', label=simple_headers[idx])

                idx = simple_headers.index(des_headers[2])  # index for ball pressure setpoint
                new = pd.DataFrame(run_data[headers[idx]][index_enable[2 * i]:index_enable[2 * i + 1]])
                new = new.set_index(new.index.values - startTime)
                ax1.plot(new, 'k--', label=simple_headers[idx])

                idx = simple_headers.index(des_headers[1])  # index for tank pressure setpoint
                new = pd.DataFrame(run_data[headers[idx]][index_enable[2 * i]:index_enable[2 * i + 1]])
                new = new.set_index(new.index.values - startTime)
                ax2.plot(new.index, filtfilt(b, a, new.values.transpose()[0]), 'b', label=simple_headers[idx])

            except IndexError:
                # if index happens to be out of range, plot the remainder of the file
                # plot ball pressure and setpoint on ax1
                idx = simple_headers.index(des_headers[0])
                new = pd.DataFrame(run_data[headers[idx]][index_enable[2 * i]::])
                new.set_index(new.index.values - startTime)
                ax1.plot(new, 'k', label=simple_headers[idx])

                idx = simple_headers.index(des_headers[2])
                new = pd.DataFrame(run_data[headers[idx]][index_enable[2 * i]::])
                new.set_index(new.index.values - startTime)
                ax1.plot(new, 'k--', label=simple_headers[idx])
                # plot tank pressure on other axis
                idx = simple_headers.index(des_headers[1])
                new = pd.DataFrame(run_data[headers[idx]][index_enable[2 * i]::])
                new.set_index(new.index.values - startTime)
                ax2.plot(new.index, filtfilt(b, a, new.values.transpose()[0]), 'b', label=simple_headers[idx])

            list_fig_obj.append(fig)
            list_fig2_obj.append(fig2)
            list_ax1_obj.append(ax1)
            list_ax2_obj.append(ax2)

    return list_fig_obj, list_ax1_obj, list_fig2_obj, list_ax2_obj


