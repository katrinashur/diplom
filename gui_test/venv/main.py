import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QMainWindow, QTextEdit, QAction, QFileDialog, QApplication)
from PyQt5.QtGui import QIcon
import form  # Это наш конвертированный файл дизайна
import subprocess
import win32pipe, win32file, pywintypes
import time
from ImageProcessor import ImageProcessor
from EmotionAnalyzer import EmotionAnalyzer
from Recorder import Recorder
from datetime import datetime
import os

class ExampleApp(QtWidgets.QMainWindow, form.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.start.clicked.connect(self.start_experiment)
        self.stop.clicked.connect(self.stop_experiment)
        self.test_button.clicked.connect(self.process_data)

        self.recorder = Recorder('')
        self.experiment_info = []
        self.experiment_info.append(datetime.now().strftime("%Y-%m-%d.%H_%M_%S.%f"))
        self.experiment_info.append( os.path.abspath(os.curdir) + '\\' + self.experiment_info[0])
        print(self.experiment_info)
        self.process_info = []
        self.process_info.append(['RecordVideo.exe',  r'\\.\pipe\video_pipe'])
        #self.process_info.append(['BrainWavesCollect.exe',  r'\\.\pipe\brain_pipe'])
        self.openDirectory.clicked.connect(self.open_folder)
        self.path = ''

    def open_folder(self):
        self.path = str(QFileDialog.getExistingDirectory(self, "Open folder"))
        self.experimentPath.setText(self.path)

    def start_experiment(self):
        if len(self.experimenName.text()) !=0:
            self.experiment_info[0] = self.experimenName.text()
            self.experiment_info[1] = "/" + self.experimenName.text()
        if len(self.experimentPath.text()) !=0:
            self.experiment_info[1] = self.experimentPath.text() + "/" + experiment_info[0]

        for i in range(len(self.process_info)):
            self.recorder.start_record(self.process_info[i], self.experiment_info)

    def stop_experiment(self):
        for i in range(len(self.process_info)):
            self.recorder.stop_record()    #завершаем работу всех процессов

    def process_data(self):  #тут обрабатываем результаты эксперимента
        faces = ImageProcessor.find_faces("D:/Documents/DIPLOM/rep/gui_test/venv/exp/foto.jpg")
        emo_analyzer = EmotionAnalyzer()
        result = emo_analyzer.predict(faces[1][0])
        print(result)


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


# class VideoRecorder():
#     def __init__(self, experiment_path):
#         self.experiment_path = experiment_path
#         self.proc = None
#         self.handle = None
#
#     def start_record(self):
#         cmd = 'RecordVideo.exe ' #+ self.experiment_path
#         import subprocess
#         PIPE = subprocess.PIPE
#         self.proc = subprocess.Popen(cmd, stdin=PIPE, stdout=PIPE)  # запускаем запись видео
#         time.sleep(3) #надо подождать пока там создается пайп или попробовать здесь другие флаги
#         self.handle = win32file.CreateFile(
#             r'\\.\pipe\demo_pipe',
#             win32file.GENERIC_WRITE,
#             0,
#             None,
#             win32file.OPEN_EXISTING,
#             0,
#             None)
#
#     def stop_record(self):
#         test_data = "0".encode("ascii")
#         win32file.WriteFile(self.handle, test_data)  # команда закончить работу!


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()


