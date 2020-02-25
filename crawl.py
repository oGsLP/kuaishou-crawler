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
from bs4 import BeautifulSoup
import re

profile_url = "https://live.kuaishou.com/profile/"
data_url = "https://live.kuaishou.com/m_graphql"
work_url = "https://live.kuaishou.com/u/"

param_did = "?did=web_67063b98a8884a80dccf7ed18172acfa"

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

    # User-Agent/Cookie 根据自己的电脑修改
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
    'Cookie': 'did=web_67063b98a8884a80dccf7ed18172acfa; clientid=3; client_key=65890b29; didv=1579495215536; userId=1489161552; kuaishou.live.bfb1s=477cb0011daca84b36b3a4676857e5a1; userId=1489161552; kuaishou.live.web_st=ChRrdWFpc2hvdS5saXZlLndlYi5zdBKgATq2nZA1Yla0gW-XmZNyzWqZVVbHQxzEi4IPFxnLR6lwBKiJQPYjnwHvU5p2ejU_456SQwWYx5AZX-X-gqKVvrObQ6mNLYmMTu9O7WYvj8-LBDTNnkLpQ7tpB3Yvumc-HPsnZkiKtWZkz54OdwENQaQ8OHMs-SZK-pIA77xXYv-CKPaW_40TnMRwaD4_TVcci5_ADYx8KlP76uPvkbh6TEQaEpwewD8CakIZrC7t8JEKqqml3iIgqvGUkWi91EPRqyOxbgLP49WtVMpVGdQYBobIs4upgr0oBTAB; kuaishou.live.web_ph=a70df58d8d097d3b613ace8ca7b6c502e8b1'
}


def crawl_user(uid):
    global headers
    payload = {"operationName": "privateFeedsQuery",
               "variables": {"principalId": uid, "pcursor": "", "count": 999},
               "query": "query privateFeedsQuery($principalId: String, $pcursor: String, $count: Int) {\n  privateFeeds(principalId: $principalId, pcursor: $pcursor, count: $count) {\n    pcursor\n    list {\n      id\n      thumbnailUrl\n      poster\n      workType\n      type\n      useVideoPlayer\n      imgUrls\n      imgSizes\n      magicFace\n      musicName\n      caption\n      location\n      liked\n      onlyFollowerCanComment\n      relativeHeight\n      timestamp\n      width\n      height\n      counts {\n        displayView\n        displayLike\n        displayComment\n        __typename\n      }\n      user {\n        id\n        eid\n        name\n        avatar\n        __typename\n      }\n      expTag\n      __typename\n    }\n    __typename\n  }\n}\n"}
    res = requests.post(data_url, headers=headers, json=payload)

    works = json.loads(res.content.decode(encoding='utf-8', errors='strict'))['data']['privateFeeds']['list']

    if not os.path.exists("data"):
        os.makedirs("data")

    # 这两行代码将response写入json供分析
    # with open("data/" + uid + ".json", "w") as fp:
    #     fp.write(json.dumps(works, indent=2))

    # 防止该用户在直播，第一个作品默认为直播，导致获取信息为NoneType
    if works[0]['id'] is None:
        works.pop(0)
    name = works[0]['user']['name']

    dir = "data/" + name + "(" + uid + ")/"
    # print(len(works))
    if not os.path.exists(dir):
        os.makedirs(dir)
    print("开始爬取用户 " + name + "，保存在目录 " + dir)
    print(" 共有" + str(len(works)) + "个作品")

    for j in range(len(works)):
        crawl_work(uid, dir, works[j], j + 1)
        time.sleep(1)
    print("用户 " + name + "爬取完成!")
    print()
    time.sleep(1)


'''
快手分为五种类型的作品，在作品里面表现为workType属性
 * 其中两种图集: `vertical`和`multiple`，意味着拼接长图和多图，所有图片的链接在imgUrls里
 * 一种单张图片: `single` 图片链接也在imgUrls里
 * K歌: `ksong` 图片链接一样，不考虑爬取音频...
 * 视频: `video` 需要解析html获得视频链接
'''


def crawl_work(uid, dir, work, wdx):
    w_type = work['workType']
    w_caption = re.sub(r"\s+", " ", work['caption'])
    w_name = re.sub(r'[\\/:*?"<>|\r\n]+', "", w_caption)[0:24]
    w_time = time.strftime('%Y-%m-%d', time.localtime(work['timestamp'] / 1000))

    if w_type == 'vertical' or w_type == 'multiple' or w_type == "single" or w_type == 'ksong':
        w_urls = work['imgUrls']
        l = len(w_urls)
        print("  " + str(wdx) + ")图集作品：" + w_caption + "，" + "共有" + str(l) + "张图片")
        for i in range(l):
            p_name = w_time + "_" + w_name + "_" + str(i + 1) + ".jpg"
            pic = dir + p_name
            if not os.path.exists(pic):
                r = requests.get(w_urls[i])
                r.raise_for_status()
                with open(pic, "wb") as f:
                    f.write(r.content)
                print("    " + str(i + 1) + "/" + str(l) + " 图片 " + p_name + " 下载成功 √")
            else:
                print("    " + str(i + 1) + "/" + str(l) + " 图片 " + p_name + " 已存在 √")
    elif w_type == 'video':
        w_url = work_url + uid + "/" + work['id'] + param_did
        res = requests.get(w_url, headers=headers)
        html = res.text
        soup = BeautifulSoup(html, "html.parser")

        pattern = re.compile(r"playUrl", re.MULTILINE | re.DOTALL)
        script = soup.find("script", text=pattern)
        s = pattern.search(script.text).string
        v_url = s.split('playUrl":"')[1].split('.mp4')[0].encode('utf-8').decode('unicode-escape') + '.mp4'
        print("  " + str(wdx) + ")视频作品：" + w_caption)
        v_name = w_time + "_" + w_name + ".mp4"
        video = dir + v_name

        if not os.path.exists(video):
            r = requests.get(v_url)
            r.raise_for_status()

            with open(video, "wb") as f:
                f.write(r.content)
            print("    视频 " + v_name + " 下载成功 √")
        else:
            print("    视频 " + v_name + " 已存在 √")
    else:
        print("错误的类型")


def read_preset():
    p_path = "preset"
    u_arr = []
    if not os.path.exists(p_path):
        print("创建预设文件 preset ...")
        open(p_path, "w")
    if not os.path.getsize(p_path):
        print("请在预设文件 preset 中记录需要爬取的用户id，一行一个")
        exit(0)
    with open(p_path, "r") as f:
        for line in f:
            if line[0] != "#":
                u_arr.append(line.strip())
    return u_arr


def switch_id(uid):
    payload = {"operationName": "SearchOverviewQuery",
               "variables": {"keyword": uid, "ussid": None},
               "query": "query SearchOverviewQuery($keyword: String, $ussid: String) {\n  pcSearchOverview(keyword: $keyword, ussid: $ussid) {\n    list {\n      ... on SearchCategoryList {\n        type\n        list {\n          categoryId\n          categoryAbbr\n          title\n          src\n          __typename\n        }\n        __typename\n      }\n      ... on SearchUserList {\n        type\n        ussid\n        list {\n          id\n          name\n          living\n          avatar\n          sex\n          description\n          counts {\n            fan\n            follow\n            photo\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      ... on SearchLivestreamList {\n        type\n        lssid\n        list {\n          user {\n            id\n            avatar\n            name\n            __typename\n          }\n          poster\n          coverUrl\n          caption\n          id\n          playUrls {\n            quality\n            url\n            __typename\n          }\n          quality\n          gameInfo {\n            category\n            name\n            pubgSurvival\n            type\n            kingHero\n            __typename\n          }\n          hasRedPack\n          liveGuess\n          expTag\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"}
    res = requests.post(data_url, headers=headers, json=payload)
    dt = json.loads(res.content.decode(encoding='utf-8', errors='strict'))['data']
    return dt['pcSearchOverview']['list'][1]['list'][0]['id']


def crawl():
    for uid in read_preset():
        if uid.isdigit():
            crawl_user(switch_id(uid))
        else:
            crawl_user(uid)


if __name__ == "__main__":
    crawl()
