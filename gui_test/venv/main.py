import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import (QMainWindow, QTextEdit, QAction, QFileDialog, QApplication,
                             QDialog, QTableWidgetItem, QHBoxLayout)
from PyQt5.QtGui import QRegExpValidator
import json
import form
import time
import cv2
import psutil
from ExperimentService import ExperimentService
from ExperimentDao import ExperimentDao
from datetime import datetime, timedelta
from ExperimentError import ExperimentError


class MainWindow(QtWidgets.QMainWindow, form.Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.experiment_service = ExperimentService()

        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.start.clicked.connect(self.start_experiment)
        self.stop.clicked.connect(self.stop_experiment)
        self.delete_2.clicked.connect(self.delete_experiment)
        self.experimentName.setText(datetime.now().strftime("%Y-%m-%d.%H_%M_%S.%f"))
        self.update.clicked.connect(self.update_name)
        self.error_action(self.update_table())
        self.complete.clicked.connect(self.post_processing_data)
        self.include.clicked.connect(self.include_in_dataset)

        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.check_process)
        self.stop.hide()


        regexp_str = "[A-Za-z0-9\.\_\-]+"
        self.experimentName.setValidator(QRegExpValidator(QtCore.QRegExp(regexp_str)))

        self.exp_in_process = False
        self.res_in_process = False


    def checkIfProcessRunning(self, processName):
        # Iterate over the all the running process
        for proc in psutil.process_iter():
            try:
                # Check if process name contains the given name string.
                if processName.lower() in proc.name().lower():
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return False

    def update_name(self):
        self.experimentName.setText(datetime.now().strftime("%Y-%m-%d.%H_%M_%S.%f"))

    def closeEvent(self, e):
        if self.exp_in_process or self.res_in_process:
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
                self.stop_experiment()
                e.accept()
            elif msgBox.clickedButton() == noBtn:
                e.ignore()

    # def update_buttons(self, row, column):
    #     is_completed = self.experiments.item(row, 2).text()
    #     is_included = self.experiments.item(row, 3).text()
    #     if is_completed == 'Нет':
    #         self.complete.show()
    #     else:
    #         self.complete.hide()
    #
    #     if is_included == 'Нет':
    #         self.include.show()
    #     else:
    #         self.include.hide()

    def update_table(self):
        self.experiments.setRowCount(0)
        self.experiments.clear()
        labels = ['Название', 'Дата и время', 'Обработан', 'В выборке']
        self.experiments.setColumnCount(len(labels))
        self.experiments.setHorizontalHeaderLabels(labels)

        exps = self.experiment_service.get_experiments()
        self.error_action(exps[1])
        for e in exps[0]:
            row = self.experiments.rowCount()
            self.experiments.setRowCount(row + 1)

            self.experiments.setItem(row, 0, QTableWidgetItem(e.name))
            self.experiments.setItem(row, 1, QTableWidgetItem(e.datetime))
            if e.is_completed == 1:
                self.experiments.setItem(row, 2, QTableWidgetItem("Да"))
            else:
                self.experiments.setItem(row, 2, QTableWidgetItem("Нет"))

            if e.is_included == 1:
                self.experiments.setItem(row, 3, QTableWidgetItem('Да'))
            else:
                self.experiments.setItem(row, 3, QTableWidgetItem('Нет'))

    # def check_before_experiment(self):
    #     is_ready = True
    #     cap = cv2.VideoCapture(0)
    #     if not cap.isOpened():
    #         self.show_message_box('Ошибка!', 'Не удается установить соединение с веб-камерой!')
    #         is_ready = False
    #     cap.release()
    #     #todo: проверить epoc+
    #     if is_ready:
    #         self.start_experiment()

    def start_experiment(self):
        if self.checkIfProcessRunning('RecordVideo.exe') or self.checkIfProcessRunning('BrainWavesCollect.exe'):
            self.show_message_box('Ошибка!', 'Эксперимент уже был запущен!')
            return
        if self.res_in_process or self.exp_in_process:
            return
        if len(self.experimentName.text()) > 0:
            name = self.experimentName.text()
            exp = self.experiment_service.get_experiment(name)
            self.error_action(exp[1])
            if exp[0] is None and exp[1] == ExperimentError.OK:
                self.exp_in_process = True
                self.stop.show()
                self.start.hide()
                self.experiment_service.start_record(name)
                time.sleep(1)
                self.label_2.setText('Эксперимент начался')
                self.timer.start()
            elif exp[0] is not None:
                self.show_message_box('Ошибка', 'Эксперимент с таким именем существует. Выберите другое имя.')
        else:
            self.show_message_box('Ошибка!', 'Введите имя эксперимента!')


    def check_process(self):
        self.timer.stop()
        experiment_error = self.experiment_service.check_process()
        if experiment_error == ExperimentError.OK:
            self.timer.start()
        else:
            self.error_action(experiment_error)
            self.stop_experiment()


    def stop_experiment(self):
        self.start.show()
        self.stop.hide()
        self.exp_in_process = False
        self.label_2.setText('Пожалуйста, подождите...')
        self.error_action(self.experiment_service.stop_record())
        self.error_action(self.update_table())
        self.label_2.setText('')

    def post_processing_data(self):
        if self.exp_in_process:
            return
        row = self.experiments.currentRow()
        if row != -1 and self.experiments.item(row, 2).text() != 'Да':
            self.res_in_process = True
            self.label_2.setText('Пожалуйста, подождите...')
            name = self.experiments.item(row, 0).text()
            self.error_action(self.experiment_service.process_data(name))
            self.error_action(self.update_table())
            self.res_in_process = False
            self.label_2.setText('')

    def include_in_dataset(self):
        if self.exp_in_process or self.res_in_process:
            return
        row = self.experiments.currentRow()
        if row != -1 and self.experiments.item(row, 3).text() != 'Да' and self.experiments.item(row, 2).text() == 'Да':
            self.res_in_process = True
            name = self.experiments.item(row, 0).text()
            self.error_action(self.experiment_service.include_in_dataset(name))
            self.error_action(self.update_table())
            self.res_in_process = False

    def delete_experiment(self):
        if self.exp_in_process or self.res_in_process:
            return
        row = self.experiments.currentRow()
        if row != -1:
            name = self.experiments.item(row, 0).text()
            self.error_action(self.experiment_service.delete_experiment(name))
            self.error_action(self.update_table())

    def error_action(self, error):
        if error == ExperimentError.NO_BRAIN_WAVES:
            self.show_message_box('Ошибка!', 'Во время эксперимента не произошло измерения мозговых сигналов!'
                                        '\n Проверьте устройство EPOC+')
        elif error == ExperimentError.NO_FACE:
            self.show_message_box('Ошибка!', 'Не удалось найти лицо на записи эксперимента!')
        elif error == ExperimentError.NO_CONNECTION_TO_CAMERA:
            self.show_message_box('Ошибка!', 'Не удается установить соединение с веб-камерой!')
        elif error == ExperimentError.NO_CONNECTION_TO_EPOC:
            self.show_message_box('Ошибка!', 'Не удается установить соединение с устройством EPOC+!')
        elif error == ExperimentError.INCORRECT_DB:
            self.show_message_box('Ошибка!', 'Проверьте сохранность файлов базы данных и файлов экспериментов.')
        elif error == ExperimentError.PERMISSION_ERROR:
            self.show_message_box('Предупреждение', 'Возможно не удалось удалить результаты эксперимента, '
                                             '\nтак как файлы или папка кем-то используются')
        elif error == ExperimentError.LOST_PROCESS:
            self.show_message_box('Ошибка!', 'Было потеряно соединение с одним из считывающих данные процессом.')

    def show_message_box(self, title, message):
        msgBox = QtWidgets.QMessageBox(self)
        msgBox.setWindowTitle(title)
        msgBox.setText(message)
        msgBox.addButton('Ок', QtWidgets.QMessageBox.AcceptRole)
        msgBox.exec_()


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()


