# -*- coding: utf-8 -*-
from enum import Enum
from typing import List
from datetime import datetime
import numpy as np

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

class HistoricalData():
    def __init__(self, historical_data:List[str]):

        self.__historical_data = np.array(historical_data)
        if self.__historical_data.shape[0] == 0:
            return None

        self.date = self.__load(HistoricalDataColumns.DATE, datetime)
        self.time = self.__load(HistoricalDataColumns.TIME, datetime)
        self.open = self.__load(HistoricalDataColumns.OPEN, np.double)
        self.high = self.__load(HistoricalDataColumns.HIGH, np.double)
        self.low = self.__load(HistoricalDataColumns.LOW, np.double)
        self.close = self.__load(HistoricalDataColumns.CLOSE, np.double)
        self.volume = self.__load(HistoricalDataColumns.VOLUME, np.double)
    
    def __load(self, column:HistoricalDataColumns, dtype):
        values = self.__select(column, dtype)
        return values      

    def __select(self, column:HistoricalDataColumns, dtype):
        return np.array(self.__historical_data[:, column.value]).astype(dtype)
