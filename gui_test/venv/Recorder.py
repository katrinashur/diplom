import subprocess
import win32pipe, win32file, pywintypes
import time
import os

class Recorder():

    def __init__(self, experiment_path):
        #self.experiment_path = experiment_path
        self.proc = []
        self.handle = []

    def start_record(self, process_info, experiment_info):
        args = process_info[0] + ' ' + process_info[1] + ' ' + experiment_info[0] + ' ' + experiment_info[1]
        print(args)
        PIPE = subprocess.PIPE
        os.mkdir(experiment_info[1])
        self.proc.append(subprocess.Popen(args, stdin=PIPE, stdout=PIPE))  # запускаем запись видео
        time.sleep(3) #надо подождать пока там создается пайп или попробовать здесь другие флаги
        self.handle.append(win32file.CreateFile(
            process_info[1],
            win32file.GENERIC_WRITE,
            0,
            None,
            win32file.OPEN_EXISTING,
            0,
            None))

    def stop_record(self):
        for i in range(len(self.proc)):
            test_data = "0".encode("ascii")
            win32file.WriteFile(self.handle[i], test_data)  # команда закончить работу!