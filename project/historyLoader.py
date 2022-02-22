# -*- coding: utf-8 -*-
import os
from historyData import HistoryData,HistoryPeriods

ALL_DIRECTORY_PATH = 'files/USDJPY/ALL'
MONTHLY_DIRECTORY_PATH =r'files/USDJPY/MONTHLY'
PREDICT_FILE_PATH = 'C:\\Users\\rsk85\\AppData\\Roaming\\MetaQuotes\\Terminal\\Common\\Files\\test.txt'
#PREDICT_FILE_PATH = 'files/USDJPY/PREDICT/test.csv'

def loadPredictHistory(historyPeriod = HistoryPeriods.M1):
    return HistoryData(__readFile(PREDICT_FILE_PATH), historyPeriod)

def loadAllHistory(historyPeriod = HistoryPeriods.M1):
    listdir = os.listdir(ALL_DIRECTORY_PATH)
    files = [s for s in listdir if 'all' in s]
    rows = []
    for fileName in files:
        path = __createFilePath(ALL_DIRECTORY_PATH, fileName)
        rows.extend(__readFile(path))
    return HistoryData(rows, historyPeriod)

def loadMonthlyHistory(year, month, historyPeriod = HistoryPeriods.M1):
    fileName = f'USDJPY_{year}_{month:02}.csv'
    path = __createFilePath(MONTHLY_DIRECTORY_PATH, fileName)
    return HistoryData(__readFile(path), historyPeriod)

def __createFilePath(directoryPath,fileName):
    return f'{directoryPath}/{fileName}'

def __readFile(path):
    rows = []
    with open(path) as csv:
        for row in csv:
            rows.append(row.strip().split(','))
    return rows