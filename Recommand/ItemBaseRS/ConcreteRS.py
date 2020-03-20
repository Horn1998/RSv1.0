from Recommand.UserBaseRS.KNN.AbstractRS import AbstractRS
from Common.LogProcess.Logger import Logger
from surprise import KNNBaseline, KNNBasic
import os
class KNNBaselineRS(AbstractRS):
    def __init__(self, path, sim_options={'name': 'pearson_baseline', 'user_based': False}):
        self.path = os.path.expanduser(path)
        self.algo = KNNBaseline(sim_options = sim_options)

    def train(self):
        self.data.build_full_trainset()
        self.algo = KNNBaseline()
        self.algo.fit(self.data)

        # 给用户提供序号，适配getNeighbors函数


class KNNBasicRS(AbstractRS):
    def __init__(self, path, sim_options={'name': 'pearson_baseline', 'user_based': False}):
        self.path = os.path.expanduser(path)
        self.algo = KNNBasic(sim_options = sim_options)
