# Code copied from File ops/getFilePath.py on 11-20-2021
from tkinter import filedialog as fd
from tkinter import Tk

import os

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