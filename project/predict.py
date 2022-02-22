# -*- coding: utf-8 -*-
import historyLoader
import numpy as np
from historyData import HistoryPeriods
from attribute import Attribute
from models import PredictModel
import logger

def predict():
    logger.log("predict start")
    history = historyLoader.loadPredictHistory(HistoryPeriods.M1)
    attribute = Attribute(history)
    model = PredictModel()
    predictions = model.predict(attribute)
    result = np.argmax(predictions[0])
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

def predict2():
    logger.log("predict complete")
    history = historyLoader.loadPredictHistory(HistoryPeriods.M1)
    attribute = Attribute(history)
    model = PredictModel()
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

predict2()