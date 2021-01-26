import math


def DynamicValueChallenge(initial: int, solve_count: int, decay: int = 5) -> int:
    """

    :param initial: 题目的初始值
    :param solve_count: 已经解答题目的用户数量
    :param decay: 前几名动态分
    :return:
    """
    minimum = math.floor(initial / 2)

    if solve_count != 0:
        # We subtract -1 to allow the first solver to get max point value
        solve_count -= 1

    # 双星表示乘方
    value = (((minimum - initial) / (decay ** 2)) * (solve_count ** 2)) + initial
    value = math.ceil(value)

    if value < minimum:
        value = minimum

    return value
