# -*- coding: utf-8 -*-
from keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint, LearningRateScheduler
import os
from models.model_settings import ModelSettings

class HighLowModelSettings(ModelSettings):

    def step_decay(epoch):
        x = 0.0000001
        roop = epoch
        weight = 0.9 ** roop
        x = x * weight
        return x

    learning_lr = LearningRateScheduler(step_decay)    

    @property
    def base_dir(self) -> str:
        return os.path.join("models", "highlow")

    @property
    def batch_size(self) -> int:
        return 1024

    @property
    def epochs(self) -> int:
        return 3000

    @property
    def callbacks(self) -> list:
        earlyStopping = EarlyStopping(monitor='loss', min_delta=0.0001, patience=100)
        checkpoint = ModelCheckpoint(filepath=os.path.join(self.model_current_dir, "model-{epoch:02d}.h5"), monitor='loss', save_best_only=True)
        # reduce_lr = ReduceLROnPlateau(monitor='loss', factor=0.9, patience=2, min_delta=0.00001)
        # return [earlyStopping, checkpoint, self.learning_lr, reduce_lr]
        return [earlyStopping, checkpoint]
    
    @property
    def metrics(self) -> str:
        return "accuracy"

    @property
    def time_step(self) -> int:
        return 100
