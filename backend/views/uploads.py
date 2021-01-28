import time

from settings.base import BASE_DIR
from django.views.generic import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from librarys.mixin.permission import AdminRequiredMixin
from librarys.utils.strings import gen_md5
from settings.config import WHITE_LIST


class UploadView(AdminRequiredMixin, View):

    @staticmethod
    def post(request):
        upload_file = request.FILES.get("file", None)  # 获取上传的文件，如果没有文件，则默认为None
        if not upload_file:
            data = {
                "code": 1,
                "msg": "文件上传错误",
            }

            return JsonResponse(data)

        extra_name = upload_file.name.split(".")[-1]

        if extra_name not in WHITE_LIST:
            data = {
                "code": 1,
                "msg": f"只允许上传后缀为{','.join(WHITE_LIST)}的文件",
            }

            return JsonResponse(data)

        filename = gen_md5(str(time.time()).encode("utf-8")) + "." + upload_file.name.split(".")[-1]
        store_path = BASE_DIR.joinpath("front", "static", "front", "uploads", filename)
        destination = open(store_path, 'wb+')  # 打开特定的文件进行二进制的写操作
        for chunk in upload_file.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()

        full_path = str(store_path).replace(str(BASE_DIR.joinpath("front")), "")
        data = {
            "code": 0,
            "msg": "文件上传成功",
            "src": full_path,
        }

        return JsonResponse(data)

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(UploadView, self).dispatch(*args, **kwargs)
