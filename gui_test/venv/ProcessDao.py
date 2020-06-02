import json


class ProcessDao:

    @staticmethod
    def get_processes():
        processes = []
        with open('DB/db/processes.json') as json_file:
            data = json.load(json_file)
            for p in data['processes']:
                processes.append([p['name'], p['pipe']])
        return processes
