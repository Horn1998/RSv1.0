from surprise import SVD, SVDpp, NMF
from Recommand.ModelBaseRS.AbstractRS import AbstractRS
from Common.LogProcess.Logger import Logger
import os
class SVDRS(AbstractRS):
    def __init__(self):
        super.__init__()
        self.algo = SVD()




    def train(self):
        try:
            trainset = self.data.build_full_trainset()
            self.algo.fit(trainset)
        except Exception as ex:
            Logger('error').get_log().error(ex)



class NMFRS(AbstractRS):
    def __init__(self):

        self.algo = NMF()






class SVDppRS(AbstractRS):
    def __init__(self):
        self.algo = SVDpp()


    # #构建模型
    # def train(self):
    #     trainset = self.data.build_full_trainset()
    #     self.algo.fit(trainset)
