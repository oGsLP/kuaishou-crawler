#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: lenovo by XYF
@file: dist.py
@time: 2020/03/09
@function: 
"""

from lib.crawler import Crawler


def crawl():
    crawler = Crawler()

    param_did = input("预先输入本用户cookie中的did值：")
    crawler.set_did(param_did)

    uid = input("输入此次要爬取的用户id：")
    crawler.add_to_list(uid)

    crawler.crawl()

    input("请按回车键退出......")


if __name__ == "__main__":
    crawl()
