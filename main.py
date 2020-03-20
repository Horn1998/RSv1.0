#测试使用配置文件
from Config.ChildSystemConfig.RecommandCS import *
from Config.ChildSystemConfig.TPCS import *
from django.http import HttpResponse
#实际读取文件
from Builder import EngineFactory
import pymongo
def get_Config(user_id, model_type): pass
def MAIN(request):
    # config = get_Config(request['user'],  request['model_type'])
    # EngineFactory(config).build()
    return HttpResponse('OK')
