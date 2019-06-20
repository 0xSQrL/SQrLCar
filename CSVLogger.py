import time
from os import path


class CSVLogger:

    def __init__(self, headers=[], filepath=''):
        self.file = open(path.join(filepath, "data_{0:.0f}.csv".format(time.time(), filepath)), 'w+')
        for header in headers:
            self.file.write("{},".format(header))
        self.file.write('\n')

    def log_data(self, data=[]):
        for header in data:
            self.file.write("{},".format(header))
        self.file.write('\n')

    def dispose(self):
        self.file.close()
