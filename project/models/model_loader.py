# -*- coding: utf-8 -*-
from models.models import Models
from models.highlowstay.model import HighLowStayModel
from models.highlow.model import HighLowModel
from models.rate.model import RateModel
from models.lstm.model import LSTMModel
from models.highlow.model_settings import HighLowModelSettings
from models.highlowstay.model_settings import HighLowStayModelSettings
from models.rate.model_settings import RateModelSettings
from models.lstm.model_settings import LSTMModelSettings
from historicaldata.attribute import Attribute
import settings
from settings import ModelTypes
from historicaldata.historical_data import TimeBarPeriods

def load(attribute:Attribute, timeBarPeriods:TimeBarPeriods) -> Models:
    if settings.MODEL_TYPE == ModelTypes.RATE:
        return RateModel(RateModelSettings(timeBarPeriods), attribute)
    elif settings.MODEL_TYPE == ModelTypes.HIGH_LOW:
        return HighLowModel(HighLowModelSettings(timeBarPeriods), attribute)
    elif settings.MODEL_TYPE == ModelTypes.HIGH_LOW_STAY:
        return HighLowStayModel(HighLowStayModelSettings(timeBarPeriods), attribute)
    elif settings.MODEL_TYPE == ModelTypes.LSTM:
        return LSTMModel(LSTMModelSettings(timeBarPeriods), attribute)
