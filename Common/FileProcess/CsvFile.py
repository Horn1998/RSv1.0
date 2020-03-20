from Common.FileProcess.AbstractClass import FileProcess
from Common.LogProcess.Logger import Logger
from surprise import Reader, Dataset
import sys
import csv
import os
class Csv(FileProcess):
    def __init__(self, path):
        self.path = path

    def bulid(self, path):
        pass

    def delete(self, path):
        pass

    def read(self):
        try:
            content = []
            with open(self.path, 'r', encoding='utf-8') as f:
                readlines =  csv.reader(f)
                for line in readlines:
                    content.append(line)
            return content
        except Exception as ex:
            Logger('error').get_log().error(ex)


    def write(self):
        pass


    def operation(self):
        pass


    # #用于将csv数据转为
    # def surpriseRead(self, line_format, sep = ','):
    #     '''
    #     :param line_format: 'user item rating' 此三项必不可少
    #     :param sep:
    #     :return:
    #     '''
    #     try:
    #         reader = Reader(line_format=line_format, sep=sep)
    #         return Dataset.load_from_file(self.path, reader = reader)
    #     except Exception as ex:
    #         Logger('error').get_log().error(ex)



if __name__ == '__main__':
    pass