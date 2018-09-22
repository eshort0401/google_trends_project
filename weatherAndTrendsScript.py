# Standard libraries
import sys

# Third party libraries
from weatherAndTrends import loadDataAndPlot

# Script accepts up to four system arguments 
# python weatherAndTrends.py keyword state weatherVar smooth

# Check for valid input
if len(sys.argv)>5:
    sys.exit("Error! Expected 1 to 4 command line arguments. \n"
             "1: keyword - Google search keyword (default 'firewood'). \n"
             "2: state - 'VIC', 'QLD', 'NSW', 'TAS', 'ACT', 'NT', 'SA' or "
             "'WA' (default 'VIC'). \n"
             "3: weatherVar - 'rain', 'minTemp', 'maxTemp', 'minRH', "
             "'maxRH' or 'wind' (default 'maxTemp'.) \n"
             "4: smooth - natural number of weeks in running mean "
             "(default 1.)") 
else: 
    # Default arguments
    keyword='depression'
    state='VIC'
    weatherVar='radiation'
    smooth=4 # Centred running mean length in weeks; 1 for no smoothing

# Assign system arguments
if len(sys.argv)>=2:
    keyword=str(sys.argv[1])
if len(sys.argv)>=3:
    state=str(sys.argv[2])
if len(sys.argv)>=4:
    weatherVar=str(sys.argv[3])
if len(sys.argv)>=5:
    smooth=int(sys.argv[4])
    
# Check input format
if type(keyword)!=str:
    sys.exit("Error! keyword (first argument) must be a string. \n")
    
loadDataAndPlot(keyword, state, weatherVar, smooth)
        
