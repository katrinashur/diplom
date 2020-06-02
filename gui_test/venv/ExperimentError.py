import enum


class ExperimentError(enum.Enum):
    OK = 0
    NO_BRAIN_WAVES = 1
    NO_FACE = 2
    NO_CONNECTION_TO_CAMERA = 3
    NO_CONNECTION_TO_EPOC = 4
    INCORRECT_DB = 5
    LOST_CONNECTION_RECORD = 6
    EXISTING_NAME = 7
