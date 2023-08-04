from fileOps import fillWPIlog
from plotOps import plotWPILog

def main():

    ''' uncomment to preprocess the wpilog files '''
    # fillWPIlog()

    ''' if logs are already preprocessed plot them '''
    plotWPILog()

main()