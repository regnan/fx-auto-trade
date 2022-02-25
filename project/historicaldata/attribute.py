# -*- coding: utf-8 -*-
from time import time
import numpy as np
import talib as ta
from historicaldata.historical_data import TimeBar
import logger



class Attribute():

    def __init__(self, history_data:TimeBar): 
        logger.log("History convert to attribute start")
        self.__history_data = history_data
        self.period = history_data.period
        self.nun_value_index = 50
        
        self.year = np.array([date[0:4] for date in history_data.date])
        self.month = np.array([date[5:7] for date in history_data.date])
        self.date = np.array([date[8:] for date in history_data.date])
        self.hour = np.array([time[0:2] for time in history_data.time])
        self.minute = np.array([time[3:5] for time in history_data.time])

        self.open = history_data.open
        self.high = history_data.high
        self.low = history_data.low
        self.close = history_data.close
        self.volume = history_data.volume

        self.before1_close = np.roll(history_data.close, 1)
        self.before2_close = np.roll(history_data.close, 2)
        self.before3_close = np.roll(history_data.close, 3)
        self.before4_close = np.roll(history_data.close, 4)
        self.before5_close = np.roll(history_data.close, 5)
        self.after1_close = np.roll(history_data.close, -1)
        self.after2_close = np.roll(history_data.close, -2)
        self.after3_close = np.roll(history_data.close, -3)
        self.after4_close = np.roll(history_data.close, -4)
        self.after5_close = np.roll(history_data.close, -5)
        self.is_up_after1 = (history_data.close < self.after1_close).astype(np.float)
        self.is_up_after2 = (history_data.close < self.after2_close).astype(np.float)
        self.is_up_after3 = (history_data.close < self.after3_close).astype(np.float)
        self.is_up_after4 = (history_data.close < self.after4_close).astype(np.float)
        self.is_up_after5 = (history_data.close < self.after5_close).astype(np.float)

        self.before1_diff = self.close - self.before1_close
        self.before2_diff = self.close - self.before2_close
        self.before3_diff = self.close - self.before3_close
        self.before4_diff = self.close - self.before4_close
        self.before5_diff = self.close - self.before5_close

        self.bollinger_bands = dict()
        self.bollinger_bands_diff = dict()
        self.__addBollingerBands(10)
        self.__addBollingerBands(11)
        self.__addBollingerBands(12)
        self.__addBollingerBands(13)
        self.__addBollingerBands(14)
        self.__addBollingerBands(15)
        self.__addBollingerBands(16)
        self.__addBollingerBands(17)
        self.__addBollingerBands(18)
        self.__addBollingerBands(19)
        self.__addBollingerBands(20)

        self.rsi = dict()
        self.__addRsi(9)
        self.__addRsi(10)
        self.__addRsi(11)
        self.__addRsi(12)
        self.__addRsi(13)
        self.__addRsi(14)
        self.__addRsi(15)

        self.sma = dict()
        self.sma_diff = dict()
        self.__addSma(5)
        self.__addSma(10)
        self.__addSma(15)
        self.__addSma(20)
        self.__addSma(25)
        self.__addSma(50)

        self.__addMacd(12, 26, 9)
        
        logger.log("History convert to attribute complete")
    
    def __addBollingerBands(self, timeperiod):
        close = self.close
        upper1, middle,lower1 = ta.BBANDS(close, timeperiod, nbdevup=1, nbdevdn=1, matype=0)
        upper2, middle2, lower2 = ta.BBANDS(close, timeperiod, nbdevup=2, nbdevdn=2, matype=0)
        upper3, middle3, lower3 = ta.BBANDS(close, timeperiod, nbdevup=3, nbdevdn=3, matype=0)

        values = np.array(upper1)
        self.__addColumn(values, upper2)
        self.__addColumn(values, upper3)
        self.__addColumn(values, lower1)
        self.__addColumn(values, lower2)
        self.__addColumn(values, lower3)
        diff_values = np.array(close - upper1)
        self.__addColumn(diff_values, close - upper2)
        self.__addColumn(diff_values, close - upper3)
        self.__addColumn(diff_values, close - lower1)
        self.__addColumn(diff_values, close - lower2)
        self.__addColumn(diff_values, close - lower3)

        self.bollinger_bands[timeperiod] = values
        self.bollinger_bands_diff[timeperiod] = diff_values
    
    def __addMacd(self, fastperiod, slowperiod, signalperiod):
        close = self.close
        macd, macdsignal, macdhist = ta.MACD(close, fastperiod, slowperiod, signalperiod)

        values = np.array(macd)
        self.__addColumn(values, macdsignal)
        self.__addColumn(values, macdhist)

        self.macd = values
    
    def __addRsi(self, timeperiod):
        close = self.close
        rsi = ta.RSI(close, timeperiod)

        self.rsi[timeperiod] = rsi

    def __addSma(self, timeperiod):
        close = self.close
        sma = ta.SMA(close, timeperiod)
        self.sma[timeperiod] = sma
        self.sma_diff[timeperiod] = (close - sma)
    
    def __addColumn(self, array, column):
        np.column_stack([array, np.array(column)])

    
