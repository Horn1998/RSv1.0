from Common.DatabaseProcess.AbstractClass import DatabaseProcess
from Config.DatabaseConfig.MongoDB import mongo_config
from Common.LogProcess.Logger import Logger
from sklearn.utils import Bunch
import pymongo
import pickle
import os
class MongoDB(DatabaseProcess):
    #连接数据库
    def connect(self, name):
        try:
            self.myclient = pymongo.MongoClient("mongodb://" + mongo_config['host'] + ':' + mongo_config['port'])
            self.db = self.myclient[name]
        except Exception as e:
            Logger('error').get_log().error(e)


    #删除数据库中的表
    def drop(self, table):
        try:
            collist = self.db.list_collection_names()
            if table not in collist: print('删除{}表失败'.format(table))
            else:
                self.db[table].drop()
                print("删除{}表成功".format(table))
        except Exception as ex:
            Logger('error').get_log().error(ex)


    #添加数据库表
    def insert(self, table):
        try:
            collist = self.db.list_collection_names()
            if table in collist:
                print('数据表已经存在，无需重复创建')
            return self.db[table]
        except Exception as e:
            Logger('error').get_log().error(e)


    #表级操作 数据查询
    def search(self, collection, target:dict):
        try:
            return self.db[collection].find_one(target)
        except Exception as ex:
            Logger('error').get_log().error(ex)


    def search_many(self, collection, target:dict):
        try:
            return self.db[collection].find(target)
        except Exception as ex:
            Logger('error').get_log().error(ex)

    #表级操作 数据修改
    def update(self, collection, filter, update):
        try:
            return self.db[collection].find_one_and_update(filter, {'$set': update})
        except Exception as ex:
            Logger('error').get_log().error(ex)


    #表级操作 数据删除
    def delete(self, path):
        pass

    #表级操作 数据添加
    def add(self):
        pass



    # 将数据库信息转为bunch对象
    def bunchSave(self, config, dbname='test'):
        try:
            print('将数据库信息转换为bunch对象')
            catelist = os.listdir(config['DataBasePath'])
            bunch = Bunch(target_name=[], label=[], filenames=[], contents=[])
            bunch.target_name.extend(catelist)  # 将类别保存到Bunch对象中
            for table in catelist:
                # init_Table(db, table)
                collection = self.db[table]
                for item in collection.find():
                    bunch.label.append(item['type'])
                    bunch.filenames.append(item['file_name'])
                    bunch.contents.append(item['content'].strip())
            return bunch
        except Exception as ex:
            Logger('error').get_log().error(ex)


if __name__ == '__main__':
    Logger('error').get_log().error('233333')