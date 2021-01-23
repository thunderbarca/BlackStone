import pathlib
import os


# 用来检查文件是否存在
def file_exists_check(filename: str) -> bool:
    path = pathlib.Path(filename)
    return path.exists()


# 用来删除文件
def file_delete(name: str):
    if file_exists_check(filename=name):
        os.unlink(name)
