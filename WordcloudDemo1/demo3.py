import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont

#img = Image.open("D:\\Code\\Python\\test\\img\\test02.jpg")
im_blank = Image.new("RGB",[1024,768],"white")
draw = ImageDraw.Draw(im_blank)
ft = ImageFont.truetype("C:\\WINDOWS\\Fonts\\SIMYOU.TTF", 20)
draw.text((30,30), u"Python图像处理库PIL从入门到精通",font = ft, fill = 'red')
ft = ImageFont.truetype("C:\\WINDOWS\\Fonts\\SIMYOU.TTF", 40)
draw.text((30,100), u"Python图像处理库PIL从入门到精通",font = ft, fill = 'green')
ft = ImageFont.truetype("C:\\WINDOWS\\Fonts\\SIMYOU.TTF", 60)
draw.text((30,200), u"Python图像处理库PIL从入门到精通",font = ft, fill = 'blue')
ft = ImageFont.truetype("C:\\WINDOWS\\Fonts\\SIMLI.TTF", 40)
draw.text((30,300), u"Python图像处理库PIL从入门到精通",font = ft, fill = 'red')
ft = ImageFont.truetype("C:\\WINDOWS\\Fonts\\STXINGKA.TTF", 40)
draw.text((30,400), u"Python图像处理库PIL从入门到精通",font = ft, fill = 'yellow')
#字体对象2在ttc中第一个（我也不知道具体是什么字形），字大小为36号
Font2 = ImageFont.truetype("C:\\Windows\\Fonts\\simsun.ttc",36,index = 0)
#字体对象2在ttc中第二个，字大小为36号
Font3 = ImageFont.truetype("C:\\Windows\\Fonts\\simsun.ttc",36,index = 1)
#draw.ink = 255 + 0 * 256 + 0 * 256 * 256       #红色
im_blank.show()
