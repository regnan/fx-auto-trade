# -*- coding: utf-8 -*-
import numpy as np
import historicaldata.historical_loader as HistoryLoader
from historicaldata.historical_data import TimeBarPeriods
from historicaldata.attribute import Attribute
import models.model_loader as model_loader
import logger
from models.models import ResultTypes
import settings

def main():
    predictAll(settings.LEARNING_TimeBarPeriods)

def predict(timeFrame:int):
    logger.log("predict start")
    historical_data = HistoryLoader.loadPredict()
    time_bar = historical_data.load_time_bar(TimeBarPeriods(1))
    attribute = Attribute(time_bar)
    model = model_loader.load(attribute, TimeBarPeriods(timeFrame))
    predictions = model.predict()
    result = model.predict_result_type()

    if result == ResultTypes.BUY:
        return True
    elif result == ResultTypes.SELL:
        return False
    else: 
        return ""

def predictAll(timeFrame:int):
    logger.log("predict start")
    historical_data = HistoryLoader.loadPredictAll()
    time_bar = historical_data.load_time_bar(TimeBarPeriods(timeFrame))
    attribute = Attribute(time_bar)
    model = model_loader.load(attribute, TimeBarPeriods(timeFrame))
    predictions = model.predict()

if __name__ == '__main__':
    main()