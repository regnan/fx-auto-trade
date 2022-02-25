# -*- coding: utf-8 -*-
from datetime import datetime

import historicaldata.historical_loader as HistoricalLoader
from historicaldata.historical_data import TimeBarPeriods, HistoricalData
from historicaldata.attribute import Attribute
from settings import LearningPeriods
import models.model_loader as model_loader
import settings

def main():
    if settings.LEARNING_PERIOD == LearningPeriods.ALL:
        learningAll()
    if settings.LEARNING_PERIOD == LearningPeriods.CURRENT:
        learningCurrentMonth()

def learningCurrentMonth():
    now_datatime = datetime.now()
    learning(HistoricalLoader.loadMonthly(now_datatime.year, int(1)))

def learningAll():
    learning(HistoricalLoader.loadAll())

def learning(historical_data:HistoricalData):
    time_bar = historical_data.load_time_bar(TimeBarPeriods.M1)
    attribute = Attribute(time_bar)
    model = model_loader.load(attribute)
    model.learning()

# def learningFirstRate(): 
#     attribute = Attribute(HistoricalLoader.loadAll(TimeBarPeriods.M1))
#     model = HighLowStayModel()
#     model.learning(attribute)

if __name__ == '__main__':
    main()