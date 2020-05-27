# -*- coding: utf-8 -*-

from tensorflow.keras.models import load_model
import numpy as np


class EmotionAnalyzer:
    __model = ''

    __emotions = {
        0: "Angry",
        1: "Disgust",
        2: "Fear",
        3: "Happy",
        4: "Sad",
        5: "Surprise",
        6: "Neutral"
    }

    def __init__(self):
        self.__model = load_model('EmoModel')
        self.__model.summary()

    def predict(self, image):
        flatten_image = image.flatten()
        s = np.array([[float(n) / 255 for n in flatten_image]])

        pred = self.__model.predict(s)
        return pred






