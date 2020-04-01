from Recommand.CommonRS.ConcreteRS import KNNBasicRS, KNNBaselineRS, BaselineOnlyRS, NormalPredictorRS
from Recommand.ModelBaseRS.ConcreteRS import SVDppRS, SVDRS, NMFRS
from Common.DatabaseProcess.ElasticSearch import ElasticSearch
from Config.DatabaseConfig.ElasticSearch import elasticsearch_config
from Common.LogProcess.Logger import Logger
from Recommand.RecommendSystem import RSTool
from Config.BasePath import indexpath
from surprise import accuracy
import numpy as np
import traceback
import datetime
import pickle
import os
#最多同时运行四个模型
class Generator(RSTool):
    def __init__(self, config):
        """
        :param config:
        """
        self.config = config
        self.models = None
        self.rid_to_name, self.name_to_rid = {}, {}


    #获得目标系统集合
    def getRS(self):
        """
        config = {"path": D:/Restart_RA/", "source":"file", "type":"KNN", "store":"tb","module":true, "module_name":,"params":...}
        path:数据路径(str) or ES查询体(json)
        source: 数据来源.data文件 or ES
        type:根据训练时间长短选择相应推荐系统
        store:商家id
        module:是否拥有模型

        :return:
        """
        try:
            print('获取推荐系统')
            #目前只针对KNN设计推荐算法，其他的待补充
            if self.config['type'] == 'KNN':
                #para:文件路径， source:文件来源 source='ES', para={"query": {"match_all": {}}}
                self.models = [KNNBaselineRS, KNNBasicRS]
            elif self.config['type'] == 'BaselineAlgorithms':
                self.models = [BaselineOnlyRS, NormalPredictorRS]
            elif self.config['type'] == 'MatrixFactorization':
                self.models = [SVDRS, SVDppRS, NMFRS]


        except Exception as ex:
            Logger('error').get_log().error(ex)



    def getReader(self):
        try:
            print('run start', datetime.datetime.now())
            self.result = {}
            print('筛选推荐系统')
            if self.config['source'] == 'normal': self.reader = self.normalReader
            #读取某个商家某一类型数据
            elif self.config['source'] == 'ES': self.reader = self.jsonReader
        except Exception as ex:
            traceback.print_exc()
            Logger('error').get_log().error(ex)



    #获取基于商品模型所需要的数据
    def userData(self, store):
        try:
            body = {"query": {"bool": {
                "must":[
                    {
                        "term":{
                            "store": store
                        },
                    }
                ]
            }}}
            data = self.reader(store, body)
            if not data: return None
            print('读取数据完毕')
            return data
        except Exception as ex:
            Logger('error').get_log().error(ex)



    #获取基于用户模型所需要的数据
    def itemData(self, store, type):
        try:
            body = {"query": {"bool": {
                "must":[
                    {
                        "term":{
                            "store": store
                        },
                        "term":{
                            "itemtype": type
                        }
                    }
                ]
            }}}
            data = self.reader(store, body)
            if not data: return None
            print('读取数据完毕')
            return data
        except Exception as ex:
            Logger('error').get_log().error(ex)




    #训练最佳基于商品模型
    def itemtrain(self, store, type, data):
        """
        :param index:  商户名称
        :param type: 商品类型
        :return:
        """
        try:
            #如果模型已经存在则直接使用模型训练
            path = indexpath + '/' + store + '/item-' + type + '.pickle'
            if os.path.exists(path):
                modelClass = self.get_model(store, type, target='item')
                newClass = self.train(modelClass, data)
                self.save_model(newClass, store, type, 'item')
                return

            #如果模型不存在则训练模型
            for num, model in enumerate(self.models[:4]):
                print('模型' + str(model) + '评估')
                params = {'name': 'pearson_baseline', 'user_based': False }
                model = model(params = params)
                ans = model.evaluate(data)
                if ans: self.result[num] = ans
                else: continue
            MaxRMSE, MaxMAE, index = 0, 0, 0
            for key, res in self.result.items():
                # res = res.get()
                if res and 'test_rmse' in res.keys() and res['test_rmse'].tolist():
                    if np.mean(res['test_rmse'].tolist()) > MaxRMSE: index = key
                elif res and 'test_mae' in res.keys() and res['test_mae'].tolist():
                    if np.mean(res['test_mse'].tolist()) > MaxMAE: index = key
                else:
                    index = -1
            if index == -1:
                print('数据量不够，模型训练失败')
                return
            print('模型评估完毕, 最终选择' + str(index) + '号模型')
            print('run finish', datetime.datetime.now())
            model = self.models[index](params = params)
            return self.train(model, data)
        except Exception as ex:
            Logger('error').get_log().error(ex)
            return




    #训练最佳基于用户模型
    def usertrain(self, data):
        """
        :param index:  商户名称
        :param type: 商品类型
        :return:
        """
        try:

            for num, model in enumerate(self.models[:4]):
                print('模型' + str(model) + '评估')
                params = {'name': 'pearson_baseline', 'user_based': True}
                model = model(params=params)
                ans = model.evaluate(data)
                if ans:
                    self.result[num] = ans
                else:
                    continue
            MaxRMSE, MaxMAE, index = 0, 0, 0
            for key, res in self.result.items():
                # res = res.get()
                if res and 'test_rmse' in res.keys() and res['test_rmse'].tolist():
                    if np.mean(res['test_rmse'].tolist()) > MaxRMSE: index = key
                elif res and 'test_mae' in res.keys() and res['test_mae'].tolist():
                    if np.mean(res['test_mse'].tolist()) > MaxMAE: index = key
                else:
                    index = -1
            if index == -1:
                print('数据量不够，模型训练失败')
                return
            print('模型评估完毕, 最终选择' + str(index) + '号模型')
            print('run finish', datetime.datetime.now())
            model = self.models[index](params = params)

            # 用已有数据进行模型训练
            trainset = data.build_full_trainset()
            model.fit(data = trainset)

            print('----------------------------------test-------------------------------------------')
            testset = trainset.build_testset()
            predictions = model.algo.test(testset)

            accuracy.rmse(predictions, verbose=True)  # ~ 0.9979 (which is low)
            print('-----------------------------------end--------------------------------------------')
            return model
        except Exception as ex:
            Logger('error').get_log().error(ex)
            return




    #使用数据训练模型
    def train(self, model, data):
        try:
            # 用已有数据进行模型训练
            trainset = data.build_full_trainset()
            model.fit(data=trainset)

            print('----------------------------------test-------------------------------------------')
            testset = trainset.build_testset()
            predictions = model.algo.test(testset)

            accuracy.rmse(predictions, verbose=True)  # ~ 0.9979 (which is low)
            print('-----------------------------------end--------------------------------------------')
            # 保存模型到store文件夹下的type.pickle文件中
            # self.save_model(model=model, store=store.split('-')[1], type=type, toward='item')
            return model
        except Exception as es:
            Logger('error').get_log().error(es)



    #最终执行函数
    def execute(self):
        try:
            es = ElasticSearch(elasticsearch_config)
            # 获取所有索引
            indexes = []
            for dirs in os.listdir(indexpath):
                # predict-store 训练
                indexes.append('predict-' + dirs)
            self.getRS()
            self.getReader()
            stores = {}
            for index in indexes:
                store = index.split('-')[1]
                body = {
                    "query":{
                        "term":{
                            "store":store
                        }
                    }
                }
                jsons = es.search(index = index, body=body)
                if jsons: types = jsons["hits"]["hits"]
                for type in types:
                    stores.setdefault(index, [])
                    if type["_source"]["itemtype"] not in stores[index]: stores[index].append(type["_source"]["itemtype"])        #获取某个商场下的商品类型
            for store, types in stores.items():
                userdata = self.userData(store)
                user_model = self.usertrain(userdata)
                self.save_model(model=user_model, store=store.split('-')[1], type=type, toward='user')
                for type in types:
                    #训练模型并保存到制定路径
                    itemdata = self.itemData(store, type)
                    item_model = self.itemtrain(itemdata)
                    # 保存模型到store文件夹下的type.pickle文件中
                    self.save_model(model=item_model, store=store.split('-')[1], type=type, toward='item')


        except Exception as ex:
            traceback.print_exc()
            Logger('error').get_log().error(ex)



if __name__ == '__main__':
    generator = Generator(config={'type': 'KNN', 'source':'ES', 'way': {"query": {"match_all": {}}}} )
    generator.execute()
    # es = ElasticSearch(elasticsearch_config)
    # es.drop(index='predict-jingdong')


