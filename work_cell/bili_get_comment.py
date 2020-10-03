import requests
from fake_useragent import UserAgent  #设置随机请求头与睡眠

import json
import pandas as pd
import time
import datetime
headers = {"User-Agent": UserAgent(verify_ssl=False).random}
comment_api = 'https://bangumi.bilibili.com/review/web_api/short/list?media_id=102392&folded=0&page_size=20&sort=0'
RETRIES = 5
requests.adapters.DEFAULT_RETRIES = RETRIES  # 增加重连次数
s = requests.session()
s.keep_alive = False  # 关闭多余连接
s.get(url=comment_api)  # 你需要的网址

#发送get请求
response_comment = requests.get(comment_api, headers=headers)
json_comment = json.loads(response_comment.text)


# {"code":0,"message":"success","result":{"list":[{"author":{"avatar":"http://i1.hdslb.com/bfs/face/0336a07674c94bfb73ea885ee49ae9cf24f81420.jpg",
#                                                            "mid":39403976,"uname":"繁风灯和清",
#                                                            "vip":{"themeType":0,"vipStatus":0,"vipType":0}},
#                                                  "content":"！","ctime":1558261913,"cursor":"77459741604063",
#                                                  "disliked":0,"liked":0,"likes":0,"mtime":1558261913,"review_id":6420703,
#                                                  "user_rating":{"score":10},
#                                                  "user_season":{"last_ep_id":232465,"last_ep_index":"1","last_index_show":"看至第1话"}}],
#                                         "total":19150}}
total = json_comment['result']['total']  # 当前一共有多少条评论

cols = ['author', 'score', 'disliked', 'liked', 'likes', 'ctime', 'review_id', 'content', 'last_ep_index', 'cursor']
data_all = pd.DataFrame(index=range(total), columns=cols)

j = 0
while j < total:
    n = len(json_comment['result']['list']) #得到当前json中一共包含多少条评论
    for i in range(n):
        data_all.loc[j, 'author'] = json_comment['result']['list'][i]['author']['uname']
        data_all.loc[j, 'score'] = json_comment['result']['list'][i]['user_rating']['score']
        data_all.loc[j, 'disliked'] = json_comment['result']['list'][i]['disliked']
        data_all.loc[j, 'liked'] = json_comment['result']['list'][i]['liked']
        data_all.loc[j, 'likes'] = json_comment['result']['list'][i]['likes']
        data_all.loc[j, 'ctime'] = json_comment['result']['list'][i]['ctime']
        data_all.loc[j, 'content'] = json_comment['result']['list'][i]['content']

        # 每一个json路径中cursor值就藏在前一个json的最后一条评论中
        data_all.loc[j, 'cursor'] = json_comment['result']['list'][n-1]['cursor']
        j += 1
    try:
        # 'last_ep_index',用户当前的看剧状态，比如看至第13话，第6话之类
        data_all.loc[j, 'last_ep_index'] = json_comment['result']['list']['i']['user_season']['last_ep_index']
    except:
        pass

    # 所有的json路径的前半部分都是一样，都是在第一条json之后加上不同的cursor = xxxxx
    # https: // bangumi.bilibili.com / review / web_api / short / list?media_id = 102392 & folded = 0 & page_size = 20 & sort = 0 & cursor = 77489806463194
    comment_api_next = comment_api + '&cursor=' + data_all.loc[j-1, 'cursor']
    response_comment = requests.get(comment_api_next, headers=headers)
    json_comment = json.loads(response_comment.text)
    print(json_comment)


    if j % 50 == 0:
        print('已完成{}%'.format(round(j/total*100, 2)))
    time.sleep(1.1)  # 控制访问频率

data_all = data_all.fillna(0)

# "ctime":1558261913,是Linux系统上的时间表示方式，可使用time.gmtime()转化为n/m/d/h/m/d
def getDate(x):
    x = time.gmtime(x)
    return (pd.Timestamp(datetime.datetime(x[0], x[1], x[2], x[3], x[4], x[5])))

data_all['date'] = data_all['ctime'].apply(lambda x:getDate(x))
data_all.to_csv('../data/bilibilib_gzxb.csv', index=False)













