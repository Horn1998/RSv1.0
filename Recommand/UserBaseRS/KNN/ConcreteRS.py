from Recommand.UserBaseRS.KNN.AbstractRS import AbstractRS
from Common.LogProcess.Logger import Logger
from surprise import KNNBaseline, KNNBasic
import os
class KNNBaselineRS(AbstractRS):
    def __init__(self, path, sim_options={'name': 'pearson_baseline', 'user_based': True}):
        print('KNNBaseline initial')
        self.path = path
        self.algo = KNNBaseline(sim_options = sim_options)




class KNNBasicRS(AbstractRS):
    def __init__(self, path, sim_options={'name': 'pearson_baseline', 'user_based': True}):
        print('KNNBasic initial')
        self.path = path
        self.algo = KNNBasic(sim_options = sim_options)




if __name__ == '__main__':
    Object = KNNBasicRS(r'D:\Restart_RA\Recommand\UserBaseRS\测试数据\u.data')
    data = Object.reader()
    Object.evaluate(data)