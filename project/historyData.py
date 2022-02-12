# -*- coding: utf-8 -*-
from asyncio.windows_events import NULL
from fileinput import filename
from multiprocessing.sharedctypes import Value
from datetime import datetime
from tokenize import Double
from matplotlib.pyplot import axis
import numpy as np
from enum import Enum

class HistoryPeriods(Enum):
    M1 = 1
    M2 = 2
    M3 = 3
    M4 = 4
    M5 = 5
    M10 = 10
    M15 = 15
    M30 = 30
    H1 = 60
    H2 = 120
    H4 = 240
    H6 = 360
    H12 = 720
    DAY = 1440
    WEEK = 10080
    MONTH =  43200

class HistoryColumns(Enum):
    DATE = 0
    TIME = 1
    OPEN = 2
    HIGH = 3
    LOW = 4
    CLOSE = 5
    VOLUME = 6

class RemakeMethods(Enum):
    FIRST = 0
    LAST = 1
    MIN = 2
    MAX = 3
    SUM = 4

class HistoryData():

    def __init__(self, historyData, historyPeriod):
        if historyPeriod not in [e for e in HistoryPeriods]:
            return NULL

        self.__historyData = np.array(historyData)
        self.__historyPeriod = historyPeriod
        self.__size = self.__historyData.shape[0]

        if self.__size == 0:
            return NULL

        #割り切れない場合足の作り直しでエラーになるので、古いデータを削除する
        remainder = self.__size % self.__historyPeriod.value
        if remainder != 0:
            self.__historyData = np.delete(self.__historyData, slice(0, remainder), axis = 0)
            self.__size = self.__historyData.shape[0]

        self.date = self.__load__(HistoryColumns.DATE, datetime, RemakeMethods.FIRST)
        self.time = self.__load__(HistoryColumns.TIME, datetime, RemakeMethods.FIRST)
        self.open = self.__load__(HistoryColumns.OPEN, np.double, RemakeMethods.FIRST)
        self.high = self.__load__(HistoryColumns.HIGH, np.double, RemakeMethods.MAX)
        self.low = self.__load__(HistoryColumns.LOW, np.double, RemakeMethods.MIN)
        self.close = self.__load__(HistoryColumns.CLOSE, np.double, RemakeMethods.LAST)
        self.volume = self.__load__(HistoryColumns.VOLUME, np.double, RemakeMethods.SUM)
    
    #任意の列を抽出後に指定された期間の足に作り直す
    def __load__(self, historyColumn, dtype, historyMethod):
        values = self.__select__(historyColumn, dtype)
        return self.__remakeByPeriod__(values, historyMethod)        

    def __select__(self, historyColumn, dtype):
        if historyColumn not in [e for e in HistoryColumns]:
            raise Exception("illegal remake method")

        return np.array(self.__historyData[:, historyColumn.value]).astype(dtype)
    
    #1分足のデータを任意の足に変換
    def __remakeByPeriod__(self, values, remakeMethod):
        reshapedValues = np.reshape(values, (int(self.__size / self.__historyPeriod.value), self.__historyPeriod.value))
        return self.__executeRemakeMethod__(reshapedValues, remakeMethod)
    
    def __executeRemakeMethod__(self, values, remakeMethod):
        if remakeMethod not in [e for e in RemakeMethods]:
            raise Exception("illegal remake method")

        if remakeMethod == RemakeMethods.FIRST:
            return values[:, 0]
        elif remakeMethod == RemakeMethods.LAST:
            return values[:, self.__historyPeriod.value - 1]
        elif remakeMethod == RemakeMethods.MIN:
            return np.min(values, axis = 1)
        elif remakeMethod == RemakeMethods.MAX:
            return np.max(values, axis = 1)
        elif remakeMethod == RemakeMethods.SUM:
            return np.sum(values, axis = 1)
    
    def size(self):
        return self.__size



