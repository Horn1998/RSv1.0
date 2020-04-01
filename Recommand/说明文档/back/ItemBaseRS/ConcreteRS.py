from Recommand.CommonRS.AbstractRS import AbstractRS
from surprise import KNNBaseline, KNNBasic


class KNNBaselineRS(AbstractRS):
    def __init__(self,  sim_options={'name': 'pearson_baseline', 'user_based': False}):
        self.algo = KNNBaseline(sim_options = sim_options)

    def train(self):
        self.data.build_full_trainset()
        self.algo = KNNBaseline()
        self.algo.fit(self.data)

        # 给用户提供序号，适配getNeighbors函数


class KNNBasicRS(AbstractRS):
    def __init__(self,  sim_options={'name': 'pearson_baseline', 'user_based': False}):
        self.algo = KNNBasic(sim_options = sim_options)
