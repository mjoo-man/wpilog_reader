from fileOps import fillWPIlog
from plotOps import plotWPILog
from stackingPressures import stackPressures

def main():

    ''' uncomment to preprocess the wpilog files '''
    # fillWPIlog()

    ''' if logs are already preprocessed plot them for each log and each enable diable cycle'''
    # plotWPILog()

    '''A custom plot to stack pipe responses on pressures'''
    stackPressures()

main()