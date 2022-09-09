# -*- coding: utf-8 -*-
from time import time
import numpy as np
import talib as ta
from historicaldata.historical_data import HistoricalData
import logger

class Attribute():

    def __init__(self, history_data:HistoricalData): 
        logger.log("History convert to attribute start")
        self.__history_data = history_data
        self.nun_value_index = 65
        
        self.year = np.array([date[0:4] for date in history_data.date])
        self.month = np.array([date[5:7] for date in history_data.date])
        self.date = np.array([date[8:] for date in history_data.date])
        self.hour = np.array([time[0:2] for time in history_data.time])
        self.minute = np.array([time[3:5] for time in history_data.time])
        self.open = history_data.open / history_data.close
        self.high = history_data.high / history_data.close
        self.low = history_data.low / history_data.close
        self.close = history_data.close
        self.close2 = history_data.close - (history_data.close // 1)
        self.var_length = (history_data.high - history_data.low)
        self.upper_shadow = (self.var_length / (history_data.high - np.maximum(history_data.open, history_data.close)  + 0.00000001))
        self.lower_shadow = (self.var_length / (np.minimum(history_data.open, history_data.close) - history_data.low  + 0.00000001))
        self.volume = history_data.volume

        self.before1_close = np.roll(history_data.close, 1)
        self.before2_close = np.roll(history_data.close, 2)
        self.before3_close = np.roll(history_data.close, 3)
        self.before4_close = np.roll(history_data.close, 4)
        self.before5_close = np.roll(history_data.close, 5)
        self.after1_close = np.roll(history_data.close, -1)
        self.after1_close[-1] = self.close[-1]
        self.after2_close = np.roll(history_data.close, -2)
        self.after3_close = np.roll(history_data.close, -3)
        self.after4_close = np.roll(history_data.close, -4)
        self.after5_close = np.roll(history_data.close, -5)
        self.is_up_after1 = (history_data.close < self.after1_close).astype(np.float)
        self.is_up_after2 = (history_data.close < self.after2_close).astype(np.float)
        self.is_up_after3 = (history_data.close < self.after3_close).astype(np.float)
        self.is_up_after4 = (history_data.close < self.after4_close).astype(np.float)
        self.is_up_after5 = (history_data.close < self.after5_close).astype(np.float)

        # self.before1_diff = self.before1_close / self.close
        # self.before2_diff = self.before2_close / self.close
        # self.before3_diff = self.before3_close / self.close
        # self.before4_diff = self.before4_close / self.close
        # self.before5_diff = self.before5_close / self.close

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
        self.__addBollingerBands(25)

        self.rsi = dict()
        self.__addRsi(9)
        self.__addRsi(14)
        self.__addRsi(26)

        # self.rci = dict()
        # self.__addRci(9)
        # self.__addRci(14)
        # self.__addRci(26)

        self.atr = dict()
        self.__addAtr(5)
        self.__addAtr(10)
        self.__addAtr(15)
        self.__addAtr(20)
        self.__addAtr(25)
        self.__addAtr(50)

        self.sma = dict()
        self.sma_diff = dict()
        self.__addSma(5)
        self.__addSma(10)
        self.__addSma(15)
        self.__addSma(20)
        self.__addSma(25)
        self.__addSma(50)
        self.__addSma(75)
        self.__addSma(200)

        self.dema = dict()
        self.dema_diff = dict()
        self.__addDema(5)
        self.__addDema(10)
        self.__addDema(15)
        self.__addDema(20)
        self.__addDema(25)
        self.__addDema(50)
        self.__addSar()
        self.trend_line_high = np.array(ta.HT_TRENDLINE(self.high)) / self.close
        self.trend_line_low = np.array(ta.HT_TRENDLINE(self.low)) / self.close
        self.__addMacd(12, 26, 9)
        self.gc50_25 = self.sma[50] / self.sma[25]
        self.gc50_5 = self.sma[50] / self.sma[5]
        self.gc25_5 = self.sma[25] / self.sma[5]
    
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
        diff_values = np.array(close - upper1 / close)
        self.__addColumn(diff_values, upper2 / close)
        self.__addColumn(diff_values, upper3 / close)
        self.__addColumn(diff_values, lower1 / close)
        self.__addColumn(diff_values, lower2 / close)
        self.__addColumn(diff_values, lower3 / close)
        self.__addColumn(diff_values, upper3 / lower3)

        self.bollinger_bands[timeperiod] = values
        self.bollinger_bands_diff[timeperiod] = diff_values
    
    def __addMacd(self, fastperiod, slowperiod, signalperiod):
        close = self.close
        macd, macdsignal, macdhist = ta.MACD(close, fastperiod, slowperiod, signalperiod)

        values = np.array(macd)
        self.__addColumn(values, macdsignal)
        self.__addColumn(values, macdhist)
        self.__addColumn(values, macd / macdsignal)

        self.macd = values
    
    def __addRsi(self, timeperiod):
        close = self.close
        rsi = ta.RSI(close, timeperiod)

        self.rsi[timeperiod] = rsi
    
    # def __addRci(self, timeperiod):
    #     close = self.close
    #     rci = ta.RCI(close, timeperiod)

    #     self.rci[timeperiod] = rci

    def __addAtr(self, timeperiod):
        close = self.close
        atr = ta.ATR(self.high, self.low, self.close, timeperiod)
        self.atr[timeperiod] = atr

    def __addSma(self, timeperiod):
        close = self.close
        sma = ta.SMA(close, timeperiod)
        self.sma[timeperiod] = sma
        self.sma_diff[timeperiod] = (sma  / close)

    def __addDema(self, timeperiod):
        close = self.close
        dema = ta.DEMA(close, timeperiod)
        self.dema[timeperiod] = dema
        self.dema_diff[timeperiod] = (dema  / close)

    def __addSar(self):
        close = self.close
        high = self.high
        low = self.low
        sar = ta.SAR(high, low, acceleration=0, maximum=0)
        self.sar = sar
        self.sar_diff = (sar / close)
    
    def __addColumn(self, array, column):
        np.column_stack([array, np.array(column)])

    
