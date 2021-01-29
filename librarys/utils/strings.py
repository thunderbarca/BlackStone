import uuid
import datetime
import hashlib
import time
import random
import string


def get_uuid() -> str:
    """
    生成唯一id值
    :return:
    """
    return str(uuid.uuid4())


# 获取当前时间的字符串表现形式
def get_now_time() -> str:
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# 将字符转换成实数
def str2int(s):
    try:
        return int(s)
    except ValueError:
        if '-' == s[0]:
            return 0 - str2int(s[1:])
        elif s[0] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            num = 0
            for i in range(len(s)):
                if s[i] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                    num = num * 10 + int(s[i])
                else:
                    return num
        else:
            return 0


def gen_md5(info: bytes) -> str:
    """
    用来生成字符串的md5值
    :param info:加密的信息
    :return:
    """
    m2 = hashlib.md5()
    m2.update(info)
    str_md5 = m2.hexdigest()
    return str_md5


def generate_random_str(length=6) -> str:
    """
    用来生成随机字符串的函数
    :param length: 随机字符串函数的长度
    :return:
    """
    ascii_char = string.ascii_lowercase + string.digits + string.ascii_uppercase
    str_list = [random.choice(ascii_char) for _ in range(length)]
    random_str = ''.join(str_list)
    return random_str
