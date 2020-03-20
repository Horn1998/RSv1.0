from Recommand.UserBaseRS.BaselineAlgorithms.ConcreteRS import BaselineOnlyRS, NormalPredictorRS
from Recommand.ModelBaseRS.ConcreteRS import SVDppRS, SVDRS, NMFRS
from Recommand.UserBaseRS.KNN.ConcreteRS import KNNBasicRS, KNNBaselineRS
from Common.LogProcess.Logger import Logger
from Config.ChildSystemConfig.RecommandCS import RSConfig
from Recommand.RecommendSystem import RSTool
from surprise import PredictionImpossible
import multiprocessing
import datetime
import numpy as np
#最多同时运行四个模型
class Generator(RSTool):


    def __init__(self, config):
        self.config = config
        self.models = []
        self.rid_to_name, self.name_to_rid = {}, {}


    #获得目标系统集合
    def getRS(self):
        try:
            print('获取推荐系统')
            path = self.config['path']
            if self.config['type'] == 'KNN':
                self.models = [KNNBaselineRS(path), KNNBasicRS(path)]
            elif self.config['type'] == 'BaselineAlgorithms':
                self.models = [BaselineOnlyRS(path), NormalPredictorRS(path)]
            elif self.config['type'] == 'MatrixFactorization':
                self.models = [SVDRS(path), SVDppRS(path), NMFRS(path)]


        except Exception as ex:
            Logger('error').get_log().error(ex)
            Logger().clear()



    #筛选最佳系统
    def filter(self):
        try:
            print('run start', datetime.datetime.now())
            self.result, self.data = {}, {}
            print('筛选推荐系统')
            if self.config['reader'] == 'normal':  self.reader = self.normalReader
            elif self.config['reader'] == 'json': self.reader = self.jsonReader
            pool = multiprocessing.Pool(processes= 4)
            for index, model in enumerate(self.models[:4]):
                print('model' + str(index) + '读取数据')
                self.data[index] = pool.apply(self.reader, (self.config['line_format'], self.config['sep']))
            pool.close()
            pool.join()
            print('读取数据完毕')
            pool = multiprocessing.Pool(processes= min(4, len(self.models)))
            for index, model in enumerate(self.models[:4]):
                print('模型' + str(model) + '评估')
                self.result[index] = pool.apply_async(model.evaluate, (self.data[index], ['rmse', 'mae'] ))
            pool.close()
            pool.join()
            MaxRMSE, MaxMAE, index = 0, 0, 0
            for key, res in self.result.items():
                res= res.get()
                print(res)
                if 'test_rmse' in res.keys() and res['test_rmse'].tolist():
                    if np.mean(res['test_rmse'].tolist()) > MaxRMSE: index = key
                elif 'test_mae' in res.keys() and res['test_mae'].tolist():
                    if np.mean(res['test_mse'].tolist()) > MaxMAE: index = key
                else: index = 0
            print('模型评估完毕, 最终选择' + str(index) + '号模型')
            print('run finish', datetime.datetime.now())
            return self.models[index]
        except Exception as ex:
            Logger('error').get_log().error(ex)
            return None



    #效率对比
    def contrast(self):
        print('contrast start', datetime.datetime.now())
        for model in self.models:
            model.evaluate(self.data)
        print('contrast end', datetime.datetime.now())



    def run(self):
        try:
            self.getRS()
            self.filter()
        except Exception as ex:
            Logger('error').get_log().error(ex)



if __name__ == '__main__':
    filter = Generator(RSConfig)
    filter.getRS()
    filter.filter()
