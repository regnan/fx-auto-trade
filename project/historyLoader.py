# -*- coding: utf-8 -*-
import os
from datetime import datetime
from historyData import HistoryData,HistoryPeriods

DIRECTORY_PATH = 'files\\USDJPY'

def loadMonthlyData(year, month, historyPeriod = HistoryPeriods.M1):
    fileName = f'USDJPY_{year}_{month:02}.csv'
    path = __createFilePath(fileName)
    return HistoryData(__readFile(path), historyPeriod)

def loadAllData(historyPeriod = HistoryPeriods.M1):
    listdir = os.listdir(DIRECTORY_PATH)
    files = [s for s in listdir if 'all' in s]
    rows = []
    for fileName in files:
        path = __createFilePath(fileName)
        rows.extend(__readFile(path))
    return HistoryData(rows, historyPeriod)

def __createFilePath(fileName):
    return f'{DIRECTORY_PATH}\\{fileName}'

def __readFile(path):
    rows = []
    with open(path) as csv:
        for row in csv:
            rows.append(row.strip().split(','))
    return rows