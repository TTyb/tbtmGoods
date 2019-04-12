#!/usr/bin/python3.4
# -*- coding: utf-8 -*-


from flask import Flask, request, render_template
from tbtmGoods import *


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
        else:
            return []


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
    nowtime = time.strftime('%Y%m%d', time.localtime(time.time()))
    jsonPath = "json/" + nowtime
    dictList = readJson(jsonPath)
except:
    dictList = [
        {
            "标题": "",
            "原价": "",
            "折扣价": "",
            "销量": "",
            "图像URL": ""
        }
    ]

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    inter = 10
    if request.method == 'GET':
        pages = [x + 1 for x in
                 range((len(dictList) // inter) + 1 if len(dictList) % inter != 0 else len(dictList) // inter)]
        if len(dictList[:inter]):
            pages = []
        return render_template("index.html", dictList=dictList[:inter], pages=pages, nowlist=nowtime,
                               days=getfilesname("json/"))
    elif request.method == 'POST':
        search = request.form["search"]
        page = request.form["page"]
        if search and page:
            getJsonData(int(page), search)
            nowtm = time.strftime('%Y%m%d', time.localtime(time.time()))
            jsonPath = "json/" + nowtime
            newList = readJson(jsonPath)
            pages = [x + 1 for x in
                     range((len(newList) // inter) + 1 if len(newList) % inter != 0 else len(newList) // inter)]
            return render_template("index.html", dictList=newList[:inter], pages=pages, nowlist=nowtm,
                                   days=getfilesname("json/"))
        elif request.method == 'POST' and (request.form["selectday"] or request.form["nowlist"]):
            selectday = request.form["selectday"]
            if selectday == "":
                selectday = request.form["nowlist"]
            path = "json/" + selectday
            selectlist = readJson(path)
            pages = [x + 1 for x in range(
                (len(selectlist) // inter) + 1 if len(selectlist) % inter != 0 else len(selectlist) // inter)]
            if request.form["pg"]:
                pg = int(request.form["pg"])
                if pg == 1:
                    down = 0
                else:
                    down = (pg - 1) * 10 + 1
                up = down + inter
                nowlist = request.form["nowlist"]
                path = "json/" + nowlist
                selectlist = readJson(path)
                return render_template("index.html", dictList=selectlist[down:up], pages=pages, nowlist=nowlist,
                                       days=getfilesname("json/"))
            else:
                return render_template("index.html", dictList=selectlist[:inter], pages=pages, nowlist=selectday,
                                       days=getfilesname("json/"))
        else:
            return render_template("index.html", dictList=dictList, days=getfilesname("json/"))


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)
