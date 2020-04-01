from Common.DatabaseProcess.ElasticSearch import ElasticSearch
from Config.DatabaseConfig.ElasticSearch import elasticsearch_config
from Recommand.RecommendSystem import RSTool
from Common.LogProcess.Logger import Logger
from Config.BasePath import basepath, indexpath
from surprise import PredictionImpossible
import pickle
import io


class Predictor(RSTool):
    def __init__(self, config):
        #config {store:?, itemtype:?, target:?}
        self.target = config['target']
        self.rid_to_name = {}
        self.name_to_rid = {}
        self.store = config['store']
        self.type = config['itemtype']
        self.user_based = config['user_based']

    # 找到同类target
    def predict(self, k=4):
        '''
        :param k: 相似对象数
        :return: 相似对象标签
        '''
        try:

            raw_id = self.name_to_rid[self.target]
            inner_id = self.algo.trainset.to_inner_iid(raw_id)
            neighbors = self.algo.get_neighbors(inner_id, k=k)
            neighbors = (self.algo.trainset.to_raw_iid(inner_id) for inner_id in neighbors)
            neighbors = (self.rid_to_name[rid] for rid in neighbors)
            return [item  for item in neighbors]
            # return neighbors if len(neighbors) < 10 else neighbors[:10]
        except PredictionImpossible as pl:
            Logger('error').get_log().error(pl)
        except Exception as ex:
            Logger('error').get_log().error(ex)

        # 找到同类target
        def itemPredict(self, k=4):
            '''
            :param k: 相似对象数
            :return: 相似对象标签
            '''
            try:

                raw_id = self.name_to_rid[self.target]
                inner_id = self.algo.trainset.to_inner_iid(raw_id)
                neighbors = self.algo.get_neighbors(inner_id, k=k)
                neighbors = (self.algo.trainset.to_raw_iid(inner_id) for inner_id in neighbors)
                neighbors = (self.rid_to_name[rid] for rid in neighbors)
                return [item for item in neighbors]
                # return neighbors if len(neighbors) < 10 else neighbors[:10]
            except PredictionImpossible as pl:
                Logger('error').get_log().error(pl)
            except Exception as ex:
                Logger('error').get_log().error(ex)



    def read_item_names(self):
        """
        获取电影名到电影id 和 电影id到电影名的映射
        """
        es = ElasticSearch(elasticsearch_config)

        body = {
            "query":{
                "bool": {
                "must": [
                    {
                    "term": {
                        "store": self.store
                    },
                    "term": {
                        "itemtype": self.type
                    }
                    }
                ]
            }
            }
        }
        jsons = es.search(index='predict-' + self.store, body=body)
        if jsons: types = jsons["hits"]["hits"]
        for type in types:
            id = type["_source"]["itemid"]
            name = type["_source"]["item"]
            self.rid_to_name[id] = name
            self.name_to_rid[name] = id



    def read_user_names(self):
        """
        获取电影名到电影id 和 电影id到电影名的映射
        """
        es = ElasticSearch(elasticsearch_config)

        body = {
            "query":{
                "bool": {
                "must": [
                    {
                    "term": {
                        "store": self.store
                    },
                    "term": {
                        "itemtype": self.type
                    }
                    }
                ]
            }
            }
        }
        jsons = es.search(index='predict-' + self.store, body=body)
        if jsons: types = jsons["hits"]["hits"]
        for type in types:
            id = type["_source"]["userid"]
            name = type["_source"]["user"]
            self.rid_to_name[id] = name
            self.name_to_rid[name] = id



    # 获取模型
    def get_model(self, store, type, target = 'item'):
        try:
            with open(indexpath + '/' + store + '/' + target + '-'+ type + '.pickle', 'rb') as p:
                return pickle.load(p)
        except Exception as ex:
            Logger('error').get_log().error(ex)
            return None




    def run(self, k=4):
        #基于用户推荐，一般在无搜索状态下用到
        if self.user_based:
            self.algo = self.get_model(store = self.store, type =self.type, target='user').algo
            self.read_user_names()
        #基于商品推荐，一般在搜索状态下
        else:
            self.algo = self.get_model(store=self.store, type=self.type, target='item').algo
            self.read_item_names()
        #模型没有训练完成
        if not self.algo: return []
        return self.predict(k=k)


if __name__ == '__main__':
    predictor = Predictor({'store':'jingdong', 'itemtype': '1', 'target': '116', 'user_based': True})
    ans = predictor.run()
    print(ans)