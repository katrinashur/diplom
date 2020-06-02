import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import (QMainWindow, QTextEdit, QAction, QFileDialog, QApplication,
                             QDialog, QTableWidgetItem, QHBoxLayout)
from PyQt5.QtGui import QIcon
import form  # Это наш конвертированный файл дизайна
from StoreManager import DataManager
from ExperimentService import ExperimentService
from ExperimentDao import ExperimentDao
from datetime import datetime, timedelta
from ExperimentError import ExperimentError

# class ErrorWindow(QtWidgets.QMessageBox):
#     def __init__(self, parent=None):
#         QtWidgets.QMessageBox.__init__(self, parent)
#         self.setWindowTitle("Предупреждение")
#         self.setText("Эксперимент не закончен, возможна частичная потеря результатов. Закрыть?")
#         # msgBox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
#         self.btnBox = QtWidgets.QDialogButtonBox(self)
#         self.btnBox.addButton(QtWidgets.QPushButton("&Да"), QtWidgets.QDialogButtonBox.YesRole)
#         self.btnBox.addButton(QtWidgets.QPushButton("&Нет"), QtWidgets.QDialogButtonBox.NoRole)
#
#         self.hbox = QtWidgets.QHBoxLayout()
#         self.hbox.addWidget(self.btnBox)
#         self.vbox = QtWidgets.QVBoxLayout()
#         self.vbox.addStretch(1)
#         self.vbox.addLayout(self.hbox)
#
#         self.setLayout(self.vbox)
#
#         self.setWindowTitle("Предупреждение")
#         self.setText("Эксперимент не закончен, возможна частичная потеря результатов. Закрыть?")
#         correctBtn = msgBox.addButton('Correct', QtWidgets.QMessageBox.YesRole)
#         incorrectBtn = msgBox.addButton('Incorrect', QtWidgets.QMessageBox.NoRole)
#         cancelBtn = msgBox.addButton('Cancel', QtWidgets.QMessageBox.RejectRole)


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
        self.experiments.cellClicked.connect(self.update_buttons)
        self.complete.clicked.connect(self.post_processing_data)
        self.include.clicked.connect(self.include_in_dataset)
        #self.experiments.currentChanged(QModelIndex).connect(self.update_table)
        self.stop.hide()

        self.complete.hide()
        self.include.hide()

        self.exp_in_process = True
        self.res_in_process = False

    def update_name(self):
        self.experimentName.setText(datetime.now().strftime("%Y-%m-%d.%H_%M_%S.%f"))

    def closeEvent(self, e):
        if self.exp_in_process and self.res_in_process:
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

    def update_buttons(self, row, column):
        is_completed = self.experiments.item(row, 2).text()
        is_included = self.experiments.item(row, 3).text()
        if is_completed == 'Нет':
            self.complete.show()
        else:
            self.complete.hide()

        if is_included == 'Нет':
            self.include.show()
        else:
            self.include.hide()




    def update_table(self):
        self.experiments.clear()
        labels = ['Название', 'Дата и время', 'Обработан', 'В выборке']
        self.experiments.setColumnCount(len(labels))
        self.experiments.setHorizontalHeaderLabels(labels)

        exps = self.experiment_service.get_experiments()
        for e in exps:
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

    def start_experiment(self):
        name = self.experimentName.text()

        self.exp_in_process = True
        self.stop.show()
        self.start.hide()
        self.process_data.hide()
        self.experiment_service.start_record(name)
        # todo: ловить ошибки

    def stop_experiment(self):
        self.start.show()
        self.stop.hide()
        self.process_data.show()
        self.exp_in_process = False
        self.error_action(self.experiment_service.stop_record())
        self.error_action(self.update_table())

    def processing_data(self):
        name = self.experimentName.text()
        self.error_action(self.experiment_service.process_data(name))
        self.error_action(self.update_table())

    def post_processing_data(self):
        row = self.experiments.currentRow()
        name = self.experiments.item(row, 0).text()
        self.error_action(self.experiment_service.process_data(name))
        self.error_action(self.update_table())
        self.complete.hide()

    def include_in_dataset(self):
        row = self.experiments.currentRow()
        name = self.experiments.item(row, 0).text()
        self.error_action(self.experiment_service.include_in_dataset(name))
        self.error_action(self.update_table())
        self.include.hide()

    def delete_experiment(self):
        row = self.experiments.currentRow()
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
            show_message_box('Ошибка!', 'Файл, хранящий эксперименты некорректен или не существует.'
                                        '\n Проверьте DB/experiments.json')

    def show_message_box(self, title, message):
        msgBox = QtWidgets.QMessageBox(self)
        msgBox.setWindowTitle(title)
        msgBox.setText(message)
        msgBox.addButton('Ок', QtWidgets.QMessageBox.AcceptRole)
        msgBox.exec_()


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = MainWindow()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()


