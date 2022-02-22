# -*- coding: utf-8 -*-
from datetime import datetime

import historyLoader
from historyData import HistoryPeriods
from attribute import Attribute
from models import LearningModel

def learningCurrentMonth():
    nowDatetime = datetime.now()
    historyData = historyLoader.loadMonthlyHistory(nowDatetime.year, int(1), HistoryPeriods.M5)
    learning(Attribute(historyData))

def learningAll():
    historyData = historyLoader.loadAllHistory(HistoryPeriods.M1)
    learning(Attribute(historyData))

def learning(attribute):
    model = LearningModel(attribute.paramCount)
    model.learning(attribute)
    model.save()

def learningFirstRate(): 
    historyData = historyLoader.loadAllHistory(HistoryPeriods.M1)
    attribute = Attribute(historyData)
    model = LearningModel(attribute.paramCount)
    model.learning(attribute)


#learningCurrentMonth()
learningAll()

#learningFirstRate()