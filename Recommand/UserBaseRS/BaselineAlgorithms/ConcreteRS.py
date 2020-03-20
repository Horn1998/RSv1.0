from Recommand.UserBaseRS.BaselineAlgorithms.AbstractRS import AbstractRS
from surprise import NormalPredictor, BaselineOnly
import os
class NormalPredictorRS(AbstractRS):
    def __init__(self, path):
        self.path = os.path.expanduser(path)
        self.algo = NormalPredictor()



class BaselineOnlyRS(AbstractRS):
    def __init__(self, path):
        self.path = os.path.expanduser(path)
        self.algo = BaselineOnly()