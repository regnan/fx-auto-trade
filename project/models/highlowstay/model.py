# -*- coding: utf-8 -*-
import numpy as np
from numpy import ndarray
from keras.models import Sequential
from keras.layers import Dense, Dropout, BatchNormalization
from keras import optimizers
from sklearn.preprocessing import MinMaxScaler
from historicaldata.attribute import Attribute
from models.models import Models, LearningParam, ResultTypes
from keras.layers.recurrent import LSTM
import settings

class HighLowStayModel(Models):

    def generate_learning_param(self, attribute:Attribute) -> LearningParam:
        params = LearningParam()
        # params.add(attribute.year.astype(np.int))
        # params.add(attribute.month.astype(np.int))
        # params.add(attribute.date.astype(np.int))
        # params.add(attribute.hour.astype(np.int))
        # params.add(attribute.minute.astype(np.int))
        # params.add(attribute.open.astype(np.float))
        # params.add(attribute.high.astype(np.float))
        # params.add(attribute.low.astype(np.float))
        # params.add(attribute.close.astype(np.float))
        # params.add(attribute.close2.astype(np.float))
        params.add(attribute.volume.astype(np.int))

        # params.add(attribute.before1_diff.astype(np.float))
        # params.add(attribute.before2_diff.astype(np.float))
        # params.add(attribute.before3_diff.astype(np.float))
        # params.add(attribute.before4_diff.astype(np.float))
        # params.add(attribute.before5_diff.astype(np.float))

        # params.add(attribute.bollinger_bands_diff.get(10))
        # params.add(attribute.bollinger_bands_diff.get(15))
        params.add(attribute.bollinger_bands_diff.get(20))
        # params.add(attribute.bollinger_bands_diff.get(25))
        params.add(attribute.rsi.get(9))
        params.add(attribute.rsi.get(14))
        params.add(attribute.rsi.get(26))
        # params.add(attribute.rci.get(9))
        # params.add(attribute.rci.get(14))
        # params.add(attribute.rci.get(26))
        params.add(attribute.sma_diff.get(5))
        params.add(attribute.sma_diff.get(20))
        params.add(attribute.sma_diff.get(25))
        params.add(attribute.sma_diff.get(50))
        # params.add(attribute.sma_diff.get(75))
        # params.add(attribute.sma_diff.get(200))
        # params.add(attribute.dema_diff.get(5))
        # params.add(attribute.dema_diff.get(25))
        # params.add(attribute.dema_diff.get(50))
        # params.add(attribute.sar_diff)
        params.add(attribute.macd)
        params.add(attribute.trend_line_high)
        params.add(attribute.trend_line_low)
        params.add(attribute.gc50_25)
        params.add(attribute.gc50_5)
        params.add(attribute.gc25_5)
        params.add(attribute.upper_shadow)
        params.add(attribute.lower_shadow)
        return params

    def generate_learning_collect_answer(self, attribute:Attribute) -> LearningParam:
        diff = (attribute.close - attribute.after1_close).astype(np.float)

        answers = LearningParam()
        answers.add((diff <= -0.05).astype(np.int))
        answers.add(((diff > -0.05) & (diff < 0.05)).astype(np.int))
        answers.add((diff >= 0.05).astype(np.int))
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
        model.add(Dense(3, activation='softmax'))

        adagrad = optimizers.adagrad_v2.Adagrad()
        model.compile(loss='categorical_crossentropy', metrics=[self.model_settings.metrics], optimizer=adagrad)
        return model

    def generate_xtrain_scaler(self) -> MinMaxScaler:
        return MinMaxScaler(feature_range=(-1, 1))

    def generate_ytrain_scaler(self) -> MinMaxScaler:
        return MinMaxScaler(feature_range=(0, 1))

    def predict_result(self) -> ndarray:
        result = np.array([np.argmax(i) for i in self.predictions])
        y_train = np.delete(self.y_train, slice(len(self.y_train) - len(result)), 0)
        y_train = np.array([np.argmax(i) for i in y_train])
        x_train = np.delete(self.x_train, slice(len(self.x_train) - len(result)), 0)

        closeIndex = 3
        count = 0
        trueCount = 0
        tradecount = 0
        total = 0
        for i in range(len(result)-1):
            count = count + 1
            if(y_train[i] == result[i]):
                trueCount = trueCount + 1
            if(y_train[i] == 0):
                tradecount = tradecount + 1
                total = total + (x_train[i+1][closeIndex] - x_train[i][closeIndex])
            if(y_train[i] == 2):
                tradecount = tradecount + 1
                total = total + (x_train[i][closeIndex] - x_train[i+1][closeIndex])
        
        print('count: ' + str(count))
        print('trueCount: ' + str(trueCount))
        print('tradecount: ' + str(tradecount))
        print('total: ' + str(total))

        return self.predictions

    def predict_result_type(self) -> ResultTypes:
        train = self.x_train
        result = self.ytrain_scaler.inverse_transform(self.predictions)

        print('up: ' + str(result[-1][0]))
        print('stay: ' + str(result[-1][1]))
        print('down: ' + str(result[-1][2]))
        print('current:' + str(self.x_train[-1][3]))

        if result[-1][0] > 0.60:
            return ResultTypes.BUY
        elif result[-1][2] > 0.60:
            return ResultTypes.SELL
        else:
            return ResultTypes.STAY
  