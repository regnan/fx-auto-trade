# -*- coding: utf-8 -*-
import os
from datetime import datetime,time
import numpy as np
import matplotlib.pyplot as plt
import talib as ta
from enum import Enum

from historyLoader import HistoryLoader
from historyData import HistoryColumns, HistoryData

class CSV_HEADER(Enum):
    TIME = 0
    OPEN = 1
    HIGH = 2
    LOW = 3
    CLOSE = 4
    VOLUME = 5

def currentDataConvert():
    return 'OK'

def allDataConvert():
    #historyData = HistoryData(historyLoader.HistoryLoader.loadAllData())
    historyLoader = HistoryLoader()
    historyData = historyLoader.loadMonthlyData(2022, 1)
    close = historyData.close

    upper1, middle,lower1 = ta.BBANDS(close, timeperiod=2500, nbdevup=1, nbdevdn=1, matype=0)
    upper2, middle2, lower2 = ta.BBANDS(close, timeperiod=2500, nbdevup=2, nbdevdn=2, matype=0)
    upper3, middle3, lower3 = ta.BBANDS(close, timeperiod=2500, nbdevup=3, nbdevdn=3, matype=0)

    plt.plot(middle,label='price',color='k')
    plt.plot(upper1,label='upper1',color='b')
    plt.plot(lower1,label='lower1',color='b')
    plt.plot(upper2,label='upper2',color='g')
    plt.plot(lower2,label='lower2',color='g')
    plt.plot(upper3,label='upper3',color='r')
    plt.plot(lower3,label='lower3',color='r')
    plt.xlabel('date')
    plt.ylabel('price')
    plt.legend()
    plt.show()
    return 'OK'


allDataConvert()