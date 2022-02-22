# -*- coding: utf-8 -*-
from asyncio.windows_events import NULL
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout, BatchNormalization
from keras import optimizers
from keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint, LearningRateScheduler
import matplotlib.pyplot as plt
from tensorflow import keras
import os

MODEL_DIR = "my_model"

class PredictModel():
    def __init__(self):
        self.model = keras.models.load_model(MODEL_DIR)

    def predict(self, learningParam):
        return self.model.predict(learningParam.x_train)
    
    def result(self):
        if self.result is NULL:
            print('No result')
        return self.result


class LearningModel():
    batch_size = 1024
    epochs = 1
    earlyStopping = EarlyStopping(monitor='loss', min_delta=0.0001, patience=200)
    reduce_lr = ReduceLROnPlateau(monitor='loss', factor=0.9, patience=2, min_delta=0.00001)
    checkpoint = ModelCheckpoint(filepath=os.path.join(MODEL_DIR, "model-{epoch:02d}.h5"), monitor='loss', save_best_only=True)
    
    def step_decay(epoch):
        x = 0.0000001
        roop = epoch
        weight = 0.9 ** roop
        x = x * weight
        return x
    # def step_decay(epoch):
    #     x = 0.00005
    #     roop = int(epoch/30)
    #     weight = 0.9 ** roop
    #     return x * weight
    learning_lr = LearningRateScheduler(step_decay)
    callbacks = [earlyStopping, checkpoint]
    # callbacks = [earlyStopping, reduce_lr, checkpoint]

    def __init__(self, paramCount):
        model = Sequential()
        # model.add(Dense(1024, activation='sigmoid', input_shape=(paramCount,)))
        # model.add(Dropout(0.1))

        model.add(Dense(1024, activation='tanh', input_shape=(paramCount,)))
        model.add(Dropout(0.1))
        model.add(BatchNormalization())
        # model.add(Dropout(0.1))
        # model.add(LSTM(512))
        # model.add(BatchNormalization())
        model.add(Dense(1024, activation='tanh'))
        model.add(Dropout(0.1))
        model.add(BatchNormalization())
        model.add(Dense(512, activation='tanh'))
        model.add(Dropout(0.1))
        model.add(BatchNormalization())
        model.add(Dense(256, activation='tanh'))
        model.add(Dropout(0.1))
        model.add(BatchNormalization())
        model.add(Dense(64, activation='tanh'))
        model.add(BatchNormalization())
        model.add(Dense(16, activation='tanh'))
        model.add(BatchNormalization())
        
        # model.add(Dense(512, activation='tanh'))
        # model.add(BatchNormalization())
        # model.add(Dropout(0.1))
        # model.add(Dense(256, activation='tanh'))
        # model.add(BatchNormalization())
        # model.add(Dropout(0.1))
        # model.add(Dense(128, activation='tanh'))
        # model.add(BatchNormalization())
        # model.add(Dropout(0.1))

        # model.add(Dropout(0.1))
        # model.add(Dense(256, activation='relu'))
        #model.add(Dropout(0.1))


        # model.add(Dense(256, activation='sigmoid'))
        #mean_squared_error
        #categorical_crossentropy
        #logloss
        #binary_crossentropy
        # model.add(Dense(1, activation='sigmoid'))
        model.add(Dense(3, activation='softmax'))
        adam = optimizers.adam_v2.Adam(lr=0)
        # adam = optimizers.adagrad_v2.Adagrad()
        model.compile(loss='categorical_crossentropy', metrics=['accuracy'], optimizer=adam)
        # モデルの読み込み
        model.load_weights(os.path.join(MODEL_DIR, "latest.h5")) 
        self.__model = model
        print("complete model create")

    def learning(self, learningParam):
        history = self.__model.fit(learningParam.x_train, learningParam.y_train, batch_size=self.batch_size, epochs=self.epochs, verbose=1, validation_split=0.1, callbacks=self.callbacks)

        #正答率
        plt.plot(history.history['accuracy'])
        plt.plot(history.history['val_accuracy'])
        plt.title('model accuracy')
        plt.ylabel('accuracy')
        plt.xlabel('epoch')
        plt.legend(['train', 'test'], loc='upper left')
        plt.show()

        #損失関数
        plt.plot(history.history['loss'])
        plt.plot(history.history['val_loss'])
        plt.title('model loss')
        plt.ylabel('loss')
        plt.xlabel('epoch')
        plt.legend(['train', 'test'], loc='upper left')
        plt.show()

    def save(self):
        self.__model.save('my_model')
    