from Common.LogProcess.Logger import Logger
from Common.FileProcess.AbstractClass import FileProcess
from surprise import Reader
from surprise import Dataset
class Data(FileProcess):
    def __init__(self, path):
        self.path = path
    def bulid(self, path):
        pass

    def delete(self, path):
        pass

    def read(self, line_format, sep = ','):
        '''

        :param line_format: 'user item rating'
        :param sep:
        :return:
        '''
        try:
            reader = Reader(line_format=line_format, sep=sep)
            return Dataset.load_from_file(self.path, reader = reader)
        except Exception as ex:
            Logger('error').get_log().error(ex)

    def operation(self):
        pass