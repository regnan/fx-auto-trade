# -*- coding: utf-8 -*-
import os
from typing import List
from historicaldata.historical_data import HistoricalData

ALL_DIRECTORY_PATH = 'files/USDJPY/All'
MONTHLY_DIRECTORY_PATH ='files/USDJPY/Monthly'
# PREDICT_FILE_PATH = 'files/USDJPY/Predict/predict.csv'
PREDICT_FILE_PATH = 'C:/Users/rsk85/AppData/Roaming/MetaQuotes/Terminal/Common/Files/predict.csv'
PREDICT_ALL_FILE_PATH = 'files/USDJPY/Predict'

def loadPredict() -> HistoricalData:
    return HistoricalData(__readFile(PREDICT_FILE_PATH))

def loadPredictAll() -> HistoricalData:
    rows = []
    listdir = os.listdir(PREDICT_ALL_FILE_PATH)
    files = [s for s in listdir]
    for fileName in files:
        path = __createFilePath(PREDICT_ALL_FILE_PATH, fileName)
        rows.extend(__readFile(path))
    return HistoricalData(rows)

def loadAll() -> HistoricalData:
    rows = []
    listdir = os.listdir(ALL_DIRECTORY_PATH)
    files = [s for s in listdir]
    for fileName in files:
        path = __createFilePath(ALL_DIRECTORY_PATH, fileName)
        rows.extend(__readFile(path))
    return HistoricalData(rows)

def loadMonthly(year, month) -> HistoricalData:
    fileName = f'USDJPY_{year}_{month:02}.csv'
    path = __createFilePath(MONTHLY_DIRECTORY_PATH, fileName)
    return HistoricalData(__readFile(path))

def __createFilePath(directoryPath,fileName) -> str:
    return f'{directoryPath}/{fileName}'

def __readFile(path) -> List[str]:
    rows = []
    with open(path) as csv:
        for row in csv:
            rows.append(row.strip().split(','))
    return rows