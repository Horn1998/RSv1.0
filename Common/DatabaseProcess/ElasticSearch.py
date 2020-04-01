from Common.DatabaseProcess.AbstractClass import DatabaseProcess
from Common.FileProcess.Folder import Folder
from Common.FileProcess.TXTFile import TXTFile
from Common.LogProcess.Logger import Logger
from elasticsearch import Elasticsearch as ES
from elasticsearch import helpers
import traceback
import datetime
import jieba
import json
import os
class ElasticSearch(DatabaseProcess):
    def __init__(self, config):
        self._es = ES([{'host': config['host'],'port': config['port']}])
        if self._es.ping(): print('connect success')
        else: print('connect fail')

    def connect(self):
        pass


    def drop(self, index):
        try:
            self._es.indices.delete(index, ignore=[400, 404])
            print('drop '+index+' success')
        except Exception as ex:
            print('drop index fail')
            traceback.print_exc()
            Logger('error').get_log().error(ex)

    #此功能弃用
    def add(self, index, property, config = {'number_of_shards': 5, 'number_of_replicas': 0}):
        '''
        :param config: 设置分片和备份
        :return:
        '''
        settings = {
            "settings": {
                "number_of_shards": config['number_of_shards'],  # 一个分片
                "number_of_replicas": config['number_of_replicas']  # 0个备份
            },
            "mappings": {
                "Document": {
                    "dynamic": "strict",  # 含义不明确
                    # "properties": {
                    #     "content": {
                    #         "type": "text"
                    #     },
                    #     "file_name": {
                    #         "type": "text"
                    #     },
                    #     "Date": {
                    #         "type": "date"
                    #     }
                    # }
                    "properties":property,
                }
            }
        }
        try:
            if not self._es.indices.exists(index):
                self._es.indices.create(index = index, ignore = 400, body = settings)
                print('Created Index')
        except Exception as ex:
            Logger('error').get_log().error(ex, '创建失败')


    def delete(self, path):
        pass



    def search(self, index, body):
        """

        :param index: 索引
        :param body:     body = {"_source":"operated"}
        :return:
        """
        return self._es.search(index= index, body=body, size = 10000)



    def update(self, index:str, q:json, target:json, doc_type=None ):
        """
        :param index: 索引名称
        :param q:
        :param target:
        :return:
        """
        # update_body = {
        #     "query": {
        #         "bool": {
        #             "must": [
        #                 {
        #                     "term": {
        #                         "user": "test"
        #                     }
        #                 },
        #                 {
        #                     "term": {
        #                         "item": 'test'
        #                     }
        #                 }
        #             ]
        #         }
        #     },
        # "script": {
        #                     "inline": "ctx._source.score = params.score",
        #                     "params": {
        #                         "score": score
        #                     },
        #                     "lang": "painless"
        #
        #                 }
        #
        #             }
        try:
            update_body = {
                "query": {
                    "bool": {
                        "must": [q]
                    }
                },
                "script": {
                    "inline": "ctx._source.score = params.score",
                    "params": target,
                    "lang": "painless"

                }

            }
            self._es.update_by_query(index=index, doc_type=doc_type, body=update_body)
        except Exception as ex:
            traceback.print_exc()
            Logger('error').get_log().error(ex)




    #数据批量导入
    def insert(self, index, type, datas:list):
        actions = []
        for data in datas:
            action = {
                "_index": index,
                "_type": type,
                "_source": data
            }
            actions.append(action)
        startime = datetime.datetime.now()
        if len(actions):
            try:
                helpers.bulk(self._es, actions, request_timeout = 100)
                Logger().get_log().error('本次共写入｛｝条数据'.format(len(actions)))
            except Exception as ex:
                traceback.print_exc()
                Logger('error').get_log().error(ex)


    #将所有文档存储到elasticsearch中
    def documents_Init(self, DataBasePath, index_name='test'):
        '''
        在index_name数据库下创建表并添加数据
        :param Data_BasePath: 数据文件夹根目录
        :param index_name:    数据库名称
        :return:
        '''
        print('将所有文档存储到elasticsearch')
        folder, txtFile = Folder(), TXTFile()
        indexnames = os.listdir(DataBasePath)
        save_dict = []
        content = folder.read('txt', txtFile)
        for item in content:
            result = (str(content)).replace("\r\n", "").strip()  # 删除多余空行与空格
            cutResult = jieba.cut(result)  # 默认方式分词，分词结果用空格隔开
            # save_dict.append(
            #         {'file_name': ChildPath, 'content': result, 'type': name, 'keywords': ' '.join(cutResult)})
        try:
            self.insert(index_name, save_dict)  # 将数据批量导入elasticsearch
        except Exception as ex:
            traceback.print_exc()
            Logger('error').get_log().error(ex)
        else:
            Logger().get_log().error('索引初始化完成')


# 使日期序列化
class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return json.JSONEncoder.default(self, obj)


