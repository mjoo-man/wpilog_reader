import numpy as np
from fileOps import getFilePath, getCSVFiles, update_progress
from plotOps import findEnableDisable, getNumPlots, getHeaderstoPlot
import os
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

def plot_wobbles(saveData=False):
    # get the directory of the logs to be analyzed
    log_dir = getFilePath("Select Folder with the Logs to Plot")

    os.chdir(log_dir)

    data_for_csv = {}

    save_dir = os.path.join(log_dir, "peak_data")
    os.makedirs(save_dir, exist_ok=True)

    filenames = getCSVFiles(log_dir)
    for file in filenames:


        # just read the headers of each file
        headers = pd.read_csv(file, index_col=0, nrows=0).columns.tolist()

        simple_headers = [headers[i].replace("NT:/SmartDashboard/", "") for i in range(len(headers))]

        des_headers = ['Drive Velocity', 'Pipe Angle']

        run_data = pd.read_csv(file, index_col=0)  # timestamp is the index

        # convert pipe angle to degrees
        run_data['NT:/SmartDashboard/Pipe Angle'] = run_data['NT:/SmartDashboard/Pipe Angle'] * 180 / np.pi

        index_enable = findEnableDisable(run_data)
        numPlots = getNumPlots(index_enable)
        press_index = simple_headers.index('Ball Pressure (psi)')

        ax = run_data.plot()

        # plot desired curves
        for i in range(numPlots):
            update_progress(f"Working on plot {i} of {numPlots} in file: {file}", i/numPlots)

            startTime = index_enable[2 * i]
            fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
            # ax2 = ax1.twinx()
            '''
            p = 2 for cmd vrive vel
            p = 4 for drive vel
            p = 5 for pipe angle
            '''
            try:
                # Plot pipe on ax1
                idx = simple_headers.index('Pipe Angle')
                new = pd.DataFrame(run_data[headers[idx]][index_enable[2 * i]:index_enable[2 * i + 1]])
                # new = new.set_index(new.index.values - startTime)
                ax1.plot(new, color='green', label=simple_headers[idx])
                # peak_idx, heights = find_peaks(new.values.transpose()[0], height=-1, prominence=0.5)
                # ax1.scatter(new.index[peak_idx], heights['peak_heights'], marker='x')
                # # save the found peaks to a dataframe for later
                # data_for_csv[f'figure {i+2} peaks'] = heights['peak_heights']
                # data_for_csv[f'figure {i + 2} time'] = new.index[peak_idx]

                for p in [simple_headers.index(x) for x in ['Drive Velocity']]: # plot cmd dive vel and drive vel on ax2
                    new = pd.DataFrame(run_data[headers[p]][index_enable[2 * i]:index_enable[2 * i + 1]])
                    # new = new.set_index(new.index.values - startTime)
                    ax2.plot(new, label=simple_headers[p])
                    # if p == 2:
                    #     data_for_csv[f'figure {i + 1} commanded drive velocity'] = new.values[peak_idx]
            except IndexError:
                # if index happens to be out of range, plot the remainder of the file
                # plot pipe on ax1
                new = pd.DataFrame(run_data[headers[idx]][index_enable[2 * i]::])
                # new.set_index(new.index.values - startTime)
                ax1.plot(new, color='green', label=simple_headers[idx])
                # save data to file
                # peak_idx, heights = find_peaks(new.values.transpose()[0], height=-1, prominence=0.5)
                # ax1.scatter(new.index[peak_idx], heights['peak_heights'], marker='x')
                # data_for_csv[f'figure {i + 2} peaks'] = heights['peak_heights']
                # data_for_csv[f'figure {i + 2} time'] = new.index[peak_idx]

                for p in [simple_headers.index(x) for x in ['Drive Velocity']]:
                    new = pd.DataFrame(run_data[headers[p]][index_enable[2 * i]::])
                    # new = new.set_index(new.index.values - startTime)
                    ax2.plot(new, label=simple_headers[p])
                    # data_for_csv[f'figure {i + 1} commanded drive velocity'] = new.values[peak_idx]
            try:
                runPressure = round(run_data[headers[press_index]][startTime:index_enable[2 * i + 1]].mean(), 2)
            except IndexError:
                runPressure = round(run_data[headers[press_index]][index_enable[2 * i]::].mean(), 2)
            # plt.title(f"Response at {runPressure} psi")
            # n = len(run_data[headers[0]][index_enable[2*i]:index_enable[2*i+1]])
            # print(f"Response at {runPressure} psi")

            # ax = plt.axes()
            # ax.xaxis.set_major_formatter(lambda x, pos: x /2)

            ax1.set_title(f"Robot Response at {runPressure}psi")
            ax1.set_ylabel("Angle (deg)")
            ax2.set_ylabel("rad/s")
            ax2.set_xlabel("time (s)")
            # plt.xticks(np.linspace(0, index_enable[2*i+1]-index_enable[2*i], n))
            ax1.grid()
            ax2.grid()
            ax1.legend()
            ax2.legend()
            # align_yaxis(ax1, 0, ax2, 0)
            # os.chdir(save_dir)
            # pd.DataFrame(data=data_for_csv).to_csv(f"Figure {i+2} data Regular.csv")
            # data_for_csv = {} # clear the dict after everything is saved
            # os.chdir(log_dir)
        plt.show()

plot_wobbles()