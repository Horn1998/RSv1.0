from Common.FileProcess.AbstractClass import FileProcess
from Common.LogProcess.Logger import Logger
import pandas as pd
import traceback
import json
import os
class Json(FileProcess):
    def bulid(self):
       pass

    def delete(self, path):
        pass

    def read(self, path):
        '''
        :param path: 文件路径
        :return: dict
        '''
        try:
            with open(path, 'r') as f:
                return json.load(fp = f)
        except Exception as ex:
            Logger('error').get_log().error(ex)

    def dict_to_json(self, dict):
        return json.dumps(dict)



    def json_to_dict(self, json):
        return json.loads(json)


    def get_df(self, dict):
        return pd.DataFrame(dict)



    def operation(self):
        pass


if __name__ == '__main__':
    reader = Json()
    content = reader.read('')
    print(content)

