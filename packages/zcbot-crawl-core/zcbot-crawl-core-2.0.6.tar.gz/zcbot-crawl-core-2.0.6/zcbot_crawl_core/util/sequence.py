# -*- coding: UTF-8 -*-
"""常用工具类"""
import random
from datetime import datetime
from uuid import uuid4

uuidChars = ("a", "b", "c", "d", "e", "f",
             "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s",
             "t", "u", "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5",
             "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "G", "H", "I",
             "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V",
             "W", "X", "Y", "Z")


def short_uuid():
    uuid = str(uuid4()).replace('-', '')
    result = ''
    for i in range(0, 8):
        sub = uuid[i * 4: i * 4 + 4]
        x = int(sub, 16)
        result += uuidChars[x % 0x3E]
    return result


# 生成批次编号
def gen_batch_id():
    # 时间(3位毫秒)+随机数(3位)
    return f"{datetime.now().strftime('%y%m%d%H%M%S%f')[0:10]}{random.randint(1000, 9990)}"


# 测试
if __name__ == '__main__':
    while True:
        print(gen_batch_id())
