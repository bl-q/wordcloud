import os
import numpy as np
from operator import itemgetter
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator
from wordcloud.query_integral_image import query_integral_image

from PIL import Image, ImageOps, ImageDraw, ImageFont

item1 = itemgetter(1)

FONT_PATH = os.environ.get("FONT_PATH", "C:\\windows\\Fonts\\simkai.ttf")

STOPWORDS = set([x.strip() for x in open(
    os.path.join(os.path.dirname(__file__), 'stopwords.txt'),
    encoding= 'utf-8').read().split('\n')])

#重要参数：词云图像的height, width, 及背景boolean_mask
#重要属性：height，width和integral
class IntegralOccupancyMap(object):
    def __init__(self, height, width, mask):
        self.height = height
        self.width = width
        if mask is not None:
            # the order of the cumsum's is important for speed ?!
            self.integral = np.cumsum(np.cumsum(255 * mask, axis=1),
                                      axis=0).astype(np.uint32)
        else:
            self.integral = np.zeros((height, width), dtype=np.uint32)
    # 采样位置
    def sample_position(self, size_x, size_y, random_state):
        # 调用内建的计算积分图（integral image）函数
        return query_integral_image(self.integral, size_x, size_y,
                                    random_state)
    # 更新self.integral
    def update(self, img_array, pos_x, pos_y):
        partial_integral = np.cumsum(np.cumsum(img_array[pos_x:, pos_y:],
                                               axis=1), axis=0)
        # paste recomputed part into old image
        # if x or y is zero it is a bit annoying
        if pos_x > 0:
            if pos_y > 0:
                partial_integral += (self.integral[pos_x - 1, pos_y:]
                                     - self.integral[pos_x - 1, pos_y - 1])
            else:
                partial_integral += self.integral[pos_x - 1, pos_y:]
        if pos_y > 0:
            partial_integral += self.integral[pos_x:, pos_y - 1][:, np.newaxis]

        self.integral[pos_x:, pos_y:] = partial_integral

# 定义文化词云子类
class CTCultureWordCloud(WordCloud):
    """This is a class about word cloud for Chinese Traditional culture.

    Parameters
    ----------

    Attributes
    ----------
    ``words_`` : dict of string to float
        Word tokens with associated frequency.

        .. versionchanged: 2.0
            ``words_`` is now a dictionary

    ``layout_`` : list of tuples (string, int, (int, int), int, color))
        Encodes the fitted word cloud. Encodes for each word the string, font
        size, position, orientation and color.

    Notes
    -----

    """

    # 子类构造方法
    def __init__(self, font_paths=None, width=400, height=200, margin=2,
                 ranks_only=None, prefer_horizontal=.9, mask=None, scale=1,
                 color_func=None, max_words=200, min_font_size=4,
                 stopwords=None, random_state=None, background_color='black',
                 max_font_size=None, font_step=1, mode="RGB",
                 relative_scaling=.5, regexp=None, collocations=True,
                 colormap=None, normalize_plurals=True):
        #font_path : string list //字体路径列表，需要展现什么字体就把该字体路径+后缀名写上，如：font_path = '黑体.ttf'
        #font_step: int(default=1) //字体步长，如果步长大于1，会加快运算但是可能导致结果出现较大的误差。
        #max_words: number(default=200) // 要显示的词的最大个数
        #stopwords : set of strings or None //设置需要屏蔽的词，如果为空，则使用内置的STOPWORDS
        #random_state : 随机状态
        #background_color : color value (default=”black”) //背景颜色，如background_color='white',背景颜色为白色。
        #width : int (default=400) //输出的画布宽度，默认为400像素
        #height : int (default=200) //输出的画布高度，默认为200像素
        #prefer_horizontal : float (default=0.90) //词语水平方向排版出现的频率，默认 0.9
        # （词语垂直方向排版出现频率为 0.1 ）
        #mask : nd-array or None (default=None) //如果参数为空，则使用二维遮罩绘制词云。如果 mask 非空，
        # 设置的宽高值将被忽略，
        # 遮罩形状被 mask 取代。除全白（#FFFFFF）的部分将不会绘制，其余部分会用于绘制词云。
        # 如：bg_pic = imread('读取一张图片.png')，背景图片的画布一定要设置为白色（#FFFFFF），
        # 然后显示的形状为不是白色的其他颜色。可以用ps工具将自己要显示的形状复制到一个纯白色的画布上再保存，就ok了。
        #scale : float (default=1) //按照比例进行放大画布，如设置为1.5，则长和宽都是原来画布的1.5倍。
        #mode : string (default=”RGB”) //当参数为“RGBA”并且background_color不为空时，背景为透明。
        #relative_scaling : float (default=.5) //词频和字体大小的关联性
        #color_func : callable, default=None //生成新颜色的函数，如果为空，则使用 self.color_func
        #regexp : string or None (optional) //使用正则表达式分隔输入的文本
        #collocations : bool, default=True //是否包括两个词的搭配
        #colormap : string or matplotlib colormap, default=”viridis” //给每个单词随机分配颜色，
        # 若指定color_func，则忽略该方法。

        #fit_words(frequencies) // 根据词频生成词云
        #generate(text) // 根据文本生成词云
        #generate_from_frequencies(frequencies[, ...]) // 根据词频生成词云
        #generate_from_text(text) // 根据文本生成词云
        #process_text(text) // 将长文本分词并去除屏蔽词（此处指英语，中文分词还是需要自己用别的库先行实现）
        # 使用上面的 fit_words(frequencies)
        #fit_words(frequencies) ）
        #recolor([random_state, color_func, colormap]) // 对现有输出重新着色。重新上色会比重新生成整个词云快很多。
        #to_array() // 转化为 numpy array
        #to_file(filename) // 输出到文件

        # 初始化子类的属性
        # 增加字体列表子类属性
        if font_paths is None:
            font_paths = [FONT_PATH]
        self.font_paths = font_paths

        # 调用父类的构造方法，
        super().__init__(FONT_PATH, width, height, margin,
                 ranks_only, prefer_horizontal, mask, scale,
                 color_func, max_words, min_font_size,
                 stopwords, random_state, background_color,
                 max_font_size, font_step, mode,
                 relative_scaling, regexp, collocations,
                 colormap, normalize_plurals)

    # 子类重新改写的词云生成方法，返回值是词云对象本身
    # frequencies为词频字典
    def generate_from_frequencies(self, frequencies, max_font_size=None):
        frequencies = sorted(frequencies.items(), key=item1, reverse=True)
        if len(frequencies) <= 0:
            raise ValueError("We need at least 1 word to plot a word cloud, "
                             "got %d." % len(frequencies))
        frequencies = frequencies[:self.max_words]

        # largest entry will be 1
        max_frequency = float(frequencies[0][1])

        frequencies = [(word, freq / max_frequency)
                       for word, freq in frequencies]

        if self.random_state is not None:
            random_state = self.random_state
        else:
            random_state = Random()

        if self.mask is not None:
            mask = self.mask
            width = mask.shape[1]
            height = mask.shape[0]
            if mask.dtype.kind == 'f':
                warnings.warn("mask image should be unsigned byte between 0"
                              " and 255. Got a float array")
            if mask.ndim == 2:
                boolean_mask = mask == 255
            elif mask.ndim == 3:
                # if all channels are white, mask out
                boolean_mask = np.all(mask[:, :, :3] == 255, axis=-1)
            else:
                raise ValueError("Got mask of invalid shape: %s"
                                 % str(mask.shape))
        else:
            boolean_mask = None
            height, width = self.height, self.width
        # 核心调用IntegralOccupancyMap，建立占用对象occupancy
        # 参数：height背景区域高度（像素数），width背景区域宽度（像素数），boolean_mask是否是前景像素（黑色255）的bool数组
        occupancy = IntegralOccupancyMap(height, width, boolean_mask)

        # create 灰度image
        img_grey = Image.new("L", (width, height))
        draw = ImageDraw.Draw(img_grey) #建立图像生成对象
        img_array = np.asarray(img_grey)
        # 初始化词云内部区域布局信息列表（显示字体类型、字体大小、显示位置、旋转角度、显示颜色）
        # 增加了字体类型
        font_types, font_sizes, positions, orientations, colors = [], [], [], [], []

        last_freq = 1.

        if max_font_size is None:
            # if not provided use default font_size
            max_font_size = self.max_font_size

        if max_font_size is None:
            # figure out a good font size by trying to draw with
            # just the first two words
            if len(frequencies) == 1:
                # we only have one word. We make it big!
                font_size = self.height
            else:
                # 只生成两个词
                self.generate_from_frequencies(dict(frequencies[:2]),
                                               max_font_size=self.height)
                # find font sizes
                sizes = [x[2] for x in self.layout_]
                font_size = int(2 * sizes[0] * sizes[1] / (sizes[0] + sizes[1]))
        else:
            font_size = max_font_size

        # we set self.words_ here because we called generate_from_frequencies
        # above... hurray for good design?
        # 修改为可重复文字列表
        self.words_ = dict(frequencies)

        # start drawing grey image
        # 修改部分
        fonts_len = len(self.font_paths)
        # 可重复性汉字或英文单词和频率的元组列表[(word1,freq1),...,(wordm,freqm)]
        my_frequencies = []

        # 对每个词循环
        for word, freq in frequencies:
            # select the font size
            # rs为词频和字体大小的关联性系数
            rs = self.relative_scaling
            if rs != 0:
                font_size = int(round((rs * (freq / float(last_freq))
                                       + (1 - rs)) * font_size))
            #self.prefer_horizontal为词语水平方向排版出现的频率，默认 0.9
            if random_state.random() < self.prefer_horizontal:
                orientation = None
            else:
                orientation = Image.ROTATE_90
            tried_other_orientation = False

            # 随机选取一种字体
            n = random_state.randint(0, fonts_len-1)
            # 只保留"_"前面的汉字或英文
            word = word.split("_")[0]
            while True:
                # try to find a position
                font = ImageFont.truetype(self.font_paths[n], font_size)
                # transpose font optionally
                transposed_font = ImageFont.TransposedFont(
                    font, orientation=orientation)
                # get size of resulting text
                # 返回一个两元素的元组，是给定字符串像素意义上的size
                box_size = draw.textsize(word, font=transposed_font)
                # find possible places using integral image:
                # 返回值result是一个二元组坐标位置（x,y）
                result = occupancy.sample_position(box_size[1] + self.margin,
                                                   box_size[0] + self.margin,
                                                   random_state)
                #
                if result is not None or font_size < self.min_font_size:
                    # either we found a place or font-size went too small
                    break
                # if we didn't find a place, make font smaller
                # but first try to rotate!
                if not tried_other_orientation and self.prefer_horizontal < 1:
                    orientation = (Image.ROTATE_90 if orientation is None else
                                   Image.ROTATE_90)
                    tried_other_orientation = True
                else:
                    font_size -= self.font_step
                    orientation = None

            if font_size < self.min_font_size:
                # we were unable to draw any more
                break

            x, y = np.array(result) + self.margin // 2
            # actually draw the text
            draw.text((y, x), word, fill="white", font=transposed_font)
            positions.append((x, y))
            orientations.append(orientation)
            font_types.append(n)
            font_sizes.append(font_size)
            # 修改font_path=self.font_paths[n]
            colors.append(self.color_func(word, font_size=font_size,
                                          position=(x, y),
                                          orientation=orientation,
                                          random_state=random_state,
                                          font_path=self.font_paths[n]))
            # 添加选项
            my_frequencies.append((word, freq))
            # recompute integral image
            if self.mask is None:
                img_array = np.asarray(img_grey)
            else:
                img_array = np.asarray(img_grey) + boolean_mask
            # recompute bottom right
            # the order of the cumsum's is important for speed ?!
            # 更新self.integral属性
            occupancy.update(img_array, x, y)
            last_freq = freq #记录上一次处理的词频

        self.layout_ = list(zip(my_frequencies, font_types, font_sizes, positions,
                                orientations, colors))
        return self

    # 生成词云图片方法
    def to_image(self):
        self._check_generated()
        if self.mask is not None:
            width = self.mask.shape[1]
            height = self.mask.shape[0]
        else:
            height, width = self.height, self.width
        # self.mode的default=”RGB”，“RGBA”并且background_color不为空时，背景为透明
        img = Image.new(self.mode, (int(width * self.scale),
                                    int(height * self.scale)),
                        self.background_color)
        draw = ImageDraw.Draw(img)
        for (word, count), font_type, font_size, position, orientation, color in self.layout_:
            font = ImageFont.truetype(self.font_paths[font_type],
                                      int(font_size * self.scale))
            transposed_font = ImageFont.TransposedFont(
                font, orientation=orientation)
            pos = (int(position[1] * self.scale),
                   int(position[0] * self.scale))
            draw.text(pos, word, fill=color, font=transposed_font)
        return img

    def recolor(self, random_state=None, color_func=None, colormap=None):
        """Recolor existing layout.

        Applying a new coloring is much faster than generating the whole
        wordcloud.

        Parameters
        ----------
        random_state : RandomState, int, or None, default=None
            If not None, a fixed random state is used. If an int is given, this
            is used as seed for a random.Random state.

        color_func : function or None, default=None
            Function to generate new color from word count, font size, position
            and orientation.  If None, self.color_func is used.

        colormap : string or matplotlib colormap, default=None
            Use this colormap to generate new colors. Ignored if color_func
            is specified. If None, self.color_func (or self.color_map) is used.

        Returns
        -------
        self
        """
        if isinstance(random_state, int):
            random_state = Random(random_state)  #random_state是随机数生成种子
        self._check_generated() # 检查layout_属性是否倍计算了

        if color_func is None:
            if colormap is None:
                color_func = self.color_func
            else:
                color_func = colormap_color_func(colormap)
        # 布局属性被重新计算，word_freq为元组
        self.layout_ = [(word_freq, font_type, font_size, position, orientation,
                         color_func(word=word_freq[0], font_size=font_size,
                                    position=position, orientation=orientation,
                                    random_state=random_state,
                                    font_path=self.font_paths[font_type]))
                        for word_freq, font_type, font_size, position, orientation, _
                        in self.layout_]
        return self

# 绘制文化词云函数
# 参数read_name是生成词云的词频文件名
def DrawWordcloud(read_name):
    image = Image.open('sou1.jpg') #作为背景形状的图
    graph = np.array(image)
    # 图片并转化为灰度图像，获取图像矩阵img_array
    img_array = np.array(image.convert('L'))

    #img1 = Image.open('timg.jpg').convert('L')  # 读图片并转化为灰度图像
    # img1.show()
    #img_array = np.array(img1)  # 转化为数组

    w, h = img_array.shape

    # 获取背景图轮廓（图像边缘检测）
    img_border = np.zeros((w, h))
    # 通过源图像每个元素与卷积算子（sobel算子做卷积和）进行乘积再求和（忽略最外圈边框像素）
    for x in range(1, w - 1):
        for y in range(1, h - 1):
            Sx = img_array[x + 1][y - 1] + 2 * img_array[x + 1][y] + img_array[x + 1][y + 1] - \
                 img_array[x - 1][y - 1] - 2 * \
                 img_array[x - 1][y] - img_array[x - 1][y + 1]
            Sy = img_array[x - 1][y + 1] + 2 * img_array[x][y + 1] + img_array[x + 1][y + 1] - \
                 img_array[x - 1][y - 1] - 2 * \
                 img_array[x][y - 1] - img_array[x + 1][y - 1]
            #得到梯度
            img_border[x][y] = (Sx * Sx + Sy * Sy) ** 0.5
            # img_border[x-1][y-1] = img_border[x][y]

    img2 = Image.fromarray(img_border)
    # img2.convert('RGBA')
    # img2.show()
    # 生成轮廓灰度图像并反转
    i_img2 = ImageOps.grayscale(img2)
    # i_img2.show()
    i_img3 = ImageOps.invert(i_img2)
    # 生成轮廓的透明格式图像
    i_img3 = i_img3.convert('RGBA')
    #i_img3.show()
    # r, g, b, alpha = i_img3.split()
    # r, g, b, alpha = i_img3.split()
    # alpha = alpha.point(lambda i: i > 0 and 204)

    # 生成图云
    #参数分别是指定字体、背景颜色、最大的词的大小、使用给定图作为背景形状
    # max_words 要显示的词的最大个数
    # scale: float(default=1)  # 按照比例进行放大画布，如设置为1.5，则长和宽都是原来画布的1.5倍
    # mask: 如果参数为空，则使用二维遮罩绘制词云。如果 mask 非空，遮罩形状被 mask 取代

    # 设置字体路径表
    font_paths=['C:\\windows\\Fonts\\msyhbd.ttc',
                'C:\\windows\\Fonts\\simkai.ttf',
                'C:\\windows\\Fonts\\simhei.ttf',
                'C:\\windows\\Fonts\\STLITI.TTF',
                'C:\\windows\\Fonts\\STHUPO.TTF',
                'C:\\windows\\Fonts\\STXINGKA.TTF',
                'C:\\windows\\Fonts\\STFANGSO.TTF',
                'C:\\windows\\Fonts\\FZYTK.TTF',
                'C:\\windows\\Fonts\\SIMYOU.TTF'
                ]
    wc = CTCultureWordCloud(font_paths,
                   background_color = 'White',
                   max_words = 3000,
                   mask = graph,
                   random_state=30,
                   scale= 1)

    tb = pd.read_csv(read_name) #调用pandas读取词频文件CSV（逗号分割）到DataFrame
    words = list(tb.word)  #词表 (series类型)
    values = tb.val #词频表 (series类型)

    dic = {}
    for key,val in zip(words, values):
        dic[key] = val

    wc.generate_from_frequencies(dic) #根据给定词频词典生成词云

    # 根据图片生成词云颜色
    image_colors = ImageColorGenerator(graph)
    #wc.recolor(color_func=image_colors)

    img3 = wc.to_image()
    img3 = img3.convert('RGBA')
    #img3.show()
    wc.to_file('Wordcloud.png') #保存的图片命名为Wordcloud.png

    plt.imshow(wc)
    plt.axis("off")  # 不显示坐标轴
    plt.show()

    #i_img3.size = img3.size
    #img4 = img3.paste(i_img3,(0,0))
    #img4 = Image.composite(img3, i_img3, alpha)
    i_img3 = i_img3.resize(img3.size)
    # 合成带文字轮廓的词云图（两个图像混合插入方法）
    img4 = Image.blend(img3, i_img3, 0.3)
    img4.show()
    img4.save('Wordcloud4.png')
    #i_img3.paste(img3, (0, 0))
    #i_img3.show()

if __name__=='__main__':

    DrawWordcloud("word_lst.csv")

