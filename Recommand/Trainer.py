from Common.LogProcess.Logger import Logger
from Recommand.RecommendSystem import RSTool
class Trainer(RSTool):
    #获得模型
    def __init__(self, config):
        self.algo = self.get_model(userid= config['user'], option= config['option'])
        if config['format'] == 'json': self.data = self.jsonReader(config['path']).reader()
        elif config['format'] == 'csv': self.data = self.normalReader(config['path']).reader()
        elif config['format'] == 'data': self.data = self.normalReader(config['path'], sep = '\t').reader()


    #训练模型
    def train(self):
        try:
            trainset = self.data.build_full_trainset()
            self.algo.fit(trainset)
        except Exception as ex:
            Logger('error').get_log().error(ex)


    def run(self):
        self.train()