# -*- coding: utf-8 -*-
from datetime import datetime

import historicaldata.historical_loader as HistoricalLoader
from historicaldata.historical_data import TimeBarPeriods, HistoricalData
from historicaldata.attribute import Attribute
from settings import LearningPeriods
import models.model_loader as model_loader
import settings
from tensorflow.python.client import device_lib

def main():
    learningAll()
    # print(device_lib.list_local_devices())

def learningAll():
    learning(HistoricalLoader.loadAll())

def learning(historical_data:HistoricalData):
    time_bar = historical_data.load_time_bar(settings.LEARNING_TimeBarPeriods)
    attribute = Attribute(time_bar)
    model = model_loader.load(attribute, settings.LEARNING_TimeBarPeriods)
    model.learning()

if __name__ == '__main__':
    main()