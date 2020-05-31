import subprocess
import win32pipe, win32file, pywintypes
from pywintypes import com_error
import time
import os


class Recorder:

    def __init__(self, experiment_path):
        self.processes = [('BrainWavesCollect.exe', r'\\.\pipe\brain_pipe'), ('RecordVideo.exe',  r'\\.\pipe\video_pipe')]
        self.proc = []
        self.handle = []

    def start(self, experiment_info):
        for i in range(len(self.processes)):
            args = self.processes[i][0] + ' ' + self.processes[i][1] + ' ' + experiment_info[0] + ' ' + experiment_info[1]
            print(args)
            PIPE = subprocess.PIPE
            self.proc.append(subprocess.Popen(args))  # запускаем запись видео
            print(self.proc)
            time.sleep(3)
            try:
                self.handle.append(win32file.CreateFile(
                    self.processes[i][1],
                    win32file.GENERIC_WRITE,
                    0,
                    None,
                    win32file.OPEN_EXISTING,
                    0,
                    None))
            except pywintypes.error as e:
                if e.args[0] == 2:
                    print("no pipe")
                    time.sleep(1)
                elif e.args[0] == 109:
                    print("broken pipe")

    def stop(self):
        for i in range(len(self.processes)):
            test_data = "0".encode("ascii")
            try:
                win32file.WriteFile(self.handle[i], test_data)  # команда закончить работу!
            except pywintypes.error as e:
                if e.args[0] == 109:
                    print("broken pipe")
