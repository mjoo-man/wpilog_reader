import numpy as np
from fileOps import getFilePath, getCSVFiles, update_progress
from plotOps import findEnableDisable, getNumPlots, getHeaderstoPlot
import os
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

def get_angle(num_plates):

    Ramp_Length = 82 # in
    Plate_Height = 1.125 # in
    ang = np.arcsin(Plate_Height*num_plates / Ramp_Length)

    return round(ang*180/np.pi, 2)
def ramp_data(saveData=False):
    # get the directory of the logs to be analyzed
    log_dir = getFilePath("Select Folder with the Logs to Plot")

    os.chdir(log_dir)

    data_for_csv = {}
    #


    filenames = getCSVFiles(log_dir)
    for file in filenames:

        save_dir = os.path.join(log_dir, f"{file[:6]} ballast peak_data")
        os.makedirs(save_dir, exist_ok=True)

        # just read the headers of each file
        headers = pd.read_csv(file, index_col=0, nrows=0).columns.tolist()

        simple_headers = [headers[i].replace("NT:/SmartDashboard/", "") for i in range(len(headers))]
        print(simple_headers)
        # des_headers = ['Commanded Drive Velocity', 'Drive Velocity', 'Drive Angle', 'Pitch Speed', 'NumPlates']
        des_headers = ['CMD Drive Velocity', 'Drive Velocity', 'Drive Angle', 'NumPlates']
        ramp_idx = simple_headers.index('NumPlates')
        run_data = pd.read_csv(file, index_col=0)  # timestamp is the index

        # convert drive angle to degrees
        run_data['NT:/SmartDashboard/Drive Angle'] = - run_data['NT:/SmartDashboard/Drive Angle'] * 180 / np.pi

        index_enable = findEnableDisable(run_data)
        numPlots = getNumPlots(index_enable)

        ax = run_data.plot()

        # plot desired curves
        for i in range(numPlots):
            update_progress(f"Working on plot {i} of {numPlots}", i/numPlots)

            startTime = index_enable[2 * i]
            fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
            # ax2 = ax1.twinx()

            try:
                # Plot drive_angle on ax1
                idx = simple_headers.index('Drive Angle')
                new = pd.DataFrame(run_data[headers[idx]][index_enable[2 * i]:index_enable[2 * i + 1]])
                # new = new.set_index(new.index.values - startTime)
                ax1.plot(new, color='green', label=simple_headers[idx])
                peak_idx, heights = find_peaks(new.values.transpose()[0], height=1, prominence=2)
                ax1.scatter(new.index[peak_idx], heights['peak_heights'], marker='x')
                # save the found peaks to a dataframe for later
                data_for_csv[f'figure {i+2} peaks'] = heights['peak_heights']
                data_for_csv[f'figure {i + 2} time'] = new.index[peak_idx].values

                for p in [simple_headers.index(x) for x in ['CMD Drive Velocity', 'Drive Velocity']]: # plot cmd dive vel and drive vel on ax2
                    new = pd.DataFrame(run_data[headers[p]][index_enable[2 * i]:index_enable[2 * i + 1]])
                    # new = new.set_index(new.index.values - startTime)
                    ax2.plot(new, label=simple_headers[p])
                    # if p == 2:
                    #     data_for_csv[f'figure {i + 1} commanded drive velocity'] = new.values[peak_idx]
            except IndexError:
                # if index happens to be out of range, plot the remainder of the file
                # plot drive angle on ax1
                idx = simple_headers.index('Drive Angle')
                new = pd.DataFrame(run_data[headers[idx]][index_enable[2 * i]::])
                # new.set_index(new.index.values - startTime)
                ax1.plot(new, color='green', label=simple_headers[idx])
                # save data to file
                peak_idx, heights = find_peaks(new.values.transpose()[0], height=1)
                ax1.scatter(new.index[peak_idx], heights['peak_heights'], marker='x')
                data_for_csv[f'figure {i + 2} peaks'] = heights['peak_heights']
                data_for_csv[f'figure {i + 2} time'] = new.index[peak_idx].values

                for p in [simple_headers.index(x) for x in ['CMD Drive Velocity', 'Drive Velocity']]: # plot cmd dive vel and drive vel on ax2
                    new = pd.DataFrame(run_data[headers[p]][index_enable[2 * i]::])
                    # new = new.set_index(new.index.values - startTime)
                    ax2.plot(new, label=simple_headers[p])
                    # data_for_csv[f'figure {i + 1} commanded drive velocity'] = new.values[peak_idx]
            try:
                runRamp = run_data[headers[ramp_idx]][startTime:index_enable[2 * i + 1]].median()
            except IndexError:
                runRamp = run_data[headers[ramp_idx]][startTime::].median()



            ax1.set_title(f"{file[:6]} Ballast Ramp at {get_angle(runRamp)} degrees")
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
            # pd.DataFrame(data=data_for_csv).to_csv(f"Figure {i+2} of {file[:5]} base peaks ramp at {get_angle(runRamp)}.csv")
            # data_for_csv = {} # clear the dict after everything is saved
            # plt.savefig(f"Figure {i+2} plot {file[:5]} base peaks ramp at {get_angle(runRamp)}.png")
            # os.chdir(log_dir)
        # plt.show()

ramp_data()