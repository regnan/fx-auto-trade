# -*- coding: utf-8 -*-
import numpy as np
import talib as ta
from historyData import HistoryData
from sklearn.preprocessing import MinMaxScaler
import logger

class Attribute():

    resultClassCount = 3

    def __init__(self, historyData:HistoryData): 
        logger.log("History convert to attribute start")
        self.__historyData = historyData
        self.__addParams()

        logger.log("History convert to attribute complete")
        params = self.params
        params = np.delete(params, slice(0, 50), 0)
        self.params = params

        logger.log("Attribute transform start")
        # データの正規化
        self.__scaler = MinMaxScaler(feature_range=(-1, 1))
        self.__scaler.fit(params)
        self.__transformParams = self.__scaler.transform(params)
        # 特徴量に追加
        #np.savetxt(DIRECTORY_PATH + "\\learningParam.csv", params, fmt="%s")

        self.__addResult(self.resultClassCount)
        self.__result = np.delete(self.__result, slice(0, 50), 0)
        self.result1 = np.array(np.delete(self.__isUpAfter1, slice(0, 50), 0))
        self.x_train = self.__transformParams
        self.y_train = self.__result
        self.paramCount = self.x_train.shape[1]
        logger.log("Attribute transform complete")
    
    def __addBollingerBands(self, timeperiod):
        close = self.__close
        upper1, middle,lower1 = ta.BBANDS(close, timeperiod, nbdevup=1, nbdevdn=1, matype=0)
        upper2, middle2, lower2 = ta.BBANDS(close, timeperiod, nbdevup=2, nbdevdn=2, matype=0)
        upper3, middle3, lower3 = ta.BBANDS(close, timeperiod, nbdevup=3, nbdevdn=3, matype=0)
        self.__addParam(upper1)
        self.__addParam(upper2)
        self.__addParam(upper3)
        self.__addParam(lower1)
        self.__addParam(lower2)
        self.__addParam(lower3)
        self.__addParam(close - upper1)
        self.__addParam(close - upper2)
        self.__addParam(close - upper3)
        self.__addParam(close - lower1)
        self.__addParam(close - lower2)
        self.__addParam(close - lower3)
    
    def __addMacd(self, fastperiod, slowperiod, signalperiod):
        close = self.__close
        macd, macdsignal, macdhist = ta.MACD(close, fastperiod, slowperiod, signalperiod)
        self.__addParam(macd)
        self.__addParam(macdsignal)
        self.__addParam(macdhist)
        self.__addParam(close - macd)
        self.__addParam(close - macdsignal)
        self.__addParam(close - macdhist)
    
    def __addRsi(self, timeperiod):
        close = self.__close
        rsi = ta.RSI(close, timeperiod)
        self.__addParam(rsi)
        self.__addParam(close - rsi)

    def __addSma(self, timeperiod):
        close = self.__close
        sma = ta.SMA(close, timeperiod)
        self.__addParam(sma)
        self.__addParam(close - sma)
    
    def __addParams(self):
        #np.diff 階差数列
        historyData = self.__historyData
        # self.__year = np.array([date[0:4] for date in historyData.date])
        # #self.__year = np_utils.to_categorical(self.__year, 10)
        # self.__month = np.array([date[5:7] for date in historyData.date])
        # self.__month = np_utils.to_categorical(self.__month, 13)
        # self.__date = np.array([date[8:] for date in historyData.date])
        # self.__date = np_utils.to_categorical(self.__date, 32)
        # self.__hour = np.array([time[0:2] for time in historyData.time])
        # self.__hour = np_utils.to_categorical(self.__hour, 24)
        # self.__minute = np.array([time[3:] for time in historyData.time])
        # self.__minute = np_utils.to_categorical(self.__minute, 60)
        self.__year = np.array([date[0:4] for date in historyData.date])
        self.__month = np.array([date[5:7] for date in historyData.date])
        self.__date = np.array([date[8:] for date in historyData.date])
        self.__hour = np.array([time[0:2] for time in historyData.time])
        self.__minute = np.array([time[3:5] for time in historyData.time])
        self.__open = historyData.open
        self.__high = historyData.high
        self.__low = historyData.low
        self.__close = historyData.close
        self.__volume = historyData.volume
        self.__before1Close = np.roll(historyData.close, 1)
        self.__before2Close = np.roll(historyData.close, 2)
        self.__before3Close = np.roll(historyData.close, 3)
        self.__before4Close = np.roll(historyData.close, 4)
        self.__before5Close = np.roll(historyData.close, 5)
        self.__after1Close = np.roll(historyData.close, -1)
        self.__after2Close = np.roll(historyData.close, -2)
        self.__after3Close = np.roll(historyData.close, -3)
        self.__after4Close = np.roll(historyData.close, -4)
        self.__after5Close = np.roll(historyData.close, -5)
        self.__isUpAfter1 = (historyData.close < self.__after1Close).astype(np.float)
        self.__isUpAfter2 = (historyData.close < self.__after2Close).astype(np.float)
        self.__isUpAfter3 = (historyData.close < self.__after3Close).astype(np.float)
        self.__isUpAfter4 = (historyData.close < self.__after4Close).astype(np.float)
        self.__isUpAfter5 = (historyData.close < self.__after5Close).astype(np.float)

        self.__before1Diff = self.__close - self.__before1Close
        self.__before2Diff = self.__close - self.__before2Close
        self.__before3Diff = self.__close - self.__before3Close
        self.__before4Diff = self.__close - self.__before4Close
        self.__before5Diff = self.__close - self.__before5Close

        close = historyData.close

        # self.params = np.array(self.__open.astype(np.float))
        self.params = np.array(self.__year.astype(np.int))
        self.__addParam(self.__month.astype(np.int))
        self.__addParam(self.__date.astype(np.int))
        self.__addParam(self.__hour.astype(np.int))
        self.__addParam(self.__minute.astype(np.int))
        self.__addParam(self.__open.astype(np.float))
        self.__addParam(self.__high.astype(np.float))
        self.__addParam(self.__low.astype(np.float))
        self.__addParam(self.__close.astype(np.float))
        self.__addParam(self.__volume.astype(np.int))

        self.__addParam(self.__before1Diff.astype(np.float))
        self.__addParam(self.__before2Diff.astype(np.float))
        self.__addParam(self.__before3Diff.astype(np.float))
        self.__addParam(self.__before4Diff.astype(np.float))
        self.__addParam(self.__before5Diff.astype(np.float))
        self.__addParam(self.__before1Close.astype(np.float))
        self.__addParam(self.__before2Close.astype(np.float))
        self.__addParam(self.__before3Close.astype(np.float))
        self.__addParam(self.__before4Close.astype(np.float))
        self.__addParam(self.__before5Close.astype(np.float))

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
        self.__addRsi(9)
        self.__addRsi(10)
        self.__addRsi(11)
        self.__addRsi(12)
        self.__addRsi(13)
        self.__addRsi(14)
        self.__addRsi(15)
        self.__addSma(5)
        self.__addSma(10)
        self.__addSma(15)
        self.__addSma(20)
        self.__addSma(25)
        self.__addSma(50)
        self.__addMacd(12, 26, 9)

    def __addParam(self, param):
        self.params = np.column_stack([self.params, param])
    
    def __addResult(self, resultClassCount):
        if resultClassCount == 3:
            diff = (self.__close - self.__after1Close).astype(np.float)
            self.__result = np.array((diff < -0.005).astype(np.int))
            self.__result = np.column_stack([self.__result, ((diff >= -0.005) & (diff <= 0.005)).astype(np.int)])
            self.__result = np.column_stack([self.__result, (diff > 0.005).astype(np.int)])
            self.result2 = np.array(np.delete(self.__result, slice(0, 50), 0))
        
        if resultClassCount == 2:
            self.__result = self.__isUpAfter1
            self.__result = np.column_stack([self.__result, (self.__isUpAfter1 == 0).astype(np.int)])
            #fuga = [" ".join(map(str, i))  for i in self.__result]
            #logger.log('\n'.join(map(str, fuga)))

        if resultClassCount == 1:
            self.__result = (self.__after1Close).astype(np.float)
            #self.__result = (self.__close - self.__after1Close).astype(np.float)
            #self.__result = self.__after1Close
    
