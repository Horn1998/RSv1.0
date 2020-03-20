import numpy as np
from sklearn.linear_model import LogisticRegression
import pickle

class test:
    def __init__(self):
        self.t1 = 1
        self.t2 = [1, 2, 3]

if __name__ == '__main__':
    with open('./the_first_pickle.pickle', 'rb') as r:
        obj = pickle.load(r)  # 将列表读取
    print(obj.t1)
    print(obj.t2)