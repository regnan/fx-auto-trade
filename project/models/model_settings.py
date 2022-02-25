# -*- coding: utf-8 -*-
import os
from abc import ABCMeta, abstractmethod
from historicaldata.historical_data import TimeBarPeriods
from datetime import datetime

class ModelSettings(metaclass=ABCMeta):
    
    def __init__(self, timeBarPeriods:TimeBarPeriods):
        self.__periods = timeBarPeriods

    @property
    def base_dir(self) -> str:
        pass

    @property
    def model_dir(self) -> str:
        return os.path.join(self.base_dir, str(self.__periods.name))

    @property
    def model_current_dir(self) -> str:
        return os.path.join(self.model_dir, "model")

    @property
    def model_history_dir(self) -> str:
        return os.path.join(self.model_dir, "history", datetime.now().strftime('%Y%m%d_%H%M%S'))

    @property
    @abstractmethod
    def batch_size(self) -> int:
        pass

    @property
    @abstractmethod
    def epochs(self) -> int:
        pass

    @property
    @abstractmethod
    def callbacks(self) -> list:
        pass

    @property
    @abstractmethod
    def metrics(self) -> str:
        pass

