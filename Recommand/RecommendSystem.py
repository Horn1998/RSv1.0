from abc import ABCMeta, abstractmethod
from Common.LogProcess.Logger import Logger
from Common.FileProcess.JsonFile import Json
from surprise import Reader, Dataset
import pandas as pd
import io
class RSTool(metaclass=ABCMeta):
    #支持.csv .data文件
    def normalReader(self, line_format='user item rating', sep=','):
        try:
            self.reader = Reader(line_format=line_format, sep=sep)
            return Dataset.load_from_file(self.config['path'], reader=self.reader)
        except Exception as ex:
            Logger('error').get_log().error(ex)
            Logger('error').clear()


    #支持.json文件
    def jsonReader(self, rating_scale =(1, 5)):
        '''
        json数据格式：
        {'itemID': [1, 1, 1, 2, 2],
                'userID': [9, 32, 2, 45, 'user_foo'],
                'rating': [3, 2, 4, 3, 1]}
        :param rating_scale:
        :return:
        '''
        try:
            dic = Json(self.config['path']).read()
            dl = list(dic.keys())
            df = pd.DataFrame(dic)
            self.reader = Reader(rating_scale=rating_scale)
            # 传入的列必须对应着 userID，itemID 和 rating（严格按此顺序）。
            return Dataset.load_from_df(df[[label for label in dl]], reader=self.reader)
        except Exception as ex:
            Logger('error').get_log().error(ex)
            Logger('error').clear()




    def read_item_names(self, sep = '\t'):
        """
        获取电影名到电影id 和 电影id到电影名的映射
        """
        rid_to_name = {}
        name_to_rid = {}
        with io.open(self.path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.split(sep)
                rid_to_name[line[0]] = line[1]
                name_to_rid[line[1]] = line[0]

        return rid_to_name, name_to_rid



    #获取模型
    def get_model(self, userid, option):
        self.algo = None        #后期处理
        pass


    @abstractmethod
    def run(self): pass