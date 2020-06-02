import json
from StoreManager import DataManager
from Experiment import Experiment


class ExperimentDao:

    @staticmethod
    def get_experiments_obj():
        experiments = []
        with open('DB/db/experiments.json', "r") as json_file:
            string = json.load(json_file)
            data = json.loads(string)
            for e in data["experiments"]:
                exp = Experiment()
                exp.name = e["name"]
                exp.datetime = e["datetime"]
                exp.is_completed = e["is_completed"]
                exp.is_included = e["is_included"]
                experiments.append(exp)
        return experiments

    @staticmethod
    def get_experiments_dict():
        with open('DB/db/experiments.json') as json_file:
            string = json.load(json_file)
        return json.loads(string)

    @staticmethod
    def save_experiment(experiment):
        exp_dict = {'name': experiment.name, 'datetime': experiment.datetime,
                    'is_completed': experiment.is_completed, 'is_included': experiment.is_included}

        data = ExperimentDao.get_experiments_dict()
        experiments = []
        if len(data['experiments']) != 0:
            experiments = data['experiments']

        experiments.append(exp_dict)
        experiments_dict = {'experiments': experiments}
        data = json.dumps(experiments_dict)
        with open("DB/db/experiments.json", "w") as write_file:
            json.dump(data, write_file)

    @staticmethod
    def get_experiment(name):
        experiment = Experiment(name)
        data = ExperimentDao.get_experiments_dict()
        for e in data["experiments"]:
            if e['name'] == name:
                experiment.datetime = e['datetime']
                experiment.is_completed = e['is_completed']
                experiment.is_included = e['is_included']
            return experiment

        return None

    @staticmethod
    def update_experiment(experiment):
        ExperimentDao.delete_experiment(experiment.name)
        ExperimentDao.save_experiment(experiment)

    @staticmethod
    def delete_experiment(name):
        index = 0
        data = ExperimentDao.get_experiments_dict()
        for i in range(len(data["experiments"])):
            if data["experiments"][i]['name'] == name:
                index = i
        data["experiments"].pop(index)
        string = json.dumps(data)
        with open("DB/db/experiments.json", "w") as write_file:
            json.dump(string, write_file)







