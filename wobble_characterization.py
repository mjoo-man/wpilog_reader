import numpy as np
from fileOps import getFilePath, getCSVFiles, update_progress
import os
import pandas as pd
import matplotlib.pyplot as plt

def analyze_wobble():

    # get the directory of the logs to be analyzed
    log_dir = getFilePath("Select Folder with the Logs to Plot")

    os.chdir(log_dir)

    filenames = getCSVFiles(log_dir)
    prog = 0
    for file in filenames:
        update_progress(f"Working on {file}", prog / len(filenames))
        prog += 1

        # just read the headers of each file
        headers = pd.read_csv(file, index_col=0, nrows=0).columns.tolist()

        simple_headers = [headers[i].replace("NT:/SmartDashboard/", "") for i in range(len(headers))]

        des_headers = ['Drive Angle', 'Commanded Drive Velocity', 'Drive Velocity', 'Pipe Angle', 'Ball Pressure (psi)']
        des_headers_index = [simple_headers.index(i) for i in des_headers]
        print(des_headers_index)
        des_full_headers = [headers[i] for i in des_headers_index]
        run_data = pd.read_csv(file, index_col=0)  # timestamp is the index

        pressure = run_data[headers[1]].to_numpy()
        cmdDriveVel = run_data[headers[2]].to_numpy()
        driveVel = run_data[headers[5]].to_numpy()
        pipeAngle = run_data[headers[6]].to_numpy()

        index = np.where(cmdDriveVel > 0.2 and cmdDriveVel < -0.2)

        np.plot()

analyze_wobble()
