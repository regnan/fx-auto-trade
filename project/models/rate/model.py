# -*- coding: utf-8 -*-
import numpy as np
from numpy import ndarray
from keras.models import Sequential
from keras.layers import Dense, Dropout, BatchNormalization
from keras import optimizers
from keras.metrics import MeanAbsoluteError
from sklearn.preprocessing import MinMaxScaler
from historicaldata.attribute import Attribute
from models.models import Models, LearningParam, ResultTypes
from keras.layers.recurrent import LSTM

class RateModel(Models):

    def generate_learning_param(self, attribute:Attribute) -> LearningParam:
        params = LearningParam()
        # params.add(attribute.year.astype(np.int))
        # params.add(attribute.month.astype(np.int))
        # params.add(attribute.date.astype(np.int))
        # params.add(attribute.hour.astype(np.int))
        # params.add(attribute.minute.astype(np.int))
        params.add(attribute.open.astype(np.float))
        params.add(attribute.high.astype(np.float))
        params.add(attribute.low.astype(np.float))
        params.add(attribute.close.astype(np.float))
        params.add(attribute.volume.astype(np.int))

        params.add(attribute.before1_diff.astype(np.float))
        params.add(attribute.before2_diff.astype(np.float))
        params.add(attribute.before3_diff.astype(np.float))
        params.add(attribute.before4_diff.astype(np.float))
        params.add(attribute.before5_diff.astype(np.float))

        params.add(attribute.bollinger_bands_diff.get(10))
        params.add(attribute.bollinger_bands_diff.get(15))
        params.add(attribute.bollinger_bands_diff.get(20))
        params.add(attribute.rsi.get(9))
        params.add(attribute.rsi.get(15))
        params.add(attribute.sma_diff.get(5))
        params.add(attribute.sma_diff.get(25))
        params.add(attribute.sma_diff.get(50))
        params.add(attribute.macd)
        params.add(attribute.trend_line)
        return params

    def generate_learning_collect_answer(self, attribute:Attribute) -> LearningParam:
        answers = LearningParam()
        answers.add(attribute.after1_close.reshape(-1, 1))
        return answers

    def generate_learning_model(self, param_count:int) -> Sequential:
        model = Sequential()
        
        model.add(LSTM(512, batch_input_shape=(None, param_count, self.model_settings.time_step), return_sequences=True))
        model.add(Dropout(0.1))
        model.add(BatchNormalization())
        model.add(LSTM(256, batch_input_shape=(None, param_count, self.model_settings.time_step), return_sequences=True))
        model.add(Dropout(0.1))
        model.add(BatchNormalization())
        model.add(LSTM(256, batch_input_shape=(None, param_count, self.model_settings.time_step), return_sequences=False))
        model.add(Dropout(0.1))
        model.add(BatchNormalization())
        model.add(Dense(256, activation='tanh'))
        model.add(Dropout(0.1))
        model.add(Dense(128, activation='tanh'))
        model.add(Dropout(0.1))
        model.add(BatchNormalization())
        model.add(Dense(64, activation='tanh'))
        model.add(Dropout(0.1))
        model.add(BatchNormalization())
        model.add(Dense(32, activation='tanh'))
        model.add(BatchNormalization())
        model.add(Dense(1, activation='relu'))

        adagrad = optimizers.adagrad_v2.Adagrad()
        mae = MeanAbsoluteError(name="mean_absolute_error", dtype=float)
        model.compile(loss='mean_absolute_error', metrics=mae, optimizer=adagrad)
        return model

    def generate_xtrain_scaler(self) -> MinMaxScaler:
        return MinMaxScaler(feature_range=(-1, 1))

    def generate_ytrain_scaler(self) -> MinMaxScaler:
        return MinMaxScaler(feature_range=(0, 1))

    def predict_result(self) -> ndarray:
        result = self.ytrain_scaler.inverse_transform(self.predictions)
        return result

    def predict_result_type(self) -> ResultTypes:
        train = np.delete(self.x_train, slice(0, self.model_settings.time_step), 0)
        result = self.ytrain_scaler.inverse_transform(self.predictions)

        diff = result[-1] - train[-1][3]
        print(diff)
        if diff > 0.005:
            return ResultTypes.BUY
        elif diff < -0.005: 
            return ResultTypes.SELL
        else:
            return ResultTypes.STAY