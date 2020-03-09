class TSPReader:
    @staticmethod
    def read(path):
        f = open(path, 'r')
        x = f.readlines()
        f.close()
        return x[6:-1]
