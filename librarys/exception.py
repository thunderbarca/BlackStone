#!/usr/bin/env python

"""
Copyright (c) 2006-2020 sqlmap developers (http://sqlmap.org/)
See the file 'LICENSE' for copying permission
"""


class BlackBaseException(Exception):
    pass


class BlackImageStartException(BlackBaseException):
    pass


class BlackConnectException(BlackBaseException):
    def __init__(self, address):
        self.address = address

    def __str__(self):
        # print("姓名长度是" + str(self.address) + "，超过长度了")
        return f"<{self.address} 无法链接>"
