import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QMainWindow, QTextEdit, QAction, QFileDialog, QApplication)
from PyQt5.QtGui import QIcon
import form  # Это наш конвертированный файл дизайна
import subprocess
import win32pipe, win32file, pywintypes
import time


class ExampleApp(QtWidgets.QMainWindow, form.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.start.clicked.connect(self.start_experiment)
        self.stop.clicked.connect(self.stop_experiment)

        self.videoRecorder = VideoRecorder('')
        self.openDirectory.clicked.connect(self.open_folder)
        self.dir = ''

    def open_folder(self):
        folder = str(QFileDialog.getExistingDirectory(self, "Open folder"))
        self.experiment_path.setText(folder)

    def start_experiment(self):
        experiment_path = self.experimentPath.text()
        self.videoRecorder.start_record()
        print(experiment_path)

    def stop_experiment(self):
        self.videoRecorder.stop_record()


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


class VideoRecorder():
    def __init__(self, experiment_path):
        self.experiment_path = experiment_path
        self.proc = None
        self.handle = None

    def start_record(self):
        cmd = 'RecordVideo.exe ' #+ self.experiment_path
        import subprocess
        PIPE = subprocess.PIPE
        self.proc = subprocess.Popen(cmd, stdin=PIPE, stdout=PIPE)  # запускаем запись видео
        time.sleep(3)
        self.handle = win32file.CreateFile(
            r'\\.\pipe\demo_pipe',
            win32file.GENERIC_WRITE,
            0,
            None,
            win32file.OPEN_EXISTING,
            0,
            None)

    def stop_record(self):
        test_data = "0".encode("ascii")
        win32file.WriteFile(self.handle, test_data)  # команда закончить работу!


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()


