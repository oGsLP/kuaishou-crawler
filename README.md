# kuaishou-crawler

> As you can see, a crawler for kuaishou pictures and videos

## Latest 

### Version 0.5.0 (2020-08-06)
##### &emsp;View [Change Log](./CHANGELOG.md)

* 现在已经提供exe版本一键执行 [查看](#release) | 或者查看如何运行代码 [查看](#run)
* Python 3.7.3
    * requests
    * json
    * os
    * ~~BeautifulSoup~~
    * re
* 自v0.3.0版本开始，已用面向对象重构，核心代码在`lib/crawler.py`中，启动文件为`crawl.py` / `ks.py`
* 功能：根据用户ID来爬取快手用户的作品，包括视频和图片
    1. 在preset文件(**使用exe版本忽略此文件**)中一行行填写用户id，若缺少文件会自动创建（目前版本已提供自动根据数字id获取真实eid）
        * 分享链接用浏览器打开，根据网址 https://live.kuaishou.com/profile/xxxx 获取id: xxxx~~
        * 或者手机里点开快手用户的头像，底下会告诉你快手号的
    2. 使用时请自己用账号登录快手网站，并使用自己的`cookie['headers']`和`didweb`替换，不保证源代码中对应值可用
        * 关于cookie的did值，你在电脑浏览器中打开快手网站登录后随便打开一个用户的视频作品，然后再地址栏中找到这一项，咱们以giao哥的第一个视频为例
            - https://live.kuaishou.com/u/3x4tn6nm8gnh9xk/3xtd5zf5qbduphc?did=web_12345shiwoluandade
            - 你要保存下来的就是did后面的 `web_12345shiwoluandade`
    3. 因为快手官网会根据cookie，识别你是否在线，爬取的时候要将网页登录并挂着
        * 实测快手网站的用户验证存在30-60分钟左右的有效时长，出现`list index out of range`时极可能是有效期已过，登录网站验证即可
        * 暂且不知道快手官方对过多请求的处理，目前碰到的有上述验证失效，也许也会有请求达到数量会中断请求，此时注释preset中已爬取的用户id，重新开始运行脚本即可
    4. 爬取的视频~~暂时是带水印的(以后考虑获取无水印视频)~~ 是无水印的 **感谢@[tjftjftjf](https://github.com/tjftjftjf)提供手机抓包链接和方法**
    5. 修复了无水印视频url的获取
* 注意事项：
    * 不考虑提供列表可选的批量下载功能
    * 有需要的合理功能可以issue反馈，看到后会考虑是否修改
    * 如果需要自定义自己的需求，可以拿走代码自行修改，喜欢的话给个star给个follow
    * **本代码仅供学习使用，不可违反法律爬取视频，以及私自盗用搬运视频，后果自负**
    * **本代码仅供学习使用，不可违反法律爬取视频，以及私自盗用搬运视频，后果自负**
    * **本代码仅供学习使用，不可违反法律爬取视频，以及私自盗用搬运视频，后果自负**
    * 重要的说三遍

## Run

0. python3环境与命令行工具
1. 进入项目目录 `cd kuaishou-crawler`
2. 安装依赖 `pip install -r requirements.txt`
3. 运行，有两个版本，`crawl.py`为运行版本，`ks.py`是用于构建exe的版本，当然也可以运行
    * `python crawl.py` / `python ks.py`
    
## Release

https://github.com/oGsLP/kuaishou-crawler/releases

* 下载打包好的exe一键运行(点击download下载即可)
    * ks.exe
    * ks.7z


## Future

* ~~自动根据id获取eid~~ √
* 获取无水印视频 √
* 进一步丰富preset预设文件的可配置选项
* ~~优化代码和log~~ √
* 提供便捷的打包exe √

## Again

**本代码仅供学习使用，不可违反法律爬取视频，以及私自盗用搬运视频，后果自负**

## Else

爬虫源码免费开源，作者维护不易，喜欢的可以随意打赏一些>_<

<center>
    <figure>
        <img src="pics/alipay.JPG" height=360px style="margin-right:25px"/>
        <img src="pics/wechat.JPG" height=360px />
    </figure>
</center>