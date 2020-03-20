from Common.FileProcess.AbstractClass import FileProcess
from Common.FileProcess.TXTFile import TXTFile
from Config.ChildSystemConfig.TPCS import Path
from Common.DatabaseProcess.MongoDB import *
from Common.LogProcess.Logger import Logger
from sklearn.datasets.base import Bunch
import pickle
import sys
import os

class BunchProcess(FileProcess):
    def __init__(self, path):
        self.path = path


    def bulid(self, path, bunchFile):
        with open(path, 'wb') as file:
            pickle.dump(bunchFile, file)

    def delete(self):
        if os.path.exists(self.path): os.remove(self.path)


    def read(self, content):
        with open(self.path, 'rb', errors='ignore') as file:
            bunch = pickle.load(file)
        return bunch


    #将数据库信息转化为bunch对象
    def dbSave(self, dbname = 'test'):
        try:
            Logger().get_log().error('将数据库信息转化为bunch对象')
            pathdict = Path(dbname).get_PathDict()
            catelist = os.listdir(pathdict['DataBasePath'])
            bunch = Bunch(target_name=[], label=[], filenames=[], contents=[])
            bunch.target_name.extend(catelist)  # 将类别保存到Bunch对象中
            mongoDB = MongoDB()
            mongoDB.connect(dbname)
            for table in catelist:
                collection = mongoDB.insert(table)
                for item in collection.find():
                    bunch.label.append(item['type'])
                    bunch.filenames.append(item['file_name'])
                    bunch.contents.append(item['content'].strip())
        except Exception as ex:
            Logger('error').get_log().error(ex)
        finally:
            return bunch


    #将txt文件转换为dat文件
    def txtSave(self, inputFile, outputFile):
        try:
            Logger().get_log().error('将文件信息转换为bunch对象')
            catelist = os.listdir(inputFile)
            bunch = Bunch(target_name=[], label=[], filenames=[], contents=[])
            bunch.target_name.extend(catelist)  # 将类别保存到Bunch对象中
            for eachDir in catelist:
                print(eachDir, inputFile)
                eachPath = inputFile + r"\\" + eachDir + r"\\"
                fileList = os.listdir(eachPath)
                for eachFile in fileList:  # 二级目录中的每个子文件
                    fullName = eachPath + eachFile  # 二级目录子文件全路径
                    bunch.label.append(eachDir)  # 当前分类标签
                    bunch.filenames.append(fullName)  # 保存当前文件的路径
                    bunch.contents.append(TXTFile(fullName).read().strip())  # 保存文件词向量
            with open(outputFile, 'wb') as file_obj:  # 持久化必须用二进制访问模式打开
                pickle.dump(bunch, file_obj)
                # pickle.dump(obj, file, [,protocol])函数的功能：将obj对象序列化存入已经打开的file中。
                # obj：想要序列化的obj对象。
                # file:文件名称。
                # protocol：序列化使用的协议。如果该项省略，则默认为0。如果为负值或HIGHEST_PROTOCOL，则使用最高的协议版

        except Exception as ex:
            Logger('error').get_log().error(ex)


    def operation(self):
        pass