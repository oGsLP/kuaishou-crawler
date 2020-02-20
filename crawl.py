#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author: lenovo by XYF
@file: crawl.py
@time: 2020/02/20
@function: 
"""

import requests
import json
import time
import os

profile_url = "https://live.kuaishou.com/profile/"
page_url = "https://live.kuaishou.com/m_graphql"
work_url = "https://live.kuaishou.com/u/"

headers = {
    'accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'Host': 'live.kuaishou.com',
    'Origin': 'https://live.kuaishou.com',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',

    # User-Agent 根据自己的电脑修改
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
    'Cookie': 'did=web_67063b98a8884a80dccf7ed18172acfa; clientid=3; client_key=65890b29; didv=1579495215536; userId=1489161552; kuaishou.live.bfb1s=477cb0011daca84b36b3a4676857e5a1; userId=1489161552; kuaishou.live.web_st=ChRrdWFpc2hvdS5saXZlLndlYi5zdBKgATq2nZA1Yla0gW-XmZNyzWqZVVbHQxzEi4IPFxnLR6lwBKiJQPYjnwHvU5p2ejU_456SQwWYx5AZX-X-gqKVvrObQ6mNLYmMTu9O7WYvj8-LBDTNnkLpQ7tpB3Yvumc-HPsnZkiKtWZkz54OdwENQaQ8OHMs-SZK-pIA77xXYv-CKPaW_40TnMRwaD4_TVcci5_ADYx8KlP76uPvkbh6TEQaEpwewD8CakIZrC7t8JEKqqml3iIgqvGUkWi91EPRqyOxbgLP49WtVMpVGdQYBobIs4upgr0oBTAB; kuaishou.live.web_ph=a70df58d8d097d3b613ace8ca7b6c502e8b1'
}


def crawl_user(uid):
    global headers
    payload = {"operationName": "privateFeedsQuery",
               "variables": {"principalId": uid, "pcursor": "", "count": 999},
               "query": "query privateFeedsQuery($principalId: String, $pcursor: String, $count: Int) {\n  privateFeeds(principalId: $principalId, pcursor: $pcursor, count: $count) {\n    pcursor\n    list {\n      id\n      thumbnailUrl\n      poster\n      workType\n      type\n      useVideoPlayer\n      imgUrls\n      imgSizes\n      magicFace\n      musicName\n      caption\n      location\n      liked\n      onlyFollowerCanComment\n      relativeHeight\n      timestamp\n      width\n      height\n      counts {\n        displayView\n        displayLike\n        displayComment\n        __typename\n      }\n      user {\n        id\n        eid\n        name\n        avatar\n        __typename\n      }\n      expTag\n      __typename\n    }\n    __typename\n  }\n}\n"}

    res = requests.post(page_url, headers=headers, json=payload)

    works = json.loads(res.content.decode(encoding='utf-8', errors='strict'))['data']['privateFeeds']['list']

    if not os.path.exists("data"):
        os.makedirs("data")

    # with open("data/" + uid + ".json", "w") as fp:
    #     fp.write(json.dumps(works, indent=2))

    name = works[0]['user']['name']

    dir = "data/" + name + "(" + uid + ")/"
    if not os.path.exists(dir):
        os.makedirs(dir)
    crawl_work(dir, works[0])

    # print(len(works))


def crawl_work(dir, work):
    w_caption = work['caption']
    w_time = time.strftime('%Y-%m-%d', time.localtime(work['timestamp'] / 1000))
    w_urls = work['imgUrls']

    for i in range(len(w_urls)):
        pic = dir + "/" + w_caption + "_" + w_time + "_" + str(i + 1) + ".jpg"
        if not os.path.exists(pic):
            r = requests.get(w_urls[i])
            r.raise_for_status()

            with open(pic, "wb") as f:
                f.write(r.content)


def crawl():
    crawl_user(uid="Zj08020125")


if __name__ == "__main__":
    crawl()
