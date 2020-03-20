from Recommand.RecommendSystem import RSTool
from Common.LogProcess.Logger import Logger
from surprise import PredictionImpossible
class Predictor(RSTool):
    def __init__(self, config):
        self.algo = self.get_model(userid= config['user'], option= config['option'])
        self.target = config['target']


    # 找到同类target
    def predict(self,  k = 4):
        '''
        :param user: 类比对象
        :param userid:用来确定预测系统
        :param k: 相似对象数
        :return: 相似对象标签
        '''
        try:
            raw_id = self.name_to_rid[self.target]
            inner_id = self.algo.trainset.to_inner_iid(raw_id)
            neighbors = self.algo.get_neighbors(inner_id, k=k)
            neighbors = (self.algo.trainset.to_raw_iid(inner_id) for inner_id in neighbors)
            neighbors = (self.rid_to_name[rid] for rid in neighbors)
            return neighbors if len(neighbors) < 10 else neighbors[:10]
        except PredictionImpossible as pl:
            Logger('error').get_log().error(pl)
        except Exception as ex:
            Logger('error').get_log().error(ex)



    def run(self, k = 4):
        self.predict(k = k)
