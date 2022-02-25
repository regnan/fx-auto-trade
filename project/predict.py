# -*- coding: utf-8 -*-
import numpy as np
import historicaldata.historical_loader as HistoryLoader
from historicaldata.historical_data import TimeBarPeriods
from historicaldata.attribute import Attribute
import models.model_loader as model_loader
import logger
from models.models import ResultTypes

def main():
    predict()

def predict3():
    logger.log("predict start")
    historical_data = HistoryLoader.loadPredict()
    time_bar = historical_data.load_time_bar(TimeBarPeriods.M1)
    attribute = Attribute(time_bar)
    model = model_loader.load(attribute)
    predictions = model.predict()
    result = predictions[-1]
    print(predictions)
    #print(predictions[-1][0] >= 0.5)
    #return model.result()
    logger.log("predict start")
    # return predictions[-1][0] >= 0.5
    if result == 0:
        return True
    elif result == 2:
        return False
    else: 
        return ""

def predict():
    logger.log("predict start")
    historical_data = HistoryLoader.loadPredict()
    time_bar = historical_data.load_time_bar(TimeBarPeriods.M1)
    attribute = Attribute(time_bar)
    model = model_loader.load(attribute)
    predictions = model.predict()
    result = model.predict_result_type()

    if result == ResultTypes.BUY:
        return True
    elif result == ResultTypes.SELL:
        return False
    else: 
        return ""

def predict2():
    logger.log("predict complete")
    historical_data = HistoryLoader.loadPredict()
    time_bar = historical_data.load_time_bar(TimeBarPeriods.M1)
    attribute = Attribute(time_bar)
    model = model_loader.load()
    predictions = model.predict(attribute)

    # print(predictions[-1][0] >= 0.5)
    # predictions = np.array(predictions)
    # #return model.result()
    # a = np.array([row[0] for row in predictions])
    # b = np.array([row[1] for row in predictions])
    # result = a > b
    # train = attribute.result1

    train = [np.argmax(i) for i in attribute.result2]
    result = [np.argmax(i) for i in predictions]

    isTrueOk = np.array(train == result)
    isOk = np.array(train == result)
    isNg = (train != result)
    print(isTrueOk)
    print(isOk)
    print(isNg)
    print(np.count_nonzero(isTrueOk == True))
    print(np.count_nonzero(isOk == True))
    print(np.count_nonzero(isNg == True))

    logger.log("predict complete")

if __name__ == '__main__':
    main()