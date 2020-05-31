

class DataManager:

    @staticmethod
    def read_file(filename):
        lines = []
        f = open(filename, 'r')
        for line in f:
            lines.append(line.rstrip('\n'))
        return lines

    @staticmethod
    def write_dataset(filename, dataset):
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

        for line in dataset:
            string =''
            for el in line:
                string += str(el) + '\t'
            f.write(string + '\n')
        f.close()
    #
    # @staticmethod
    # def list_to_str(l):
    #     for i in range(len(l)):
    #             l[i] = '\t'.join(l[i])
    #     return l

    # @staticmethod
    # def get_depth(l):
    #     if isinstance(l, (list, tuple)):
    #         t = ()
    #         for itm in l:
    #             t += get_depth(itm),
    #         return 1 + max(t)
    #     return 0
    #
    # @staticmethod
    # def how_deep(x):
    #     if x and isinstance(x, (list, tuple)):
    #         return 1 + max(how_deep(i) for i in x)
    #     return 0
    #
    # @staticmethod
    # def list_to_str(x):
    #     for i in x:
    #         if  isinstance(x[i], (list, tuple):
    #             a = 1
    #             for j in range(len(x[j])):
    #                 a *= isinstance(x[j])



