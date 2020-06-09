from wordcloud import WordCloud
import PIL.Image as image
import numpy as np
import jieba


# 分词
def trans_CN(text):
    # 接收分词的字符串
    word_list = jieba.cut(text)
    # 分词后在单独个体之间加上空格
    result = "".join(word_list)
    return result

def drawClouds():
    with open("D:\data.txt") as fp:
        text = fp.read()
        # print(text)
        # 将读取的中文文档进行分词
        text = trans_CN(text)
        # mask = np.array(image.open("F:\wordcloud\image\love.jpg"))
        wordcloud = WordCloud(font_path='C:/Windows/Fonts/simkai.ttf',
                              background_color='white',
                              ).generate(text)
        image_produce = wordcloud.to_image()
        image_produce.show()

def write():
    a = 'Django ' * 100
    d = '测试工具 ' * 70
    e = 'Jenkins ' * 30
    f = open('D:\data.txt', 'r+')
    f.read()
    f.write(d)
    f.close()
drawClouds()