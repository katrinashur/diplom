from datetime import datetime, timedelta
import os
from Recorder import Recorder
from ImageProcessor import ImageProcessor
from EmotionAnalyzer import EmotionAnalyzer
from StoreManager import DataManager
from ExperimentError import ExperimentError

class Experiment:
    def __init__(self):
        self.name = datetime.now().strftime("%Y-%m-%d.%H_%M_%S.%f")
        self.folder = os.path.abspath(os.curdir) + '\\' + self.name
        self.recorder = Recorder('')

        self.emotions = []
        self.photos = []
        self.brain_waves = []
        self.res_dataset = []

    def set_name(self, name):
        self.name = name
        self.folder = self.rsplit('\\', 1)[0] + name

    def set_folder(self, folder):
        self.folder = folder + '\\' + self.name

    def start_record(self):
        os.mkdir(self.folder)  #надо удалять если ошибка или создавать только после сигнала об удаче
        self.recorder.start([self.name, self.folder])

    def stop_record(self):
        self.recorder.stop()
        self.save_results()
        return True

    def save_results(self):
        self.prepare_brain_waves()
        self.prepare_photos()
        self.prepare_emotions()
        self.make_dataset(self.match_data())
        DataManager.write_dataset(self.folder + '\\' + 'res_' + self.name + '.tsv', self.res_dataset)

    def match_data(self):
        count_waves = 1
        count_photos = 1
        dataset = []
        while count_waves < len(self.brain_waves) and count_photos < len(self.photos):
            # узнать время первого снимка
            time_begin = datetime.strptime(self.photos[count_photos-1][-1], "%Y-%m-%d.%H_%M_%S.%f")
            # узнать время следующего снимка
            time_end = datetime.strptime(self.photos[count_photos][-1], "%Y-%m-%d.%H_%M_%S.%f")
            # узнать время первого измерения мозговых волн
            current_time = datetime.strptime(self.brain_waves[count_waves-1][-1], "%Y-%m-%d.%H_%M_%S.%f")
            if current_time > time_end:
                count_photos += 1
            elif current_time < time_begin:
                count_waves += 1
            else:
                element = self.brain_waves[count_waves-1]
                element.extend(self.photos[count_photos])
                dataset.append(element)
                #dataset.append([self.brain_waves[count_waves-1], self.photos[count_photos]])
                count_waves += 1

        return dataset

    def prepare_photos(self):
        photos = DataManager.read_file(self.folder + '\\' + 'photos_log.txt')

        for photo in photos:
            time = photo.rsplit('.', 1)[0]
            time = time.rsplit('\\', 1)[-1]
            self.photos.append([photo, time])

    def prepare_brain_waves(self):
        brain_waves_strings = DataManager.read_file(self.folder + '\\' + self.name + '.tsv')
        for line in brain_waves_strings:
            self.brain_waves.append(line.rsplit('\t', -1))
        self.brain_waves = self.brain_waves[1:]
        return len(self.brain_waves) != 0

    def prepare_emotions(self):
        emo_analyzer = EmotionAnalyzer()
        #self.emotions.append(['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral'], 'time')
        for i in range(len(self.photos)):
            faces = ImageProcessor.find_faces(self.photos[i][0])  # что если несколько лиц?
            if len(faces) == 0:
                print('No face on ' + self.photos[i][0])
            elif len(faces) > 1:
                print('More than 1 face on ' + self.photos[i][0])
            else:
                element = []
                element.extend(emo_analyzer.predict(faces[0]))
                element.append(self.photos[i][-1])
                self.emotions.append(element)

    def make_dataset(self, dataset):
        print(dataset[0][-1])
        print(self.emotions[0][-1])
        print((datetime.strptime(dataset[0][-1], "%Y-%m-%d.%H_%M_%S.%f") - \
        datetime.strptime(self.emotions[0][-1], "%Y-%m-%d.%H_%M_%S.%f")).microseconds)
        count_waves = 0
        count_emotions = 0
        while count_waves < len(dataset):
            if (datetime.strptime(dataset[count_waves][-1], "%Y-%m-%d.%H_%M_%S.%f") - \
                    datetime.strptime(self.emotions[count_emotions][-1], "%Y-%m-%d.%H_%M_%S.%f")).microseconds == 0:
                dataset[count_waves] = dataset[count_waves][:len(dataset[count_waves])-2]
                dataset[count_waves].extend(self.emotions[count_emotions])
                self.res_dataset.append(dataset[count_waves])

            elif datetime.strptime(dataset[count_waves][-1], "%Y-%m-%d.%H_%M_%S.%f") > \
                    datetime.strptime(self.emotions[count_emotions][-1], "%Y-%m-%d.%H_%M_%S.%f"):
                count_emotions += 1
                count_waves -= 1

            count_waves += 1







