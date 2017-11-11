#!/usr/bin/python3.4
# -*- coding: utf-8 -*-

import requests
import json
import time
import os

headers = {
    "User-Agent": "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5"
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
        jsonfile = open(filePath + str(int(time.time())) + ".json", "wb")
        jsonfile.write(jsonInfo)
        jsonfile.close()
        time.sleep(5)
        # infoList = bytesToDict(jsonInfo)
        # dictList = formatDict(page, infoList)
        # print(dictList)


if __name__ == "__main__":
    page = 2
    keyword = "iphone x".replace(" ", "+")
    getJsonData(page, keyword)
