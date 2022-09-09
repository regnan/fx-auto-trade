# -*- coding: utf-8 -*-
from datetime import datetime

import historicaldata.historical_loader as HistoricalLoader
from historicaldata.historical_data import TimeBarPeriods, HistoricalData
from historicaldata.attribute import Attribute
from settings import LearningPeriods
import models.model_loader as model_loader
import settings

def main():
    learningAll()
    # print(device_lib.list_local_devices())

def learningAll():
    learning(HistoricalLoader.loadAll())

def learning(historical_data:HistoricalData):
    attribute = Attribute(historical_data)
    model = model_loader.load(attribute, settings.LEARNING_TimeBarPeriods)
    model.learning()

if __name__ == '__main__':
    main()