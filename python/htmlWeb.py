#!/usr/bin/python3.4
# -*- coding: utf-8 -*-

from flask import Flask, request, render_template
from py.tbtmGoods.tbtmGoods import *


def getfilename(filename):
    for root, dirs, files in os.walk(filename):
        array = files
        if array:
            return array


def getfilesname(filename):
    for root, dirs, files in os.walk(filename):
        array = dirs
        if array:
            return array


def readJson(jsonPath):
    list = []
    array = getfilename(jsonPath)

    for jn in array:
        jnPh = jsonPath + "/" + jn
        file = open(jnPh, "rb")
        infoList = json.loads(file.read().decode("utf-8", "ignore"))
        dictList = formatDict(1, infoList["listItem"])
        list = list + dictList
    return list


try:
    jsonPath = "json/" + time.strftime('%Y%m%d', time.localtime(time.time()))
    dictList = readJson(jsonPath)
except:
    dictList = [
        {"店名": "", "标题": "", "原价": "", "折扣价": "", "地址": "", "评论": "", "销量": "", "卖点": "", "优惠": "", "图像URL": ""}]

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == 'GET':
        return render_template("index.html", dictList=dictList, days=getfilesname("json/"))
    elif request.method == 'POST':
        search = request.form["search"]
        page = request.form["page"]
        if search and page:
            getJsonData(int(page), search)
            jsonPath = "json/" + time.strftime('%Y%m%d', time.localtime(time.time()))
            newList = readJson(jsonPath)
            return render_template("index.html", dictList=newList, days=getfilesname("json/"))
        elif request.method == 'POST' and request.form["selectday"]:
            selectday = request.form["selectday"]
            path = "json/" + selectday
            selectlist = readJson(path)
            return render_template("index.html", dictList=selectlist, days=getfilesname("json/"))
        else:
            return render_template("index.html", dictList=dictList, days=getfilesname("json/"))


if __name__ == "__main__":
    app.run()
