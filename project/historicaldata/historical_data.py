# -*- coding: utf-8 -*-
from enum import Enum
from typing import List
from datetime import datetime
import numpy as np
import logger

class TimeBarPeriods(Enum):
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

class HistoricalDataColumns(Enum):
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

class TimeBar():
    def __init__(self, historical_data:List[str], time_bar_period:TimeBarPeriods):
        logger.log("Time bar generate start")

        self.__historical_data = np.array(historical_data)
        self.period = time_bar_period

        if self.__historical_data_size() == 0:
            return None

        #割り切れない場合足の作り直しでエラーになるので、古いデータを削除する
        remainder = self.__historical_data_size() % self.period.value
        if remainder != 0:
            self.__historical_data = np.delete(self.__historical_data, slice(0, remainder), axis = 0)

        self.date = self.__load(HistoricalDataColumns.DATE, RemakeMethods.FIRST, datetime)
        self.time = self.__load(HistoricalDataColumns.TIME, RemakeMethods.FIRST, datetime)
        self.open = self.__load(HistoricalDataColumns.OPEN, RemakeMethods.FIRST, np.double)
        self.high = self.__load(HistoricalDataColumns.HIGH, RemakeMethods.MAX, np.double)
        self.low = self.__load(HistoricalDataColumns.LOW, RemakeMethods.MIN, np.double)
        self.close = self.__load(HistoricalDataColumns.CLOSE, RemakeMethods.LAST, np.double)
        self.volume = self.__load(HistoricalDataColumns.VOLUME, RemakeMethods.SUM, np.double)
        
        logger.log("Time bar generate complete")
    
    #任意の列を抽出後に指定された期間の足に作り直す
    def __load(self, column:HistoricalDataColumns, method:RemakeMethods, dtype):
        values = self.__select(column, dtype)
        return self.__remake(values, method)        

    def __select(self, column:HistoricalDataColumns, dtype):
        return np.array(self.__historical_data[:, column.value]).astype(dtype)
    
    #1分足のデータを任意の足に変換    
    def __remake(self, values, method:RemakeMethods):
        reshapedValues = np.reshape(values, (self.size(), self.period.value))

        if method == RemakeMethods.FIRST:
            return reshapedValues[:, 0]
        elif method == RemakeMethods.LAST:
            return reshapedValues[:, self.period.value - 1]
        elif method == RemakeMethods.MIN:
            return np.min(reshapedValues, axis = 1)
        elif method == RemakeMethods.MAX:
            return np.max(reshapedValues, axis = 1)
        elif method == RemakeMethods.SUM:
            return np.sum(reshapedValues, axis = 1)
    
    def __historical_data_size(self) -> int:
        return self.__historical_data.shape[0]
    
    def size(self) -> int:
        return int(self.__historical_data_size() / self.period.value)

class HistoricalData():
    def __init__(self, historical_data:List[str]):
        self.__historical_data = historical_data
        self.__time_var_dict = dict()
    
    def load_time_bar(self, timeBarPeriod:TimeBarPeriods) -> TimeBar:
        if timeBarPeriod not in self.__time_var_dict:
            time_bar = TimeBar(self.__historical_data, timeBarPeriod)
            self.__time_var_dict[timeBarPeriod] = time_bar

        return self.__time_var_dict.get(timeBarPeriod)
