from elasticsearch import Elasticsearch
import traceback
import datetime
from decimal import Decimal
def Timer(index, host =  '192.168.0.13', port = 9200):
    try:
        es = Elasticsearch([{'host': host,'port': port}])
        array_search = es.search(index=index, body={"query": {"match_all": {}}}, size=10000 )
        jsons = array_search["hits"]["hits"]

        # 对用户数据进行聚合，评分
        #scores:获取用户对于某一个特定商品的满意度
        stores, scores = [], {}
        #{ "_source": { "userid":???,"operated":???,"storeid":???,"itemtype":???,"score":???，'@timestamp': '2020-03-21T10:50:38.817Z' }}
        for hits in jsons:
            user = hits["_source"]["userid"]
            operated = hits["_source"]["operated"]
            storeid = hits["_source"]["storeid"]
            itemtype = hits["_source"]["itemtype"]
            key = str(user) + '||' + str(operated) + '||' + str(storeid) +'||' + str(itemtype) if itemtype  else  str(user) + '||' + str(operated) + '||' + str(storeid) +'|| all'
            scores.setdefault(key, 0)
            score = scores[key]
            #-1表示用户对此商品不感兴趣 ,保存用户对于商品最佳满意度
            scores[key] = -1 if hits["_source"]["score"] == -1 else max(score, hits["_source"]["score"])
            if storeid not in stores: stores.append(storeid)
        # data = {"userid":1,"itemid":1,"user":"test","item":"test","score":0, 'itemtype':'test'}


        #获取电商之前最大id
        StoreId = {}
        for store in stores:
            if not es.indices.exists('predict-' + store):
                StoreId[store] = 0
                continue
            maxbody = {

                "query": {
                    "term": {
                        "store": store
                    }
                },
                "aggs": {  # 聚合查询
                    "max_id": {  # 最大值的key
                        "max": {  # 最大
                            "field": "userid"  # 查询"id"的最大值
                        }
                    }
                }
            }
            ans = es.search(index="predict-" + store, body=maxbody)
            max_id = int(ans['aggregations']['max_id']['value'])
            StoreId[store] = max_id



        # #将最新数据更新到predict-store中
        for items in scores.items():
            user, item, store, itemtype = items[0].split('||')[0], items[0].split('||')[1], items[0].split('||')[2], items[0].split('||')[3]
            if not es.indices.exists('predict-' + store):
                es.index(index='predict-' + store, body={'store': store, 'user': user, 'item': item, 'score': items[1], 'userid': 1, 'itemid': 1, 'itemtype': itemtype })
                continue

            searchbody = {
                "query": {
                    "bool": {
                        "must": [
                            {
                                "term": {
                                    "user": user
                                }
                            },
                            {
                                "term": {
                                    "item": item
                                }
                            },
                        ]
                    }
                }
            }
            index = "predict-" + store
            #index field {"itemid":1,"score":5,"item":"test","userid":1,"user":"test", "store":"taobao"}
            ans = es.search(index=index, body=searchbody)
            source = ans['hits']['hits']
            # id = es.count(index=index, q="store:" + str(store))
            if len(source) == 0:
                StoreId[store] += 1
                max_id = StoreId[store]
                es.index(index=index,
                         body={'itemtype': itemtype, 'store': store, 'user': user, 'item': item, 'score': items[1],
                               'userid': max_id, 'itemid': max_id})
                continue
            source = source[0]["_source"]
            #评分=历史评分 * 0.3 + 最新评分 * 0.7
            score = 0.7 * float(items[1]) + 0.3 * float(source['score'])
            update_body = {
                "query": {
                    "bool": {
                        "must": [
                            {
                                "term": {
                                    "user": str(user)
                                }
                            },
                            {
                                "term": {
                                    "item": str(item)
                                }
                            }
                        ]
                    }
                },
                "script": {
                    "inline": "ctx._source.score = params.score",
                    "params": {
                        "score": Decimal(score).quantize(Decimal("0.00"))
                    },
                    "lang": "painless"
                }
            }
            es.update_by_query(index=index, body=update_body)



        #根据时间戳删除超过一定日期的数据
        today = datetime.date.today()
        for hits in jsons:
            before = hits["_source"]["@timestamp"]

            d1 = datetime.datetime.strptime(before.split("T")[0], '%Y-%m-%d')
            d2 = datetime.datetime.strptime(str(today), '%Y-%m-%d')
            delta = d2 - d1
            # query = {'query': {'match': {'@timestamp': '2020-03-21T10:50:38.817Z'}}}
            # es.delete_by_query(index='log-1', body=query)
            if(delta.days > 30):
                #match匹配的是_source中的数据
                query = {'query':{'match':{'@timestamp':before}}}
                #删除过时数据
                es.delete_by_query(index=index, body=query)

    except Exception as ex:
        traceback.print_exc()
from threading import Thread, Lock
from time import sleep

class AsyncInsert:
    def __init__(self):\
        self._lock = Lock()



    def run(self, store, es, index, itemtype, user, item, score):
        with self._lock:
            maxbody = {

                           "query": {
                           "term": {
                           "store": store
                           }
                           },
                           "aggs": {  # 聚合查询
                           "max_id": {  # 最大值的key
                           "max": {  # 最大
                           "field": "userid"  # 查询"id"的最大值
                           }
                           }
                           }
                              }
            ans = es.search(index="predict-" + store, body=maxbody)
            max_id = int(ans['aggregations']['max_id']['value'])
            es.index(index=index,
                     body={'itemtype': itemtype, 'store': store, 'user': user, 'item': item, 'score': score,
                           'userid': max_id + 1, 'itemid': max_id + 1})



if __name__ == '__main__':
    Timer(index='log-jingdong')
    #
    # es = Elasticsearch([{'host': '192.168.0.13', 'port': 9200}])
    # es.indices.delete(index='predict-jingdong', ignore = [400, 404])
    # maxbody = {
    #
    #     "query": {
    #            "term":{
    #                         "store":"jingdong"
    #                 }
    #     },
    #     "aggs": {  # 聚合查询
    #         "max_id": {  # 最大值的key
    #             "max": {  # 最大
    #                 "field": "userid"  # 查询"age"的最大值
    #             }
    #         }
    #     }
    # }
    # ans = es.search(index="predict-jingdong", body=maxbody)
    # print(ans['aggregations']['max_id']['value'])


