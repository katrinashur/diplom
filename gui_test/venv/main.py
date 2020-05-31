import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QMainWindow, QTextEdit, QAction, QFileDialog, QApplication)
from PyQt5.QtGui import QIcon
import form  # Это наш конвертированный файл дизайна
from StoreManager import DataManager

from Experiment import Experiment


class ExampleApp(QtWidgets.QMainWindow, form.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.start.clicked.connect(self.start_experiment)
        self.stop.clicked.connect(self.stop_experiment)
        self.test_button.clicked.connect(self.process_data)
        self.openDirectory.clicked.connect(self.open_folder)
        self.experiment = Experiment()

    def open_folder(self):
        path = str(QFileDialog.getExistingDirectory(self, "Open folder"))
        self.experimentPath.setText(path)

    def start_experiment(self):
        if len(self.experimenName.text()) != 0:
            self.experiment.set_name(self.experimenName.text())
        if len(self.experimentPath.text()) != 0:
            self.experiment.set_folder(self.experimentPath.text())

        self.experiment.start_record()
        # todo: ловить ошибки

    def stop_experiment(self):
        self.experiment.stop_record()

    def process_data(self):
        self.experiment.save_results()



def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()


