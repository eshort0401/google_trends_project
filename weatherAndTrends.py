# Standard libraries
import sys

# Third party libraries
import matplotlib.lines as lines
import matplotlib.patches as patches
import matplotlib.pyplot as plt
from matplotlib import rcParams
import numpy as np
import pandas as pd
import scipy.signal as sgnl

# Application libraries
from stationData import readBureauStationData
from trendData import readGoogleTrendData

def loadDataAndPlot(keyword='firewood',state='VIC',weatherVar='minTemp',
                    smooth=1):
    
    print('Initialising.')
    
    # Check input format
    if type(keyword)!=str:
        sys.exit("Error! keyword (first argument) must be a string. \n")
            
    states=np.array(['VIC', 'QLD', 'NSW', 'TAS', 'ACT', 'NT', 'SA', 'WA'])    
    if np.all(state!=states):
        sys.exit("Error! state (second argument) must be 'VIC', 'NSW', 'QLD', "
                 "'ACT', 'SA', 'WA', 'NT' or 'TAS'. \n")
        
    weatherVars=np.array(['rain', 'maxTemp', 'minTemp', 'maxRH', 'minRH', 
                          'wind', 'radiation'])
    if np.all(weatherVar!=weatherVars):
        sys.exit("Error! weatherVar (third argument) must be 'rain', 'maxTemp', "
                 "'minTemp', 'maxRH', 'minRH' or 'wind'. \n")
        
    units = {'rain': 'mm day$^{-1}$',
            'minTemp': '$^{\circ}$ C',
            'maxTemp': '$^{\circ}$ C',
            'maxRH': '$\%$',
            'minRH': '$\%$',
            'wind': 'm s$^{-1}$',
            'radiation': 'MJ m$^{-1}$'}
        
    if type(smooth)!=int:
        sys.exit("Error! smooth (fourth argument) must be an integer. \n")
    
    country='AU' # Only country currently supported
        
    # Specify whether to save data or plots
    saveFiles=True
    savePlots=True
    
    # Read Google Trends data
    fileName=keyword.replace(' ', '_') + '_' + country + '_' + state
    
    print('Locating data.')
            
    try:
        trend=pd.read_pickle('./trend_data/trend_' + fileName + '.pkl')
    except:
        trend=readGoogleTrendData(keyword, country, state)
        if saveFiles:
            trend.to_pickle('./trend_data/trend_' + fileName + '.pkl')
            
    # Read BoM data
    try:
        weather=pd.read_pickle('./station_data/weather_' + country + '_' + state + '.pkl')
    except:
        weather=readBureauStationData(state)
        if saveFiles:        
            weather.to_pickle('./station_data/weather_' + country + '_' + state + '.pkl')
    
    # Resample weather data weekly
    weekWeather = pd.DataFrame()
    weekWeather = weather.resample('W').mean()
    
    # Restrict to common dates
    commonDates=trend.index.intersection(weather.index)
    weekWeather=weekWeather.loc[commonDates]
    trend=trend.loc[commonDates]
    
    # Smooth if required
    if smooth>1:
        weekWeatherSmooth=weekWeather.rolling(smooth, center=True).mean()
        trendSmooth=trend.rolling(smooth, center=True).mean()
    else:
        weekWeatherSmooth=weekWeather
        trendSmooth=trend
        
    # Calculate correlation
    rho=weekWeatherSmooth[weatherVar].corr(trendSmooth[keyword])
    
    # Plot
    plt.close("all")
    plt.rc('text', usetex=True)
        
    # Initialise fonts   
    rcParams['font.family'] = 'serif'
    rcParams.update({'font.serif': 'Times New Roman'})
    rcParams.update({'font.size': 12})
    rcParams.update({'font.weight': 'normal'})
    
    print('Plotting time series.')

    # Line plot
    trendSmooth[keyword].plot(style='-b')
    plt.xlabel('Date', size=12)
    plt.ylabel(keyword + ' [search volume]', size=12)
    plt.title('Time series for ' + country + '-' + state, size=12)
    
    weekWeatherSmooth[weatherVar].plot(secondary_y=True, style='--r')    
    plt.xlabel('Date', size=12)
    plt.ylabel(weatherVar + ' [' + units.get(weatherVar) + ']', size=12)
    
    redLine = lines.Line2D([],[],color='r', label=weatherVar, ls='--')
    blueLine = lines.Line2D([],[],color='b', label=keyword)
    extra = patches.Rectangle((0, 0), 1, 1, fc="w", fill=False, 
                              edgecolor='none', linewidth=0, 
                              label=('$\\rho=%1.2f $' % rho))
    
    plt.legend(handles=[redLine, blueLine, extra], prop={'size': 12})
    
    if savePlots:
        plt.savefig('./figures/' + weatherVar + '_' + fileName + '.svg')
        plt.savefig('./figures/' + weatherVar + '_' + fileName + '.pdf')
    
    # Scatterplot    
    plt.figure()
    
    print('Plotting scatter plot.')
    
    commonWeatherSmooth=weekWeatherSmooth.loc[commonDates][weatherVar].values
    commonTrendSmooth=trendSmooth.loc[commonDates][keyword].values
    plt.scatter(commonWeatherSmooth,commonTrendSmooth)
    plt.title('Scatterplot for ' + country + '-' + state, size=12)
    plt.xlabel(weatherVar + ' [' + units.get(weatherVar) + ']', size=12)
    plt.ylabel(keyword + ' [search volume]', size=12)
    
    # Periodogram
    plt.figure()
    
    print('Plotting periodogram.')
    
    commonWeather=weekWeather.loc[commonDates][weatherVar].values
    commonTrend=trend.loc[commonDates][keyword].values
    
    fs=1/604800
    fW, weatherSpectrum = sgnl.welch(commonWeather, fs, scaling='spectrum',
                                     nperseg=208, detrend='linear')
    fT, trendSpectrum = sgnl.welch(commonTrend, fs, scaling='spectrum',
                                   nperseg=208, detrend='linear')
    
    plt.semilogy(fT*3600*24*365,trendSpectrum, basey=2)
    plt.xlabel('Frequency [cycles per year]', size=12)
    plt.ylabel(keyword + ' [(search volume)$^2$]', size=12)
    plt.grid()
    plt.title('``'+ keyword + '" search periodogram for ' + country + '-' 
              + state, size=12)
    
    plt.figure()
    
    plt.semilogy(fW*3600*24*365,weatherSpectrum, basey=2)
    plt.xlabel('Frequency [cycles per year]', size=12)
    plt.ylabel(weatherVar + ' [(' + units.get(weatherVar) + ')$^2$]', size=12)
    plt.grid()
    plt.title(weatherVar + ' periodogram for ' + country + '-' + state, size=12)
    
    plt.show()
    
    return
    
