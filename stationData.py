import ftplib  
import numpy as np
import pandas as pd
import sys

def readBureauStationData(state):

    # Read BoM data
    ftp = ftplib.FTP('ftp2.bom.gov.au', 'anonymous','eshort0401@gmail.com')
    
    baseDirectory = 'anon/gen/clim_data/IDCKWCDEA0/tables/'
    stateDirectoryDict= {'VIC': 'vic/melbourne_airport/',
                         'NSW': 'nsw/sydney_airport_amo/',
                         'QLD': 'qld/brisbane_aero/',
                         'ACT': 'nsw/canberra_airport/',
                         'SA': 'sa/adelaide_airport/',
                         'WA': 'wa/perth_airport/',
                         'NT': 'nt/darwin_airport/',  
                         'TAS': 'tas/hobart_airport/'}
    
    if stateDirectoryDict.get(state,'error')=='error':
        sys.exit("Error! Input to readStationData must be 'VIC', 'NSW', " 
                 "'QLD', 'ACT', 'SA', 'WA', 'NT' or 'TAS'.")        
    
    directory=baseDirectory + stateDirectoryDict.get(state)
    
    ftp.cwd(directory)
    
    print('Accessed ftp2.bom.gov.au/' + directory)
    
    URL=('ftp://ftp.bom.gov.au/' + directory)
    files=ftp.nlst('*.csv');
    ftp.quit()
    
    print('Reading ' + files[0])
    weather=pd.read_csv(URL+files[0], header=10, 
                        engine='python', usecols=[1,3,5,6,7,8,9,10], 
                        names=['date','rain','maxTemp','minTemp','maxRH',
                               'minRH','wind','radiation'], skipfooter=1, 
                               encoding='unicode_escape')
    
    for i in range(1,np.size(files)):
        
        print('Reading ' + files[i])
        weatherI=pd.read_csv(URL+files[i], header=10, 
                        engine='python', usecols=[1,3,5,6,7,8,9,10], 
                        names=['date','rain','maxTemp','minTemp','maxRH',
                               'minRH','wind','radiation'], skipfooter=1, 
                               encoding='unicode_escape')
        weather=weather.append(weatherI)
        
    weather['date']=pd.to_datetime(weather['date'], dayfirst=True)
    weather.index = weather['date']
    del weather['date']
    
    weather[weather.columns]=weather[weather.columns].apply(pd.to_numeric, 
            errors='coerce')
    
    return weather