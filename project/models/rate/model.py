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
        # params.add(attribute.before1_close.astype(np.float))
        # params.add(attribute.before2_close.astype(np.float))
        # params.add(attribute.before3_close.astype(np.float))
        # params.add(attribute.before4_close.astype(np.float))
        # params.add(attribute.before5_close.astype(np.float))

        # params.add(attribute.bollinger_bands.get(10))
        # params.add(attribute.bollinger_bands.get(11))
        # params.add(attribute.bollinger_bands.get(12))
        # params.add(attribute.bollinger_bands.get(13))
        # params.add(attribute.bollinger_bands.get(14))
        # params.add(attribute.bollinger_bands.get(15))
        # params.add(attribute.bollinger_bands.get(16))
        # params.add(attribute.bollinger_bands.get(17))
        # params.add(attribute.bollinger_bands.get(18))
        # params.add(attribute.bollinger_bands.get(19))
        # params.add(attribute.bollinger_bands.get(20))
        params.add(attribute.bollinger_bands_diff.get(10))
        # params.add(attribute.bollinger_bands_diff.get(11))
        # params.add(attribute.bollinger_bands_diff.get(12))
        # params.add(attribute.bollinger_bands_diff.get(13))
        # params.add(attribute.bollinger_bands_diff.get(14))
        # params.add(attribute.bollinger_bands_diff.get(15))
        # params.add(attribute.bollinger_bands_diff.get(16))
        # params.add(attribute.bollinger_bands_diff.get(17))
        # params.add(attribute.bollinger_bands_diff.get(18))
        # params.add(attribute.bollinger_bands_diff.get(19))
        params.add(attribute.bollinger_bands_diff.get(20))
        # params.add(attribute.rsi.get(10))
        # params.add(attribute.rsi.get(9))
        params.add(attribute.rsi.get(10))
        # params.add(attribute.rsi.get(11))
        # params.add(attribute.rsi.get(12))
        # params.add(attribute.rsi.get(13))
        # params.add(attribute.rsi.get(14))
        params.add(attribute.rsi.get(15))
        # params.add(attribute.sma.get(10))
        # params.add(attribute.sma.get(20))
        params.add(attribute.sma_diff.get(5))
        params.add(attribute.sma_diff.get(10))
        # params.add(attribute.sma_diff.get(15))
        # params.add(attribute.sma_diff.get(20))
        params.add(attribute.sma_diff.get(25))
        params.add(attribute.sma_diff.get(50))
        # params.add(attribute.macd)
        params.add(attribute.macd)
        return params

    def generate_learning_collect_answer(self, attribute:Attribute) -> LearningParam:
        answers = LearningParam()
        answers.add(attribute.after1_close.reshape(-1, 1))
        return answers

    def generate_learning_model(self, param_count:int) -> Sequential:
        model = Sequential()

        model.add(Dense(512, activation='tanh', input_shape=(param_count,)))
        model.add(Dropout(0.1))
        model.add(BatchNormalization())
        # model.add(Dense(1024, activation='tanh'))
        # model.add(Dropout(0.1))
        # model.add(BatchNormalization())
        # model.add(Dense(512, activation='tanh'))
        # model.add(Dropout(0.1))
        # model.add(BatchNormalization())
        model.add(Dense(256, activation='tanh'))
        model.add(Dropout(0.1))
        model.add(BatchNormalization())
        model.add(Dense(64, activation='tanh'))
        model.add(BatchNormalization())
        model.add(Dense(16, activation='tanh'))
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
        train = self.y_train
        result = self.ytrain_scaler.inverse_transform(self.predictions)

        isOk = np.array(train == result)
        isNg = (train != result)
        print(isOk)
        print(isNg)
        print(np.count_nonzero(isOk == True))
        print(np.count_nonzero(isNg == True))
        return result

    def predict_result_type(self) -> ResultTypes:
        train = self.x_train
        result = self.ytrain_scaler.inverse_transform(self.predictions)

        isOk = np.array(train == result)
        isNg = (train != result)
        print(isOk)
        print(isNg)
        print(np.count_nonzero(isOk == True))
        print(np.count_nonzero(isNg == True))

        diff = result[-1] - train[-1][3]
        if diff > 0.005:
            return ResultTypes.BUY
        elif diff < -0.005: 
            return ResultTypes.SELL
        else:
            return ResultTypes.STAY