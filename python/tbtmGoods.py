#!/usr/bin/python3.4
# -*- coding: utf-8 -*-

import requests
import json
import time
import os

# 这是老的方法
"""
headers = {
    "User-Agent":
        "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5"
}

session = requests.session()
session.get("https://s.m.taobao.com/", headers=headers)
def getJson(page, keyword):
    getData = {
        "event_submit_do_new_search_auction": "1",
        "search": "提交",
        "tab": "all",
        "_input_charset": "utf-8",
        "topSearch": "1",
        "atype": "b",
        "searchfrom": "1",
        "action": "home:redirect_app_action",
        "from": "1",
        "q": keyword,
        "sst": "1",
        "n": "20",
        "buying": "buyitnow",
        "m": "api4h5",
        "abtest": "30",
        "wlsort": "30",
        "style": "list",
        "closeModues": "nav,selecthot,onesearch",
        "page": page
    }

    preUrl = "http://s.m.taobao.com/search?"
    # 升级头部
    headers.update(
        dict(Referer="http://s.m.taobao.com", Host="s.m.taobao.com"))
    # 抓取网页
    aliUrl = session.get(url=preUrl, params=getData, headers=headers)

    return aliUrl.content


# 解析抓取到的json
def bytesToDict(content):
    dictInfo = json.loads(content.decode("utf-8", "ignore"))
    infoList = dictInfo["listItem"]

    return infoList

# 格式化字典
def formatDict(page, infoList):
    dictList = []
    for listItem in infoList:
        formatInfo = {}
        formatInfo["页数"] = page
        Trys("店名", "nick", formatInfo, listItem)
        Trys("商品标题", "title", formatInfo, listItem)
        Trys("商品打折价", "price", formatInfo, listItem)
        Trys("发货地址", "location", formatInfo, listItem)
        Trys("评论数", "commentCount", formatInfo, listItem)
        Trys("原价", "originalPrice", formatInfo, listItem)
        Trys("售出件数", "act", formatInfo, listItem)
        Trys("折扣政策", "zkType", formatInfo, listItem)
        Trys("付款人数", "act", formatInfo, listItem)
        Trys("金币折扣", "coinLimit", formatInfo, listItem)
        Trys("详情页", "url", formatInfo, listItem)
        Trys("图像URL", "pic_path", formatInfo, listItem)
        # 修饰value
        formatInfo["详情页"] = "https:" + formatInfo["详情页"]
        formatInfo["图像URL"] = formatInfo["图像URL"].replace('60x60', '720x720')
        dictList.append(formatInfo)

    return dictList
"""

# 这是新的方法，获取详情页的信息需要如下网址参考
# https://blog.csdn.net/github_38782597/article/details/82563477
def getJson(page, keyword):

    session = requests.session()
    headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'referer': 'https://uland.taobao.com/semm/tbsearch?refpid=mm_26632258_3504122_32554087&keyword=%E5%A5%B3%E8'
                   '%A3%85 '
                   '&rewriteQuery=1&a=mi={imei}&sms=baidu&idfa={'
                   'idfa}&clk1=abab6283306413775910d4b0b37ca047&upsid=abab6283306413775910d4b0b37ca047',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/%s Mobile Safari/537.36',
    }

    url = 'https://odin.re.taobao.com/m/Nwalltbuad?sbid=sem2_kgb_activity&ignore=CATID%2CRANKINFO%2CMATCHTYPE&pvid=_TL' \
          '-41832&refpid=mm_26632258_3504122_32554087&clk1=abab6283306413775910d4b0b37ca047&idfa=%7Bidfa%7D&pid' \
          '=430680_1006&keyword=' + keyword + '&count=60&offset=' + str(60 * page) + '&relacount=8&t=1535075213992' \
                                                                                     '&callback' \
                                                                                     '=mn17jsonp1535075213992 '
    r = session.get(url=url, headers=headers)
    html = r.text
    start = html.find('(')
    datas = (json.loads(html[start + 1:-1]))['result']['item']
    return {"listItem":datas}


# 格式化字典
def formatDict(page, infoList):
    dictList = []
    for listItem in infoList:
        formatInfo = {}
        formatInfo["页数"] = page
        Trys("商品标题", "TITLE", formatInfo, listItem)
        Trys("原价", "GOODSPRICE", formatInfo, listItem)
        Trys("折扣价", "PROMOTEPRICE", formatInfo, listItem)
        Trys("售出件数", "SELL", formatInfo, listItem)
        Trys("详情页", "EURL", formatInfo, listItem)
        Trys("图像URL", "TBGOODSLINK", formatInfo, listItem)
        dictList.append(formatInfo)
    return dictList


# 一个try
def Trys(key1, key2, dict1, dict2):
    try:
        dict1[key1] = dict2[key2]
    except:
        dict1[key1] = "None"

    return dict1


# 创建递归文件夹
def createfiles(filepathname):
    try:
        os.makedirs(filepathname)
    except Exception as err:
        print(str(filepathname) + "已经存在！")


def getJsonData(page, keyword):
    for item in range(0, page):
        jsonInfo = getJson(page + 1, keyword)
        # 保存json到本地
        filePath = "json/" + str(time.strftime('%Y%m%d', time.localtime(time.time()))) + "/"
        createfiles(filePath)
        with open(filePath + str(int(time.time())) + ".json", "w") as jsonfile:
            json.dump(jsonInfo,jsonfile)
            jsonfile.close()
        time.sleep(5)

if __name__ == "__main__":
    page = 2
    keyword = "iphone x".replace(" ", "+")
    getJsonData(page, keyword)
