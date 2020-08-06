#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: lenovo by XYF
@file: like.py
@time: 2020/03/27
@function: 
"""

from lib.crawler import Crawler
param_did = "web_2761de01059f8b0a60555ae7ff5d69e4"

def crawl():
    c = Crawler()
    c.set_did(param_did)
    c.crawl_like("3xzixigzwy4kj5c")


if __name__ == '__main__':
    crawl()
