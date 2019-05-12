#!/usr/bin/python3.4
# -*- coding: utf-8 -*-

import requests
import json
import time
import os

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

# 这是新的方法，获取详情页的信息需要如下网址参考
# https://blog.csdn.net/github_38782597/article/details/82563477

def getJson(page, keyword):

    url = 'https://odin.re.taobao.com/m/Nwalltbuad?sbid=sem2_kgb_activity&ignore=CATID%2CRANKINFO%2CMATCHTYPE&pvid=_TL' \
          '-41832&refpid=mm_26632258_3504122_32554087&clk1=abab6283306413775910d4b0b37ca047&idfa=%7Bidfa%7D&pid' \
          '=430680_1006&keyword=' + keyword + '&count=60&offset=' + str(60 * page) + '&relacount=8&t=1535075213992' \
                                                                                     '&callback' \
                                                                                     '=mn17jsonp1535075213992 '
    r = session.get(url=url, headers=headers)
    html = r.text
    start = html.find('(')
    datas = (json.loads(html[start + 1:-1]))['result']['item']
    # 抓取详情页的库存、店名、收藏数
    detailInfo = getDetail(datas)
    return {"listItem":detailInfo}

def getDetail(datas):
    detailInfo = []
    for item in datas:
        try:
            resource_id = item["RESOURCEID"]
            url = r'https://h5api.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/?jsv=2.4.8&appKey=12574478&t=1535083295045' \
                  r'&sign=ef22a6dc765bd6ce86d36e2ba9a6cc33&api=mtop.taobao.detail.getdetail&v=6.0&dataType=jsonp&ttid=2017' \
                  r'%40taobao_h5_6.6.0&AntiCreep=true&type=jsonp&callback=mtopjsonp2&data=%7B%22itemNumId%22%3A%22' + str(
                resource_id) + r'%22%7D '
            r = session.get(url=url, headers=headers)
            html = r.text
            start = html.find('(')
            datas = (json.loads(html[start + 1:-1]))['data']
            # 库存
            quantity = json.loads(datas['apiStack'][0]['value'])['skuCore']['sku2info']['0']['quantity']
            item["quantity"]=quantity
            # 收藏
            favcount=datas['item']['favcount']
            item['favcount']=favcount
            # 店铺各种信息：名称：shopName、链接：taoShopUrl
            mergeItem = dict(item, **datas['seller'])
            detailInfo.append(mergeItem)
        except Exception as e:
            temp={'seller':{'shopName':'','taoShopUrl':'','quantity':'','favcount':''}}
            mergeItem = dict(item, **temp['seller'])
            detailInfo.append(mergeItem)
        time.sleep(1)
    return detailInfo

# 格式化字典
def formatDict(page, infoList):
    dictList = []
    for listItem in infoList:
        formatInfo = {}
        formatInfo["页数"] = page
        Trys("店铺", "shopName", formatInfo, listItem)
        Trys("店铺链接", "taoShopUrl", formatInfo, listItem)
        Trys("商品标题", "TITLE", formatInfo, listItem)
        Trys("原价", "GOODSPRICE", formatInfo, listItem)
        Trys("折扣价", "PROMOTEPRICE", formatInfo, listItem)
        Trys("售出件数", "SELL", formatInfo, listItem)
        Trys("库存", "quantity", formatInfo, listItem)
        Trys("收藏", "favcount", formatInfo, listItem)
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
