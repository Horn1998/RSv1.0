from Recommand.说明文档.back.BaselineAlgorithms.AbstractRS import AbstractRS
from surprise import NormalPredictor, BaselineOnly


class NormalPredictorRS(AbstractRS):
    def __init__(self, params={'name': 'pearson_baseline', 'user_based': True}):
            self.algo = NormalPredictor(params)



class BaselineOnlyRS(AbstractRS):
    def __init__(self, params={'name': 'pearson_baseline', 'user_based': True}):
            self.algo = BaselineOnly(params)
