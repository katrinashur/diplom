import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import (QMainWindow, QTextEdit, QAction, QFileDialog, QApplication, QDialog)
from PyQt5.QtGui import QIcon
import form  # Это наш конвертированный файл дизайна
from StoreManager import DataManager
from Experiment import Experiment


class ErrorWindow(QtWidgets.QMessageBox):
    def __init__(self, parent=None):
        QtWidgets.QMessageBox.__init__(self, parent)
        self.setWindowTitle("Предупреждение")
        self.setText("Эксперимент не закончен, возможна частичная потеря результатов. Закрыть?")
        # msgBox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        self.btnBox = QtWidgets.QDialogButtonBox(self)
        self.btnBox.addButton(QtWidgets.QPushButton("&Да"), QtWidgets.QDialogButtonBox.YesRole)
        self.btnBox.addButton(QtWidgets.QPushButton("&Нет"), QtWidgets.QDialogButtonBox.NoRole)

        self.hbox = QtWidgets.QHBoxLayout()
        self.hbox.addWidget(self.btnBox)
        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.addStretch(1)
        self.vbox.addLayout(self.hbox)

        self.setLayout(self.vbox)

        self.setWindowTitle("Предупреждение")
        self.setText("Эксперимент не закончен, возможна частичная потеря результатов. Закрыть?")
        correctBtn = msgBox.addButton('Correct', QtWidgets.QMessageBox.YesRole)
        incorrectBtn = msgBox.addButton('Incorrect', QtWidgets.QMessageBox.NoRole)
        cancelBtn = msgBox.addButton('Cancel', QtWidgets.QMessageBox.RejectRole)


class MainWindow(QtWidgets.QMainWindow, form.Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.start.clicked.connect(self.start_experiment)
        self.stop.clicked.connect(self.stop_experiment)
        self.openDirectory.clicked.connect(self.open_folder)
        self.experiment = Experiment()

        self.experimentName.setText(self.experiment.name)
        self.experimentPath.setText(self.experiment.folder)
        self.stop.hide()
        self.exp_in_process = True
        self.res_in_process = False

    def closeEvent(self, e):
        if  self.exp_in_process and self.res_in_process: # исправить потом на True
            msgBox = QtWidgets.QMessageBox()
            msgBox.setWindowTitle("Предупреждение")
            if self.exp_in_process:
                msgBox.setText("Эксперимент не закончен, возможна частичная потеря результатов. Закрыть?")
            elif self.res_in_process:
                msgBox.setText(
                    "Обработка результатов эксперимента не закончена, возможна частичная потеря результатов. Закрыть?")

            yesBtn = msgBox.addButton('Да', QtWidgets.QMessageBox.YesRole)
            noBtn = msgBox.addButton('Нет', QtWidgets.QMessageBox.NoRole)
            msgBox.exec_()

            if msgBox.clickedButton() == yesBtn:
                e.accept()
            elif msgBox.clickedButton() == noBtn:
                e.ignore()

    def open_folder(self):
        path = str(QFileDialog.getExistingDirectory(self, "Open folder"))
        self.experimentPath.setText(path)

    def start_experiment(self):
        if len(self.experimenName.text()) != 0:
            self.experiment.set_name(self.experimentName.text())
        if len(self.experimentPath.text()) != 0:
            self.experiment.set_folder(self.experimentPath.text())
        self.exp_in_process = True
        self.stop.show()
        self.start.hide()
        self.experiment.start_record()
        # todo: ловить ошибки

    def stop_experiment(self):
        if self.experiment.stop_record():
            self.exp_in_process = False
            self.start.show()
            self.stop.hide()

    def process_data(self):
        self.experiment.save_results()


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = MainWindow()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()


