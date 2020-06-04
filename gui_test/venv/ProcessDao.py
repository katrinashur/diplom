import json


class ProcessDao:

    __path_db = ''

    def __init__(self):
        self.__path_db = 'DB/db/processes.json'

    def get_processes(self):
        processes = []
        with open(self.__path_db) as json_file:
            data = json.load(json_file)
            for p in data['processes']:
                processes.append([p['name'], p['pipe']])
        return processes
