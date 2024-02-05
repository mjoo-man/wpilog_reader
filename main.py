from fileOps import fillWPIlog
from plotOps import plotWPILog
from AIAA_ascend import drive_Ang_Speed
from stackingPressures import stackPressures
from pressureSwapping import graphTankPress
def main():

    ''' uncomment to preprocess the wpilog files '''
    # fillWPIlog()

    ''' if logs are already preprocessed plot them for each log and each enable disable cycle'''
    # plotWPILog()

    '''A custom plot to stack pipe responses on pressures'''
    #function defaults to plotting, but if called stackPressures(True) itll return a dictionary with the time values and data
    # stackPressures()

    '''For AIAA ASCEND presentation '''
    # drive_Ang_Speed()

    ''' For robosoft '''
    # graphTankPress()
main()