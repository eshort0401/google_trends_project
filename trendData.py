from pytrends.request import TrendReq
import numpy as np
import sys

def readGoogleTrendData(keyword, country, state):

    countries=np.array(['AU'])
    states=np.array(['VIC', 'QLD', 'NSW', 'TAS', 'ACT', 'NT', 'SA', 'WA'])
    
    if np.all(country!=countries) or np.all(state!=states):
        sys.exit("Error! country must be 'AUS' and state must be 'VIC', "
                 "'NSW', 'QLD', 'ACT', 'SA', 'WA', 'NT' or 'TAS'.")
    
    location=country + '-' + state
    
    print('Requesting Google trends data.')
    
    pytrend = TrendReq(hl='en-AU')
    pytrend.build_payload(kw_list=[keyword], timeframe='today 5-y', 
                          geo=location)
    
    # Interest Over Time
    trend = pytrend.interest_over_time()
    del trend['isPartial']

    return trend