import random
import string
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from io import BytesIO
import os

# pip3 install pillow

class Captcha:
    def __init__(self):
        # 字体路径
        self.font_path = os.path.join(__name__, 'UbuntuMono-RI.ttf')
        # self.font_path = '/usr/share/fonts/truetype/ubuntu/UbuntuMono-RI.ttf'
        print(self.font_path)
        # 生成验证码位数
        self.text_num = 4
        # 生成图片尺寸
        self.pic_size = (100, 40)
        # 背景颜色，默认为白色
        self.bg_color = (255, 255, 255)
        # 字体颜色，默认为蓝色
        self.text_color = (0, 0, 255)
        # 干扰线颜色，默认为红色
        self.line_color = (255, 0, 0)
        # 是否加入干扰线
        self.draw_line = True
        # 加入干扰线条数上下限
        self.line_number = (1, 5)
        # 是否加入干扰点
        self.draw_points = True
        # 干扰点出现的概率(%)
        self.point_chance = 2

        self.image = Image.new('RGBA', (self.pic_size[0], self.pic_size[1]), self.bg_color)
        self.font = ImageFont.truetype(self.font_path, 25)
        self.draw = ImageDraw.Draw(self.image)
        self.text = self.gene_text()

    def gene_text(self):
        # 随机生成一个字符串
        source = list(string.ascii_letters)
        for i in range(0, 10):
            source.append(str(i))
        return ''.join(random.sample(source, self.text_num))

    def gene_line(self):
        # 随机生成干扰线
        begin = (random.randint(0, self.pic_size[0]), random.randint(0, self.pic_size[1]))
        end = (random.randint(0, self.pic_size[0]), random.randint(0, self.pic_size[1]))
        self.draw.line([begin, end], fill=self.line_color)

    def gene_points(self):
        # 随机绘制干扰点
        for w in range(self.pic_size[0]):
            for h in range(self.pic_size[1]):
                tmp = random.randint(0, 100)
                if tmp > 100 - self.point_chance:
                    self.draw.point((w, h), fill=(0, 0, 0))

    def gene_code(self):
        # 生成验证码图片
        font_width, font_height = self.font.getsize(self.text)
        self.draw.text(
            ((self.pic_size[0] - font_width) / self.text_num, (self.pic_size[1] - font_height) / self.text_num), self.text,
            font=self.font,
            fill=self.text_color)
        if self.draw_line:
            n = random.randint(self.line_number[0],self.line_number[1])
            print(n)
            for i in range(n):
                self.gene_line()
        if self.draw_points:
            self.gene_points()
        params = [1 - float(random.randint(1, 2)) / 100,
                  0,
                  0,
                  0,
                  1 - float(random.randint(1, 10)) / 100,
                  float(random.randint(1, 2)) / 500,
                  0.001,
                  float(random.randint(1, 2)) / 500
                  ]
        self.image = self.image.transform((self.pic_size[0], self.pic_size[1]), Image.PERSPECTIVE, params)  # 创建扭曲
        self.image = self.image.filter(ImageFilter.EDGE_ENHANCE_MORE)  # 滤镜，边界加强
        return self.image


def get_captcha_img():
    x = Captcha()
    image = x.gene_code()
    image.save('/tmp/demo.png')
    print(dir(image))
    print(x.text)
    out = BytesIO()
    image.save(out, format='PNG')
    return out.getvalue(), x.text



if __name__ == "__main__":
    x = Captcha()
    image = x.gene_code()
    image.show()
    image.save('./a.png')
    print(dir(image))
    print(x.text)