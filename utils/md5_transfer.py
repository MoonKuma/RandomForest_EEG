#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : md5_transfer.py
# @Author: MoonKuma
# @Date  : 2019/2/12
# @Desc  : use md5 to irreversibly cipher the name of participants

import hashlib
m2 = hashlib.md5()


def md5_transfer(input_str):
    m2.update(str(input_str).encode('utf-8'))
    return m2.hexdigest()

res = list()
test_list = ['a','b','c','列宁','斯大林','迈克尔·乔丹', '安哥拉宝贝', 'This is suppose to be a verrrrrrrrrrrrrrrrrrrrry long sentences']
for name in test_list:
    res.append(md5_transfer(name))

for name in res:
    print(name)