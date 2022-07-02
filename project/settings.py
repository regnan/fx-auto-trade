# -*- coding: utf-8 -*-
from enum import Enum
from historicaldata.historical_data import TimeBarPeriods

class ModelTypes(Enum):
    RATE = 1
    HIGH_LOW = 2
    HIGH_LOW_STAY = 3
    LSTM = 4
MODEL_TYPE:ModelTypes = ModelTypes.HIGH_LOW_STAY

class LearningPeriods(Enum):
    CURRENT = 1
    ALL = 2

LEARNING_PERIOD:LearningPeriods = LearningPeriods.ALL
LEARNING_TimeBarPeriods:TimeBarPeriods = TimeBarPeriods.H1

IS_SAVE_MODEL:bool = True
IS_LOAD_MODEL:bool = False