# -*- coding: utf-8 -*-
from enum import Enum

class ModelTypes(Enum):
    RATE = 1
    HIGH_LOW = 2
    HIGH_LOW_STAY = 3
MODEL_TYPE:ModelTypes = ModelTypes.RATE

class LearningPeriods(Enum):
    CURRENT = 1
    ALL = 2
LEARNING_PERIOD:LearningPeriods = LearningPeriods.ALL

IS_SAVE_MODEL:bool = True
IS_LOAD_MODEL:bool = False
IS_SEARCH_FIRST_LEARNING_RATE:bool = False