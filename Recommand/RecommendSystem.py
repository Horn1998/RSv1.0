from Common.DatabaseProcess.ElasticSearch import ElasticSearch
from Config.DatabaseConfig.ElasticSearch import elasticsearch_config
from Config.BasePath import indexpath
from abc import ABCMeta, abstractmethod
from Common.LogProcess.Logger import Logger
from Common.FileProcess.JsonFile import Json
from surprise import Reader, Dataset
import pickle
import os
class RSTool(metaclass=ABCMeta):
    #支持.csv .data文件
    def normalReader(self, line_format='user item rating', sep=',', *args):
        try:
            self.reader = Reader(line_format=line_format, sep=sep)
            return Dataset.load_from_file(self.config['path'], reader=self.reader)
        except Exception as ex:
            Logger('error').get_log().error(ex)
            Logger('error').clear()


    #支持.json文件
    def jsonReader(self,  *args):
        '''
        :param
        args[0]: index
        args[2]: 查询体
        :return:
        '''
        try:
            body = args[1]
            es = ElasticSearch(elasticsearch_config)
            res = es.search(index=args[0],  body=body)
            data = {'itemID': [], 'userID': [], 'rating': []}
            jsons = res["hits"]["hits"]
            if not jsons: return None
            #获取测试数据 itemID userID rating
            for item in jsons:
                # if itemtype not in itemtypes: itemtypes.append(itemtype)
                # itemtype = item['_source']['itemtype']
                # data.setdefault(itemtype, {'itemID': [], 'userID': [], 'rating': []})
                data['itemID'].append(item['_source']['item'])
                data['userID'].append(item['_source']['user'])
                data['rating'].append(item['_source']['score'])
            # for itemtype in itemtypes:
            df = pd.DataFrame(data)
            reader = Reader(rating_scale=(1, 5))
            # 传入的列必须对应着 userID，itemID 和 rating（严格按此顺序）。
            data = Dataset.load_from_df(df[['itemID', 'userID', 'rating']], reader)
            return data
        except Exception as ex:
            Logger('error').get_log().error(ex)




    # 获取模型
    def get_model(self, store, type, target = 'item'):
        try:
            with open(indexpath + '/' + store + '/' + target + '-'+ type + '.pickle', 'rb') as p:
                return pickle.load(p)
        except Exception as ex:
            Logger('error').get_log().error(ex)
            return None



    #储存训练好的模型
    def save_model(self, model, store, type, toward):
        try:
            if not os.path.exists(indexpath):
                os.makedirs(indexpath)
            if not os.path.exists(indexpath + '/' + str(store)):
                os.makedirs(indexpath + '/' + str(store))
            #path = indexpath/jingdong/user-1.pickle
            path = indexpath + '/' + str(store) + '/' + toward + '-' + type  + '.pickle'
            with open(path, 'wb') as p:
                pickle.dump(model, p)
                print(path + "文件创建成功")
        except Exception as ex:
            Logger('error').get_log().error(ex)










if __name__ == '__main__':
    import pandas as pd

    from surprise import NormalPredictor
    from surprise import Dataset
    from surprise import Reader
    from surprise.model_selection import cross_validate

    # 建立 DataFrame 结构。 列名是互不相关的。
    ratings_dict = {'itemID': [1, 1, 1, 2, 2],
                    'userID': [9, 32, 2, 45, 'user_foo'],
                    'rating': [3, 2, 4, 3, 1]}
    df = pd.DataFrame(ratings_dict)

    # 同样需要定义 Reader 对象，但只需指定 rating_scale 参数。
    reader = Reader(rating_scale=(1, 5))

    # 传入的列必须对应着 userID，itemID 和 rating（严格按此顺序）。
    data = Dataset.load_from_df(df[['userID', 'itemID', 'rating']], reader)

    # 然后即可根据需要来操作此数据集，例如调用cross_validate
    ans = cross_validate(NormalPredictor(), data, cv=2)
    print(ans.get())