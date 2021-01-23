import random

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from io import BytesIO

from django.http import HttpResponse
from django.views.generic import View

from settings.base import BASE_DIR


# 获取随机颜色的函数
def get_random_color():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)


class CaptchaView(View):

    @staticmethod
    def get(request):
        # 生成一个图片对象
        img_obj = Image.new(
            'RGB',
            (200, 45),
            get_random_color()
        )
        # 在生成的图片上写字符
        # 生成一个图片画笔对象
        draw_obj = ImageDraw.Draw(img_obj)
        # 加载字体文件， 得到一个字体对象
        font_obj = ImageFont.truetype(str(BASE_DIR.joinpath("backend/static/backend/font/kumo.ttf")), 38)
        # 开始生成随机字符串并且写到图片上
        tmp_list = []
        for i in range(4):
            u = chr(random.randint(65, 90))  # 生成大写字母
            l = chr(random.randint(97, 122))  # 生成小写字母
            n = str(random.randint(0, 9))  # 生成数字，注意要转换成字符串类型

            tmp = random.choice([u, l, n])
            tmp_list.append(tmp)
            draw_obj.text((20 + 40 * i, 0), tmp, fill=get_random_color(), font=font_obj)

        # 保存到session
        request.session["valid_code"] = "".join(tmp_list)

        # 不需要在硬盘上保存文件，直接在内存中加载就可以
        io_obj = BytesIO()
        # 将生成的图片数据保存在io对象中
        img_obj.save(io_obj, "png")
        # 从io对象里面取上一步保存的数据
        data = io_obj.getvalue()
        return HttpResponse(data)
