# -*- coding: utf-8 -*-
from models.models import Models
from models.highlowstay.model import HighLowStayModel
from models.rate.model import RateModel
from models.highlowstay.model_settings import HighLowStayModelSettings
from models.rate.model_settings import RateModelSettings
from historicaldata.attribute import Attribute
import settings
from settings import ModelTypes

def load(attribute:Attribute) -> Models:
    if settings.MODEL_TYPE == ModelTypes.RATE:
        return RateModel(RateModelSettings(attribute.period), attribute)
    elif settings.MODEL_TYPE == ModelTypes.HIGH_LOW:
        return HighLowStayModel(HighLowStayModelSettings(attribute.period), attribute)
    elif settings.MODEL_TYPE == ModelTypes.HIGH_LOW_STAY:
        return HighLowStayModel(HighLowStayModelSettings(attribute.period), attribute)
