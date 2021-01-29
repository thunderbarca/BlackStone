import time

from librarys.utils.strings import generate_random_str
from librarys.utils.strings import gen_md5


def generate_flag(salt: str) -> str:
    """
    用来生成动态flag字符串
    :param salt:
    :return:
    """
    flag_plain = generate_random_str(12) + salt + str(time.time())
    return f'flag{{{gen_md5(flag_plain.encode("utf-8"))}}}'
