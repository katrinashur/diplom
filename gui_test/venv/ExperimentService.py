from datetime import datetime, timedelta
import os
import json
from Recorder import Recorder
from ImageProcessor import ImageProcessor
from EmotionAnalyzer import EmotionAnalyzer
from StoreManager import DataManager
from ExperimentError import ExperimentError
from ExperimentDao import ExperimentDao
from Experiment import Experiment


class ExperimentService:
    def __init__(self):
        self.recorder = Recorder()
        self.experiment = None
        self.folder = 'DB'
        self.experimentDao = ExperimentDao()

        self.emotions = []
        self.photos = []
        self.brain_waves = []
        self.res_dataset = []

    def start_record(self, name):
        self.experiment = Experiment(name)
        if not os.path.exists(self.folder + '\\' + self.experiment.name):
            os.mkdir(self.folder + '\\' + self.experiment.name)  #надо удалять если ошибка или создавать только после сигнала об
        try:
            self.recorder.start([self.experiment.name, self.folder + '\\' + self.experiment.name])
        except ValueError:
            return ExperimentError.INCORRECT_DB

    def stop_record(self):
        self.recorder.stop()
        try:
            self.experimentDao.save_experiment(self.experiment)
        except ValueError:
            return ExperimentError.INCORRECT_DB
        self.experiment = None
        return ExperimentError.OK    # ошибки закрытия процессов

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
                count_waves += 1

        return dataset

    def prepare_photos(self):
        # DB - папка с экспериментом - файл с логами фоток
        photos = DataManager.read_file(self.folder + '\\' + self.experiment.name + '\\'
                                       + 'photos_log.txt')
        for photo in photos:
            time = photo.rsplit('.', 1)[0]
            time = time.rsplit('\\', 1)[-1]
            self.photos.append([photo, time])

    def prepare_brain_waves(self):
        # DB - папка с экспериментом - файл с мозговыми волнами
        brain_waves_strings = DataManager.read_file(self.folder + '\\' + self.experiment.name
                                                    + '\\' + self.experiment.name + '.tsv')
        for line in brain_waves_strings:
            self.brain_waves.append(line.rsplit('\t', -1))
        self.brain_waves = self.brain_waves[1:]
        return len(self.brain_waves) != 0

    def prepare_emotions(self):
        no_face = True
        emo_analyzer = EmotionAnalyzer()
        for i in range(len(self.photos)):
            faces = ImageProcessor.find_faces(self.photos[i][0])
            element = []
            if len(faces) == 0:
                print('No face on ' + self.photos[i][0])
            elif len(faces) > 1:
                print('More than 1 face on ' + self.photos[i][0])
            else:
                no_face = False
                element.extend(emo_analyzer.predict(faces[0]))
            element.append(self.photos[i][-1])
            self.emotions.append(element)
        return no_face

    def make_dataset(self, dataset):
        print(dataset[0][-1])
        print(self.emotions[0][-1])
        print((datetime.strptime(dataset[0][-1], "%Y-%m-%d.%H_%M_%S.%f") - \
        datetime.strptime(self.emotions[0][-1], "%Y-%m-%d.%H_%M_%S.%f")).microseconds)
        count_waves = 0
        count_emotions = 0
        while count_waves < len(dataset) and count_emotions < len(self.emotions):
            if (datetime.strptime(dataset[count_waves][-1], "%Y-%m-%d.%H_%M_%S.%f") - \
                    datetime.strptime(self.emotions[count_emotions][-1], "%Y-%m-%d.%H_%M_%S.%f")).microseconds == 0:

                if len(self.emotions[count_emotions]) < 8:
                    # эмоции на фото не были определены
                    count_waves += 1
                    continue
                else:
                    dataset[count_waves] = dataset[count_waves][:len(dataset[count_waves])-2]
                    dataset[count_waves].extend(self.emotions[count_emotions])
                    self.res_dataset.append(dataset[count_waves])

            elif datetime.strptime(dataset[count_waves][-1], "%Y-%m-%d.%H_%M_%S.%f") > \
                    datetime.strptime(self.emotions[count_emotions][-1], "%Y-%m-%d.%H_%M_%S.%f"):
                count_emotions += 1
                count_waves -= 1

            count_waves += 1

    def process_data(self, name):
        # найдем в базе данных этот эксперимент
        if self.get_experiment(name)[0] is not None:
            self.experiment = self.get_experiment(name)[0]
        else:
            return ExperimentError.INCORRECT_DB

        if not self.prepare_brain_waves():
            return ExperimentError.NO_BRAIN_WAVES
        self.prepare_photos()
        if self.prepare_emotions():
            return ExperimentError.NO_FACE

        self.make_dataset(self.match_data())
        # DB - папка с экспериментом - конечный файл результатов этого экспермента
        DataManager.write_dataset(self.folder + '\\' + self.experiment.name +
                                  '\\' + 'res_' + self.experiment.name + '.tsv', self.res_dataset)
        self.experiment.is_completed = 1
        # теперь обновим запись эксперимента в базе данных
        self.update_experiment(self.experiment)

        return ExperimentError.OK

    def get_experiments(self):
        exps = []
        try:
            exps = self.experimentDao.get_experiments_obj()
        except (json.decoder.JSONDecodeError, FileNotFoundError):
            return [exps, ExperimentError.INCORRECT_DB]
        return [exps, ExperimentError.OK]

    def get_experiment(self, name):
        exp = None
        try:
            exp = self.experimentDao.get_experiment(name)
        except (json.decoder.JSONDecodeError, FileNotFoundError):
            return [exp, ExperimentError.INCORRECT_DB]
        return [exp, ExperimentError.OK]

    def update_experiment(self, experiment):
        try:
            self.experimentDao.update_experiment(experiment)
        except (json.decoder.JSONDecodeError, FileNotFoundError):
            return ExperimentError.INCORRECT_DB
        return ExperimentError.OK

    def delete_experiment(self,  name):
        # сначала удаляем все из папки
        photos = []
        try:
            if os.path.exists(self.folder + '\\' + name + '\\' + 'photos_log.txt'):
                photos = DataManager.read_file(self.folder + '\\' + name + '\\'
                                               + 'photos_log.txt')
                os.remove(self.folder + '\\' + name + '\\' + 'photos_log.txt')

            for p in photos:
                if os.path.exists(p):
                    os.remove(p)

            if os.path.exists(self.folder + '\\' + name + '\\' + name + '.tsv'):
                os.remove(self.folder + '\\' + name + '\\' + name + '.tsv')

            if os.path.exists(self.folder + '\\' + name + '\\' + 'res_' + name + '.tsv'):
                os.remove(self.folder + '\\' + name + '\\' + 'res_' + name + '.tsv')

            # потом удаляем саму папку
            if os.path.exists(self.folder + '\\' + name):
                os.rmdir(self.folder + '\\' + name)
        except PermissionError:
            return ExperimentError.PERMISSION_ERROR
        except FileNotFoundError:
            return ExperimentError.INCORRECT_DB

        # потом удаляем из базы данных
        try:
            self.experimentDao.delete_experiment(name)
        except (json.decoder.JSONDecodeError, FileNotFoundError):
            return ExperimentError.INCORRECT_DB
        return ExperimentError.OK

    def include_in_dataset(self, name):
        self.experiment = self.experimentDao.get_experiment(name)
        dataset = DataManager.read_file_str(self.folder + '\\' + self.experiment.name +
                              '\\' + 'res_' + self.experiment.name + '.tsv')
        dataset = dataset[1:]
        DataManager.add_to_file(self.folder + '\\' + 'result_dataset.tsv', dataset)

        self.experiment.is_included = 1
        self.experimentDao.update_experiment(self.experiment)








