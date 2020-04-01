from Common.LogProcess.Logger import Logger
from surprise.model_selection import cross_validate
from Config.DatabaseConfig.ElasticSearch import elasticsearch_config
from Common.DatabaseProcess.ElasticSearch import ElasticSearch
from abc import ABCMeta, abstractmethod
from surprise import Dataset, Reader
import pandas as pd
'''
说明：
RMSE :均方根误差   MAE：平均绝对误差
数据要求：第一二三列严格按照用户，商品，分数来读取，根据文件不同，
选择不同的划分格式，如果是csv，则用','分隔符，如果是.data格式用’\t'分隔符，目前只支持这两种格式
返回：字典{'test_rmse':array, 'test_mae':array,...}
'''
class AbstractRS(metaclass=ABCMeta):
    #分折交叉验证
    def split(self, data, n_folds = 3):
        data.split(n_folds = 3)



    def evaluate(self, data, measures=['rmse', 'mae']):
        try:
            answer = cross_validate(self.algo, data, measures=measures)
            return answer
        except Exception as ex:
            # Logger('error').get_log().error(ex)
            return None






    # def getNeighbors(self, namelist: list, target, n):
    #     '''
    #     :param namelist: 所有用户的名称
    #     :param target: 目标用户标签
    #     :param n: 邻居个数
    #     :return:  邻居对象标签列表
    #     '''
    #     try:
    #         # 获取用户名到用户id 和 用户id到用户名的映射
    #         rid_to_name, name_to_rid = self.read_item_names(namelist)
    #         # Retieve inner id of the movie Toy Story
    #         toy_story_raw_id = name_to_rid[target]
    #         toy_story_inner_id = self.algo.trainset.to_inner_iid(toy_story_raw_id)
    #         # Retrieve inner ids of the nearest neighbors of Toy Story.
    #         toy_story_neighbors = self.algo.get_neighbors(toy_story_inner_id, k=n)
    #
    #         # Convert inner ids of the neighbors into names.
    #         toy_story_neighbors = (self.algo.trainset.to_raw_iid(inner_id)
    #                                for inner_id in toy_story_neighbors)
    #         toy_story_neighbors = (rid_to_name[rid]
    #                                for rid in toy_story_neighbors)
    #
    #         print('The' + n + ' nearest neighbors of ' + target + ' are:')
    #         for user in toy_story_neighbors: print(user)
    #         return toy_story_neighbors
    #     except Exception as ex:
    #         Logger('error').get_log().error(ex)



    def reader(self, line_format='user item rating', sep='\t'):
        try:
            #判断数据来源
            if self.source == 'File':
                self.read = Reader(line_format=line_format, sep=sep)
                self.data = Dataset.load_from_file(self.para, reader=self.read)
            elif self.source == 'ES':
                es = ElasticSearch(elasticsearch_config)
                # para = {"query": {"match_all": {}}}
                res = es._es.search(index="tb", body = self.para)
                data = {'itemID': [], 'userID': [], 'rating': []}
                jsons = res["hits"]["hits"]
                for item in jsons:
                    data['itemID'].append(item['_source']['item'])
                    data['userID'].append(item['_source']['user'])
                    data['rating'].append(item['_source']['score'])
                df = pd.DataFrame(data)
                self.read = Reader(rating_scale=(1, 5))
                self.data =  Dataset.load_from_df(df[['itemID', 'userID', 'rating']], self.read)
            else:
                return None
        except Exception as ex:
            Logger('error').get_log().error(ex)