# -*- coding: utf-8 -*-
from asyncio.windows_events import NULL
from fileinput import filename
from multiprocessing.sharedctypes import Value
import os
from datetime import datetime,time
from tokenize import Double
import numpy as np
import matplotlib.pyplot as plt
import talib as ta
from enum import Enum

class HistoryColumns(Enum):
    DATE = 0
    TIME = 1
    OPEN = 2
    HIGH = 3
    LOW = 4
    CLOSE = 5
    VOLUME = 6


class HistoryData():

    def __init__(self, historyData):
        self.ddd = 0
        self.__historyData = np.array(historyData)
        self.date = np.array(self.__historyData[:, HistoryColumns.TIME.value]).astype(datetime)
        self.time = np.array(self.__historyData[:, HistoryColumns.TIME.value]).astype(datetime)
        self.open = np.array(self.__historyData[:, HistoryColumns.OPEN.value]).astype(np.double)
        self.high = np.array(self.__historyData[:, HistoryColumns.HIGH.value]).astype(np.double)
        self.low = np.array(self.__historyData[:, HistoryColumns.LOW.value]).astype(np.double)
        self.close = np.array(self.__historyData[:, HistoryColumns.CLOSE.value]).astype(np.double)
        self.volume = np.array(self.__historyData[:, HistoryColumns.VOLUME.value]).astype(np.double)


