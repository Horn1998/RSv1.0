from Common.LogProcess.Logger import Logger
from abc import ABCMeta, abstractmethod
import math
class AbstractRS(metaclass = ABCMeta):
    def __init__(self, prefs):
        self.prefs = prefs



    @abstractmethod
    def sim_distance(self, person, other): pass




    #找到和用户相似的前5名
    def rank(self, person, n=5):
        try:
            # 求参数用户和其他所有用户的相似系数
            scores = [(self.sim_distance(person, other), other) for other in self.prefs if other != person]
            # 排序,默认根据元组第一个元素
            scores.sort(reverse=True)
            return scores[0:n] if len(scores) <= n else scores
        except Exception as ex:
            Logger('error').get_log().error(ex)




    #给用户提供商品建议
    def advisor(self, person):
            totals, simSums = {}, {}
            for other in self.prefs:
                if other == person: continue
                score = self.sim_distance(person, other)
                #忽略评价值为0或者小于0的情况
                if score <= 0: continue
                for item in self.prefs[other]:
                    #多没有看过的商品进行评价
                    if item not in self.prefs[person] or self.prefs[person][item] == 0:
                        #相似度评价值
                        totals.setdefault(item, 0)
                        totals[item] += self.prefs[other][item] * score
                        #相似度之和
                        simSums.setdefault(item, 0)
                        simSums[item] += score

            rankings = [(totals[item] /simSums[item], item) for item, total in totals.items()]
            rankings.sort(reverse=True)
            return rankings if len(rankings) < 10 else rankings[:10]
