# -*- coding: utf-8 -*-
import os
from datetime import datetime
from historyData import HistoryData

class HistoryLoader:
    DIRECTORY_PATH = 'files\\USDJPY'

    def loadCurrentData(self):
        nowDatetime = datetime.now()
        return self.loadMonthlyData(nowDatetime.year, nowDatetime.month)

    def loadMonthlyData(self, year, month):
        fileName = f'USDJPY_{year}_{month:02}.csv'
        path = self.__createFilePath(fileName)
        return HistoryData(self.__readFile(path))

    def loadAllData(self):
        listdir = os.listdir(self.DIRECTORY_PATH)
        files = [s for s in listdir if 'all' in s]
        rows = []
        for fileName in files:
            path = self.__createFilePath(fileName)
            rows.extend(self.__readFile(path))
        return HistoryData(rows)

    def __createFilePath(self, fileName):
        return f'{self.DIRECTORY_PATH}\\{fileName}'

    def __readFile(self, path):
        rows = []
        with open(path) as csv:
            for row in csv:
                rows.append(row.strip().split(','))
        return rows