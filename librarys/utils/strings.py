import uuid
import datetime
import hashlib
import time


def get_uuid() -> str:
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


def gen_md5() -> str:
    m2 = hashlib.md5()
    m2.update(str(time.time()).encode("utf-8"))
    str_md5 = m2.hexdigest()
    return str_md5
