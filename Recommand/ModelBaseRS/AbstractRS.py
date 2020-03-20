from Common.LogProcess.Logger import Logger
from surprise.model_selection import cross_validate
from sklearn.model_selection import GridSearchCV
from abc import ABCMeta, abstractmethod
from surprise import Dataset, Reader
from surprise import PredictionImpossible
import os, io
'''
说明：
RMSE :均方根误差   MAE：平均绝对误差
数据要求：第一二三列严格按照用户，商品，分数来读取，根据文件不同，
选择不同的划分格式，如果是csv，则用','分隔符，如果是.data格式用’\t'分隔符，目前只支持这两种格式
返回：字典{'test_rmse':array, 'test_mae':array,...}
'''
class AbstractRS(metaclass=ABCMeta):
    def __init__(self, path):
        self.path = path
        self.reader = None
        self.data = None
        self.rid_to_name, self.name_to_rid = {}, {}



    #分折交叉验证
    def split(self, data, n_folds = 5):
        return data.split(n_folds = n_folds)



    def evaluate(self, data, measures = ['rmse', 'mae']):
        try:
            print('-----------------' + str(self.algo) + '-----------------------')
            return cross_validate(self.algo, data, measures=measures)
        except Exception as ex:
            Logger('error').get_log().error(ex)
            Logger('error').clear()









    def train(self):
        try:
            trainset = self.data.build_full_trainset()
            self.algo.fit(trainset)
        except Exception as ex:
            Logger('error').get_log().error(ex)



    def reader(self, line_format='user item rating', sep=','):
        try:
            self.reader = Reader(line_format=line_format, sep=sep)
            self.data = Dataset.load_from_file(self.path, reader=self.reader)
            self.rid_to_name, self.name_to_rid = self.read_item_names(sep)
        except Exception as ex:
            Logger('error').get_log().error(ex)






if __name__ == '__main__':
    rid_to_name = {}
    name_to_rid = {}
    with io.open(r'D:\Restart_RA\测试样例\测试数据\u.data', 'r', encoding='utf-8') as f:
        for line in f:
            line = line.split('\t')
            rid_to_name[line[0]] = line[1]
            name_to_rid[line[1]] = line[0]
            print(line)


