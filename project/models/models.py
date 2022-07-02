# -*- coding: utf-8 -*-
from enum import Enum
import numpy as np
from numpy import ndarray
from keras.models import Sequential
import matplotlib.pyplot as plt
from tensorflow import keras
import os
import shutil
from sklearn.preprocessing import MinMaxScaler
from abc import ABCMeta, abstractmethod
from historicaldata.attribute import Attribute
import logger
import settings
from models.model_settings import ModelSettings

class ResultTypes(Enum):
    BUY = 0
    STAY = 1
    SELL = 2

class LearningParam:
    
    def __init__(self):
        self.__params:ndarray = None

    def add(self, param:ndarray):
        if self.__params is None:
            self.__params = np.array(param)
        else:
            self.__params = np.column_stack([self.__params, param])
    
    def params(self) -> ndarray:
        return np.array(self.__params)


class Models(metaclass=ABCMeta):
    
    def __init__(self, model_settings:ModelSettings, attribute:Attribute):
        # モデルの型に応じた設定を取得
        self.model_settings = model_settings

        # 学習用のパラメータと正解を作成
        print("start learning param generate")
        xtrain_params = self.generate_learning_param(attribute)
        ytrain_params = self.generate_learning_collect_answer(attribute)
        self.x_train = self.__remove_nun_rows(xtrain_params.params(), attribute)
        self.y_train = self.__remove_nun_rows(ytrain_params.params(), attribute)
        print("complete learning param generate")

        # データの正規化
        logger.log("Attribute transform start")
        self.xtrain_scaler = self.generate_xtrain_scaler()
        self.ytrain_scaler = self.generate_ytrain_scaler()
        self.xtrain_scaler.fit(self.x_train)
        self.ytrain_scaler.fit(self.y_train)
        self.transformed_xtrain = self.xtrain_scaler.transform(self.x_train)
        self.transformed_ytrain = self.ytrain_scaler.transform(self.y_train)
        logger.log("Attribute transform complete")

        self.transformed_xtrain,self.transformed_ytrain = self.create_dataset(self.transformed_xtrain, self.transformed_ytrain, self.model_settings.time_step)

    def create_dataset(self, dataset,y_t , look_back=1):
        dataX, dataY = [], []
        for i in range(len(dataset)-look_back-1):
            xset = []
            for j in range(dataset.shape[1]):
                a = dataset[i:(i+look_back), j]
                xset.append(a)
            dataY.append(y_t[i + look_back])      
            dataX.append(xset)
        return np.array(dataX), np.array(dataY)


    @abstractmethod
    def generate_learning_param(self, attribute:Attribute) -> LearningParam:
        pass

    @abstractmethod
    def generate_learning_collect_answer(self, attribute:Attribute) -> LearningParam:
        pass

    @abstractmethod
    def generate_learning_model(self, param_count:int) -> Sequential:
        pass

    @abstractmethod
    def generate_xtrain_scaler(self) -> MinMaxScaler:
        pass

    @abstractmethod
    def generate_ytrain_scaler(self) -> MinMaxScaler:
        pass

    @abstractmethod
    def predict_result(self) -> ndarray:
        pass

    @abstractmethod
    def predict_result_type(self) -> ResultTypes:
        pass

    def __remove_nun_rows(self, array:ndarray, attribute:Attribute) -> ndarray:
        return np.delete(array, slice(0, attribute.nun_value_index), 0)
        
    def learning(self):
        m_settings = self.model_settings

        # 以前学習済みのモデルが存在すればhistoryに移動しておく
        if(os.path.exists(m_settings.model_current_dir)):
            shutil.move(m_settings.model_current_dir, m_settings.model_history_dir)

        # モデルの構成を定義
        print("start learning model generate")
        model = self.generate_learning_model(self.x_train.shape[1])
        print("complete learning model generate")

        # 学習済みモデルの読み込み
        if settings.IS_LOAD_MODEL:
            model.load_weights(os.path.join(m_settings.model_dir, "latest.h5"))

        batch_size = m_settings.batch_size
        epochs = m_settings.epochs
        callbacks = m_settings.callbacks
        # self.transformed_xtrain = np.array(self.transformed_xtrain).reshape()
        history = model.fit(self.transformed_xtrain, self.transformed_ytrain, batch_size=batch_size, epochs=epochs, verbose=1, validation_split=0.2, callbacks=callbacks)

        # 学習したモデルの保存
        if settings.IS_SAVE_MODEL:
            model.save(m_settings.model_current_dir)

        # 正答率
        plt.plot(history.history[m_settings.metrics])
        plt.plot(history.history[f'val_{m_settings.metrics}'])
        plt.title('model accuracy')
        plt.ylabel('accuracy')
        plt.xlabel('epoch')
        plt.legend(['train', 'test'], loc='upper left')
        plt.show()

        # 損失関数
        plt.plot(history.history['loss'])
        plt.plot(history.history['val_loss'])
        plt.title('model loss')
        plt.ylabel('loss')
        plt.xlabel('epoch')
        plt.legend(['train', 'test'], loc='upper left')
        plt.show()

    def predict(self):
        model = keras.models.load_model(self.model_settings.model_current_dir)
        self.predictions = model.predict(self.transformed_xtrain)
        return self.predict_result()
  