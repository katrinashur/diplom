from datetime import datetime, timedelta


class Experiment:
    def __init__(self, name=datetime.now().strftime("%Y-%m-%d.%H_%M_%S.%f")):
        self.name = name
        self.datetime = datetime.now().strftime("%Y-%m-%d.%H_%M_%S.%f")
        self.is_included = 0
        self.is_completed = 0



