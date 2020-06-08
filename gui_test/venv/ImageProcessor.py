# -*- coding: utf-8 -*-
import cv2
import copy


class ImageProcessor(object):

    @staticmethod
    def find_faces(image_path):

        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=3, minSize=(30, 30))
        vector_array = []
        print("[INFO] Found {0} Faces!".format(len(faces)))

        for (x, y, w, h) in faces:

            cv2.rectangle(image, (x + int(0.15 * h), y + int(0.2 * w)), (x + int(h * 0.85), y + w), (255, 165, 0), 2)

            roi_color = image[y + int(0.2 * w):y + w, x + int(0.15 * h):x + int(h * 0.85)]

            print("[INFO] Object found.")
            dim = (48, 48)
            # resize image
            resized = cv2.resize(roi_color, dim, interpolation=cv2.INTER_AREA)
            gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
            vector_array.append(gray)

        return vector_array
