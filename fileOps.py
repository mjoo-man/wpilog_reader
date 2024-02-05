# Code copied from File ops/getFilePath.py on 11-20-2021
from tkinter import filedialog as fd
from tkinter import Tk
from updater import update_progress
import os
import pandas as pd

# function will prompt the user to select a directory and return its absolute path
def getFilePath(message):
	Tk().withdraw()
	filepath = fd.askdirectory()
	return filepath

# filter out non csv files
def getCSVFiles(directory):
	files = os.listdir(directory) # list all files in directory
	filenames = []
	for i in range(len(files)):
		# read only .csv files
		filename, extension =  os.path.splitext(files[i])
		if extension == '.csv': 
			filenames.append(filename+extension)
	return filenames # return only csv paths

def fillWPIlog():
	# get the directory of the logs to be analyzed
	log_dir = getFilePath("Select Folder with the Logs")
	print(log_dir)
	os.chdir(log_dir)
	# for development use
	# log_dir = r"C:\Users\Micah\Desktop\7_28_rolling tests"

	#create save directory if it doesnt already exist
	save_dir = os.path.join(log_dir, "filled_files")
	os.makedirs(save_dir, exist_ok=True)

	filenames = getCSVFiles(log_dir)
	prog = 0
	for file in filenames:
		update_progress(f"Working on {file}", prog/len(filenames))
		prog+=1
		# just read the headers of each file 
		headers = pd.read_csv(file, index_col=0, nrows=0).columns.tolist()

		# read data in the enabled disabled
		run_data = pd.read_csv(file, index_col=0) # timestamp is the index

		fill_data = run_data.fillna(method="ffill") # forward fill all nan with the preceeding number
		fill_data = fill_data.fillna(0.0) # get the first nan to be zero


		#title the file after the first file picked and add merged
		os.chdir(save_dir)
		newName = os.path.basename(file).split(".")[0] + '-filled.csv'
		fill_data.to_csv(newName)
		os.chdir(log_dir)
