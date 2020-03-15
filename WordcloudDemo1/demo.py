import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud,ImageColorGenerator
from PIL import Image,ImageOps
from skimage import measure,draw,data,color,filters

def DrawWordcloud(read_name):
    image = Image.open('timg.jpg')#作为背景形状的图
    graph = np.array(image)

    #参数分别是指定字体、背景颜色、最大的词的大小、使用给定图作为背景形状
    # max_words 要显示的词的最大个数
    # scale: float(default=1)  # 按照比例进行放大画布，如设置为1.5，则长和宽都是原来画布的1.5倍
    # mask: 如果参数为空，则使用二维遮罩绘制词云。如果 mask 非空，遮罩形状被 mask 取代
    wc = WordCloud(font_path = 'C:\\windows\\Fonts\\msyhbd.ttc',  #'C:\\windows\\Fonts\\simhei.ttf'
                   background_color = 'White',
                   max_words = 3000,
                   mask = graph,
                   random_state=30,
                   scale= 1)

    tb = pd.read_csv(read_name) #读取词频文件CSV（逗号分割）到DataFrame
    words = list(tb.word)  #词表
    values = tb.val #词频表

    dic = {}
    for key,val in zip(words, values):
        dic[key] = val

    wc.generate_from_frequencies(dic) #根据给定词频生成词云
    image_color = ImageColorGenerator(graph)
    plt.imshow(wc)
    plt.axis("off") #不显示坐标轴
    plt.show()
    img3 = wc.to_image()
    img3 = img3.convert('RGBA')
    #img3.show()
    wc.to_file('Wordcloud.png')#保存的图片命名为Wordcloud.png

    img1 = Image.open('timg.jpg').convert('L')  # 读图片并转化为灰度图
    edges = filters.sobel(img1)
    e_img = Image.fromarray(edges)
    e_img.show()
    #plt.imshow(edges, plt.cm.gray)

    #img1.show()
    img_array = np.array(img1)  # 转化为数组

    w, h = img_array.shape

    img_border = np.zeros((w + 1, h + 1))

    for x in range(1, w - 1):
        for y in range(1, h - 1):
            Sx = img_array[x + 1][y - 1] + 2 * img_array[x + 1][y] + img_array[x + 1][y + 1] - \
                 img_array[x - 1][y - 1] - 2 * \
                 img_array[x - 1][y] - img_array[x - 1][y + 1]
            Sy = img_array[x - 1][y + 1] + 2 * img_array[x][y + 1] + img_array[x + 1][y + 1] - \
                 img_array[x - 1][y - 1] - 2 * \
                 img_array[x][y - 1] - img_array[x + 1][y - 1]
            img_border[x][y] = (Sx * Sx + Sy * Sy) ** 0.5
            #img_border[x-1][y-1] = img_border[x][y]

    img2 = Image.fromarray(img_border)
    #img2.convert('RGBA')
    #img2.show()
    i_img2 = ImageOps.grayscale(img2)
    #i_img2.show()
    i_img3 = ImageOps.invert(i_img2)
    i_img3 = i_img3.convert('RGBA')
    #r, g, b, alpha = i_img3.split()
    #r, g, b, alpha = i_img3.split()
    #i_img3.show()
    #alpha = alpha.point(lambda i: i > 0 and 204)
    #i_img3.size = img3.size
    #img4 = img3.paste(i_img3,(0,0))
    #img4 = Image.composite(img3, i_img3, alpha)
    i_img3 = i_img3.resize(img3.size)
    img4 = Image.blend(img3, i_img3, 0.3)
    img4.show()
    #i_img3.paste(img3, (0, 0))
    #i_img3.show()

if __name__=='__main__':

    DrawWordcloud("word_lst.csv")
