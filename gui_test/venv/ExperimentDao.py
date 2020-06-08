import json
from Experiment import Experiment


class ExperimentDao:
    __path_db = ''

    def __init__(self):
        self.__path_db = "DB\\db\\experiments.json"

    def get_experiments_obj(self):
        experiments = []
        #print (self.__path_db)
        with open(self.__path_db, "r") as json_file:
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

    def get_experiments_dict(self):
        with open(self.__path_db) as json_file:
            string = json.load(json_file)
        return json.loads(string)

    def save_experiment(self, experiment):
        exp_dict = {'name': experiment.name, 'datetime': experiment.datetime,
                    'is_completed': experiment.is_completed, 'is_included': experiment.is_included}

        data = self.get_experiments_dict()
        experiments = []
        if len(data['experiments']) != 0:
            experiments = data['experiments']

        experiments.append(exp_dict)
        experiments_dict = {'experiments': experiments}
        data = json.dumps(experiments_dict)
        with open(self.__path_db, "w") as write_file:
            json.dump(data, write_file)

    def get_experiment(self, name):
        experiment = Experiment(name)
        data = self.get_experiments_dict()
        for e in data["experiments"]:
            if e['name'] == name:
                experiment.datetime = e['datetime']
                experiment.is_completed = e['is_completed']
                experiment.is_included = e['is_included']
                return experiment

        return None

    def update_experiment(self, experiment):
        self.delete_experiment(experiment.name)
        self.save_experiment(experiment)

    def delete_experiment(self, name):
        index = 0
        data = self.get_experiments_dict()
        for i in range(len(data["experiments"])):
            if data["experiments"][i]['name'] == name:
                index = i
        data["experiments"].pop(index)
        string = json.dumps(data)
        with open(self.__path_db, "w") as write_file:
            json.dump(string, write_file)







