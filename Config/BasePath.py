#为了方便Linux与Windows下路径转换，这里设置基础路径
import os, sys
import copy
#当前文件路径
path = os.getcwd()
#当前文件父路径
basepath = os.path.abspath(os.path.dirname(path) + os.path.sep + ".")
indexpath = copy.deepcopy(basepath + r'\测试样例\测试文件夹')
