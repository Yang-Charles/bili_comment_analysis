import pandas as pd
# data = pd.read_csv('bilibilib_gzxb.csv', usecols=[0, 1, 3, 4, 7])
data = pd.read_csv('../data/bilibilib_gzxb.csv')
print(data.head())

comment_data = data['content']
print(comment_data.head())

#  Cannot compare type 'Timestamp' with type 'str'
# pandas 读取 csv 文件时，date 列是 str 类型，
# 所以我们先将 date 列转换成 datetime 类型，然后基于 pandas 的 Timestamp 类型构建筛选条件。
data['date'] = pd.to_datetime(data['date'])
criteria = (data['score'] > 8) & (data['date'] > pd.Timestamp(2019, 1, 1))
print(data[criteria])

# 基于字符串的记录筛选
criteria_1 = data['author'].str.contains('阳')
print(data[criteria_1])
