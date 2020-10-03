

import pandas as pd
from pyecharts.charts import Pie, Line, Scatter
import os
import numpy as np
import jieba
import jieba.analyse
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

# font = FontProperties(fname=r'c:\windows\fonts\simsun.ttc') # size=20指定本机的汉字字体位置
font = FontProperties(fname='/Users/MAC/Library/Fonts/msyh.ttf')

# os.chdir('F:\\python_study\\pachong\\工作细胞')

datas = pd.read_csv('../data/bilibilib_gzxb.csv', index_col=0, encoding='utf8')

"""
描述性分析
"""

del datas['ctime']
del datas['cursor']
del datas['liked']

# 评分分布，评分分布取值2，4，6，8，10 对应1-5颗星

scores = datas['score'].groupby(datas['score']).count()
print(scores.head())

pie_chart.add(
    "评分",
    ['一星', '二星', '三星', '四星', '五星'],
    scores.values,
    radius=[40, 75],
    #    center=[50, 50],
    is_random=True,
    #    radius=[30, 75],
    is_legend_show=False,
    is_label_show=True,
)
pie_chart.render('评分.html')


datas['date'] = datas['date'].apply(lambda x: pd.Timestamp(x).date())
datas['time'] = datas['date'].apply(lambda x: pd.Timestamp(x).time().hour)

print(datas.iat[1, 1])  #取data的第一列.head())
num_date = datas.author.groupby(datas['date']).count()
num_date = datas['author'].groupby(datas['date']).count()
print(num_date.head())

# 评论数日期分布
chart = Line("评论数日期分布")
chart.use_theme('dark')
chart.add('评论数日期分布', num_date.index, num_date.values, is_fill=True, line_opacity=0.2,
          area_opacity=0.4, symbol=None)

chart.render('评论时间分布.html')

# 好评字数分布
datalikes = datas.loc[datas.likes > 5]
datalikes['num'] = datalikes.content.apply(lambda x: len(x))
chart = Scatter("likes")
chart.use_theme('dark')
chart.add('likes', np.log(datalikes.likes), datalikes.num, is_visualmap=True,
          xaxis_name='log(评论字数)',

          )
chart.render('好评字数分布.html')

# 评论每日内的时间分布
num_time = datas.author.groupby(datas['time']).count()

# 时间分布

chart = Line("评论日期内时间分布")
chart.use_theme('dark')
chart.add("评论数", x_axis=num_time.index.values, y_axis=num_time.values,
          is_label_show=True,
          mark_point_symbol='diamond', mark_point_textcolor='#40ff27',
          line_width=2
          )

chart.render('评论日内时间分布.html')

# 时间分布
chart = Line("评论数时间分布")
chart.use_theme('dark')
chart.add('评论数时间分布', num_date.index, num_date.values, is_fill=True, line_opacity=0.2,
          area_opacity=0.4, symbol=None)

chart.render('评论时间分布.html')

# 评分时间分布
datascore = datas.score.groupby(datas.dates).mean()
chart = Line("评分时间分布")
chart.use_theme('dark')
chart.add('评分', datascore.index,
          datascore.values,
          line_width=2
          )
chart.render('评分时间分布.html')

"""
评论分析
"""

texts = ';'.join(datas.content.tolist())
cut_text = " ".join(jieba.cut(texts))
# TF_IDF
keywords = jieba.analyse.extract_tags(cut_text, topK=500, withWeight=True, allowPOS=('a', 'e', 'n', 'nr', 'ns'))
text_cloud = dict(keywords)
pd.DataFrame(keywords).to_excel('TF_IDF关键词前500.xlsx')

bg = plt.imread("血小板.jpg")
# 生成
wc = WordCloud(  # FFFAE3
    background_color="white",  # 设置背景为白色，默认为黑色
    width=400,  # 设置图片的宽度
    height=600,  # 设置图片的高度
    mask=bg,
    random_state=2,
    max_font_size=500,  # 显示的最大的字体大小
    font_path="STSONG.TTF",
).generate_from_frequencies(text_cloud)
# 为图片设置字体

# 图片背景
# bg_color = ImageColorGenerator(bg)
# plt.imshow(wc.recolor(color_func=bg_color))
plt.imshow(wc)
# 为云图去掉坐标轴
plt.axis("off")
plt.show()
wc.to_file("词云.png")
