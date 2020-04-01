from Recommand.CommonRS.AbstractRS import AbstractRS
from surprise import KNNBaseline, KNNBasic
from surprise import BaselineOnly

class KNNBaselineRS(AbstractRS):
    def __init__(self,  params = {'name': 'pearson_baseline', 'user_based': True}):
        print('KNNBaseline initial')
        self.algo = KNNBaseline(sim_options = params)

    def fit(self, data):
        return self.algo.fit(data)


class KNNBasicRS(AbstractRS):
    def __init__(self,  params = {'name': 'pearson_baseline', 'user_based': True}):
        print('KNNBasic initial')
        self.algo = KNNBasic(sim_options = params)

    def fit(self, data):
        return self.algo.fit(data)



class NormalPredictorRS(AbstractRS):
    def __init__(self, params={'name': 'pearson_baseline', 'user_based': True}):
        print('NormalPredictor initial')
        self.algo = NormalPredictor(params)




class BaselineOnlyRS(AbstractRS):
    def __init__(self, params={'name': 'pearson_baseline', 'user_based': True}):
        print('BaselineOnly initial')
        self.algo = BaselineOnly(params)




if __name__ == '__main__':
    from surprise import NormalPredictor

    KNN = KNNBaselineRS(source='ES', para={"query": {"match_all": {}}})
    KNN.reader()
    answer = KNN.evaluate()
    print(answer)
