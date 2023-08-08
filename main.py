from fileOps import fillWPIlog
from plotOps import plotWPILog
from stackingPressures import stackPressures

def main():

    ''' uncomment to preprocess the wpilog files '''
    # fillWPIlog()

    ''' if logs are already preprocessed plot them for each log and each enable diable cycle'''
    # plotWPILog()

    '''A custom plot to stack pipe responses on pressures'''
    #function defaults to plotting, but if called stackPressures(True) itll return a dictionary with the time values and data
    stackPressures()

main()