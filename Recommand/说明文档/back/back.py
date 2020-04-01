# from Recommand.UserBaseRS.BaselineAlgorithms.ConcreteRS import BaselineOnlyRS, NormalPredictorRS
# from Recommand.ModelBaseRS.ConcreteRS import SVDppRS, SVDRS, NMFRS
# from Recommand.UserBaseRS.KNN.ConcreteRS import KNNBasicRS, KNNBaselineRS
# from Common.DatabaseProcess.ElasticSearch import ElasticSearch
# from Config.DatabaseConfig.ElasticSearch import elasticsearch_config
# from Config.BasePath import basepath, indexpath
# from Common.LogProcess.Logger import Logger
# from Recommand.RecommendSystem import RSTool
# import traceback
# from surprise import accuracy
# import multiprocessing
# import datetime
# import numpy as np
# import pickle
# import os
#
#
# # 最多同时运行四个模型
# class Generator(RSTool):
#     def __init__(self, config):
#         """
#
#         :param config:
#         """
#         self.config = config
#         self.models = None
#         self.rid_to_name, self.name_to_rid = {}, {}
#
#     # 获得目标系统集合
#     def getRS(self):
#         """
#         config = {"path": D:/Restart_RA/", "source":"file", "type":"KNN", "store":"tb","module":true, "module_name":,"params":...}
#         path:数据路径(str) or ES查询体(json)
#         source: 数据来源.data文件 or ES
#         type:根据训练时间长短选择相应推荐系统
#         store:商家id
#         module:是否拥有模型
#
#         :return:
#         """
#         try:
#             print('获取推荐系统')
#             if self.config['type'] == 'KNN':
#                 # para:文件路径， source:文件来源 source='ES', para={"query": {"match_all": {}}}
#                 self.models = [KNNBaselineRS, KNNBasicRS]
#             elif self.config['type'] == 'BaselineAlgorithms':
#                 self.models = [BaselineOnlyRS(), NormalPredictorRS()]
#             elif self.config['type'] == 'MatrixFactorization':
#                 self.models = [SVDRS(), SVDppRS(), NMFRS()]
#
#
#         except Exception as ex:
#             Logger('error').get_log().error(ex)
#
#     def getReader(self):
#         try:
#             print('run start', datetime.datetime.now())
#             self.result, self.data = {}, {}
#             print('筛选推荐系统')
#             if self.config['source'] == 'normal':
#                 self.reader = self.normalReader
#             # 读取某个商家某一类型数据
#             elif self.config['source'] == 'ES':
#                 self.reader = self.jsonReader
#         except Exception as ex:
#             traceback.print_exc()
#             Logger('error').get_log().error(ex)
#
#     # 训练最佳模型
#     def itemtrain(self, store, type, userbased: bool = False):
#         """
#         :param index:  商户名称
#         :param type: 商品类型
#         :return:
#         """
#         try:
#             # 不需要并行读取数据，不同模型训练数据相同
#             # pool = multiprocessing.Pool(processes=4)
#             # for num, model in enumerate(self.models[:4]):
#             #     print('电商' + index + '类型' + type + 'model' + str(num) + '读取数据')
#             #     self.data[index] = pool.apply(self.reader, (index, type, self.config['way']))
#             # pool.close()
#             # pool.join()
#             data = self.reader(store, type)
#             if not data: return None
#             print('读取数据完毕')
#             for num, model in enumerate(self.models[:4]):
#                 print('模型' + str(model) + '评估')
#                 params = {'name': 'pearson_baseline', 'user_based': userbased}
#                 model = model(params=params)
#                 ans = model.evaluate(data)
#                 if ans:
#                     self.result[num] = ans
#                 else:
#                     continue
#             MaxRMSE, MaxMAE, index = 0, 0, 0
#             for key, res in self.result.items():
#                 # res = res.get()
#                 if res and 'test_rmse' in res.keys() and res['test_rmse'].tolist():
#                     if np.mean(res['test_rmse'].tolist()) > MaxRMSE: index = key
#                 elif res and 'test_mae' in res.keys() and res['test_mae'].tolist():
#                     if np.mean(res['test_mse'].tolist()) > MaxMAE: index = key
#                 else:
#                     index = -1
#             if index == -1:
#                 print('数据量不够，模型训练失败')
#                 return
#             print('模型评估完毕, 最终选择' + str(index) + '号模型')
#             print('run finish', datetime.datetime.now())
#             model = self.models[index]
#
#             # 用已有数据进行模型训练
#             trainset = data.build_full_trainset()
#             model.fit(trainset)
#
#             print('----------------------------------test-------------------------------------------')
#             testset = trainset.build_testset()
#             predictions = model.algo.test(testset)
#
#             accuracy.rmse(predictions, verbose=True)  # ~ 0.9979 (which is low)
#             print('-----------------------------------end--------------------------------------------')
#             # 保存模型到store文件夹下的type.pickle文件中
#             self.save_model(model=model, store=store.split('-')[1], type=type)
#         except Exception as ex:
#             Logger('error').get_log().error(ex)
#             return
#
#     def usertrain(self, store, type, userbased: bool = False):
#         """
#         :param index:  商户名称
#         :param type: 商品类型
#         :return:
#         """
#         try:
#             data = self.reader(store, type)
#             if not data: return None
#             print('读取数据完毕')
#             for num, model in enumerate(self.models[:4]):
#                 print('模型' + str(model) + '评估')
#                 params = {'name': 'pearson_baseline', 'user_based': userbased}
#                 model = model(params=params)
#                 ans = model.evaluate(data)
#                 if ans:
#                     self.result[num] = ans
#                 else:
#                     continue
#             MaxRMSE, MaxMAE, index = 0, 0, 0
#             for key, res in self.result.items():
#                 # res = res.get()
#                 if res and 'test_rmse' in res.keys() and res['test_rmse'].tolist():
#                     if np.mean(res['test_rmse'].tolist()) > MaxRMSE: index = key
#                 elif res and 'test_mae' in res.keys() and res['test_mae'].tolist():
#                     if np.mean(res['test_mse'].tolist()) > MaxMAE: index = key
#                 else:
#                     index = -1
#             if index == -1:
#                 print('数据量不够，模型训练失败')
#                 return
#             print('模型评估完毕, 最终选择' + str(index) + '号模型')
#             print('run finish', datetime.datetime.now())
#             model = self.models[index]
#
#             # 用已有数据进行模型训练
#             trainset = data.build_full_trainset()
#             model.fit(trainset)
#
#             print('----------------------------------test-------------------------------------------')
#             testset = trainset.build_testset()
#             predictions = model.algo.test(testset)
#
#             accuracy.rmse(predictions, verbose=True)  # ~ 0.9979 (which is low)
#             print('-----------------------------------end--------------------------------------------')
#             # 保存模型到store文件夹下的type.pickle文件中
#             self.save_model(model=model, store=store.split('-')[1], type=type, toward=user)
#         except Exception as ex:
#             Logger('error').get_log().error(ex)
#             return
#
#     # 储存训练好的模型
#     def save_model(self, model, store, type, toward):
#         try:
#             if not os.path.exists(indexpath):
#                 os.makedirs(indexpath)
#             if not os.path.exists(indexpath + '/' + str(store)):
#                 os.makedirs(indexpath + '/' + str(store))
#             # path = indexpath/jingdong/user-1.pickle
#             path = indexpath + '/' + str(store) + '/' + toward + '-' + type + '.pickle'
#             with open(path, 'wb') as p:
#                 pickle.dump(model, p)
#                 print(path + "文件创建成功")
#         except Exception as ex:
#             Logger('error').get_log().error(ex)
#
#     def execute(self):
#         try:
#             es = ElasticSearch(elasticsearch_config)
#             # 获取所有索引
#             indexes = []
#             for dirs in os.listdir(indexpath):
#                 # predict-store 训练
#                 indexes.append('predict-' + dirs)
#             self.getRS()
#             self.getReader()
#             stores = {}
#             for index in indexes:
#                 store = index.split('-')[1]
#                 body = {
#                     "query": {
#                         "term": {
#                             "store": store
#                         }
#                     }
#                 }
#                 jsons = es.search(index=index, body=body)
#                 if jsons: types = jsons["hits"]["hits"]
#                 for type in types:
#                     stores.setdefault(index, [])
#                     if type["_source"]["itemtype"] not in stores[index]: stores[index].append(
#                         type["_source"]["itemtype"])  # 获取某个商场下的商品类型
#             for store, types in stores.items():
#                 for type in types:
#                     # 训练模型并保存到制定路径
#                     self.train(store, type)
#         except Exception as ex:
#             traceback.print_exc()
#             Logger('error').get_log().error(ex)
#
#
# if __name__ == '__main__':
#     generator = Generator(config={'type': 'KNN', 'source': 'ES', 'way': {"query": {"match_all": {}}}})
#     generator.execute()
#     pass

