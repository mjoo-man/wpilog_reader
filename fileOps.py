# Code copied from File ops/getFilePath.py on 11-20-2021
from tkinter import filedialog as fd
from tkinter import Tk

# function will prompt the user to select a directory and return its absolute path
def getFilePath(message):
	Tk().withdraw()
	filepath = fd.askdirectory()
	return filepath
