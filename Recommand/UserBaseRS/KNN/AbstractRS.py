from Common.LogProcess.Logger import Logger
from surprise.model_selection import cross_validate

from abc import ABCMeta, abstractmethod
from surprise import Dataset, Reader
'''
说明：
RMSE :均方根误差   MAE：平均绝对误差
数据要求：第一二三列严格按照用户，商品，分数来读取，根据文件不同，
选择不同的划分格式，如果是csv，则用','分隔符，如果是.data格式用’\t'分隔符，目前只支持这两种格式
返回：字典{'test_rmse':array, 'test_mae':array,...}
'''
class AbstractRS(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, path): pass
        # self.path = path        #数据路径
        # self.algo = algo        #推荐算法



    #分折交叉验证
    def split(self, data, n_folds = 5):
        data.split(n_folds = 5)



    def evaluate(self, data, measures=['rmse', 'mae']):
        try:
            answer = cross_validate(self.algo, data, measures=measures)
            return answer
        except Exception as ex:
            Logger('error').get_log().error(ex)



    def adapter(self, sep, name_list):
        id, rid_to_name, name_to_rid = 0, {}, {}
        for name in name_list:
            if name not in name_to_rid.keys():
                id += 1
                name_to_rid[name] = id
        for key, val in name_to_rid.items():
            rid_to_name[val] = key
        return rid_to_name, name_to_rid



    def getNeighbors(self, namelist: list, target, n):
        '''
        :param namelist: 所有用户的名称
        :param target: 目标用户标签
        :param n: 邻居个数
        :return:  邻居对象标签列表
        '''
        try:
            # 获取用户名到用户id 和 用户id到用户名的映射
            rid_to_name, name_to_rid = self.read_item_names(namelist)
            # Retieve inner id of the movie Toy Story
            toy_story_raw_id = name_to_rid[target]
            toy_story_inner_id = self.algo.trainset.to_inner_iid(toy_story_raw_id)
            # Retrieve inner ids of the nearest neighbors of Toy Story.
            toy_story_neighbors = self.algo.get_neighbors(toy_story_inner_id, k=n)

            # Convert inner ids of the neighbors into names.
            toy_story_neighbors = (self.algo.trainset.to_raw_iid(inner_id)
                                   for inner_id in toy_story_neighbors)
            toy_story_neighbors = (rid_to_name[rid]
                                   for rid in toy_story_neighbors)

            print('The' + n + ' nearest neighbors of ' + target + ' are:')
            for user in toy_story_neighbors: print(user)
            return toy_story_neighbors
        except Exception as ex:
            Logger('error').get_log().error(ex)



    def reader(self, line_format='user item rating', sep='\t'):
        try:
            self.reader = Reader(line_format=line_format, sep=sep)
            return Dataset.load_from_file(self.path, reader=self.reader)
        except Exception as ex:
            Logger('error').get_log().error(ex)