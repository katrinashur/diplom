

class DataManager:

    @staticmethod
    def read_file_str(filename):
        lines = []
        f = open(filename, 'r')
        for line in f:
            lines.append(line)
        return lines

    @staticmethod
    def add_to_file(filename, dataset_str):
        if len(DataManager.read_file_str(filename)) == 0:
            DataManager.write_header(filename)

        f = open(filename, 'a')
        if not f.closed:
            for line in dataset_str:
                f.write(line)

    @staticmethod
    def read_file(filename):
        lines = []
        f = open(filename, 'r')
        if not f.closed:
            for line in f:
                lines.append(line.rstrip('\n'))
        return lines

    @staticmethod
    def write_dataset(filename, dataset):
        DataManager.write_header(filename)
        f = open(filename, 'a')

        if not f.closed:
            for line in dataset:
                string =''
                for el in line:
                    string += str(el) + '\t'
                f.write(string + '\n')
        f.close()

    @staticmethod
    def write_header(filename):
        channels = ("AF3", "F7", "F3", "FC5", "T7", "P7", "Pz", "O1", "O2", "P8", "T8", "FC6", "F4", "F8", "AF4")
        rhythms = ("theta", "alpha", "lowBeta", "highBeta", "gamma")
        emotions =('Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral')

        f = open(filename, 'w')

        if not f.closed:
            f.write('#\t')
            for channel in channels:
                for rhythm in rhythms:
                    f.write(channel + '_' + rhythm + '\t')
            f.write('time' + '\t')
            for emotion in emotions:
                f.write(emotion + '\t')
            f.write('time' + '\t' + '\n')

        f.close()





