from __future__ import unicode_literals
import os

# 增加了 render_template
from flask import Flask, request, abort, render_template

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, StickerSendMessage, StickerMessage

import configparser

import urllib
import re
import random

import requests
import json


app = Flask(__name__)

# LINE 聊天機器人的基本資料
config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))

def getweather(station):
    end_point = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/O-A0001-001?Authorization=rdec-key-123-45678-011121314"

    data = requests.get(end_point).json()
    data = data["records"]["location"]

    target_station = "not found"
    for item in data:
        if item["locationName"] == str(station):
            target_station = item
    return target_station




def makeaqi(station):
    end_point = "http://opendata.epa.gov.tw/webapi/api/rest/datastore/355000000I-000259?filters=SiteName eq '" + \
        station + "'&sort=SiteName&offset=0&limit=1000"

    data = requests.get(end_point)
    aqimsg = ""

    if data.status_code == 500:
        return "無 AQI 資料"
    else:
        aqidata = data.json()['result']['records'][0]
        aqimsg += "AQI = " + aqidata['AQI'] + "\n"
        aqimsg += "PM2.5 = " + aqidata["PM2.5"] + " μg/m3\n"
        aqimsg += "PM10 = " + aqidata["PM10"] + " μg/m3\n"
        aqimsg += "空品：" + aqidata["Status"]
        return aqimsg

def makeweather(station):
    weatherdata = getweather(station)
    if weatherdata == "not found":
        return False

    weatherdata = weatherdata['weatherElement']
    msg = "天氣報告 - " + station
    msg += "\n\n氣溫 = " + weatherdata[3]['elementValue'] + "℃\n"
    msg += "濕度 = " + \
        str(float(weatherdata[4]['elementValue']) * 100) + "% RH\n"

    msg += makeaqi(station)
    return msg


def makerailfall(station):
    result = requests.get(
        "https://opendata.cwb.gov.tw/api/v1/rest/datastore/O-A0002-001?Authorization=rdec-key-123-45678-011121314")
    msg = "降雨報告 - " + station + "\n\n"

    if(result.status_code != 200):
        return "雨量資料讀取失敗"
    else:
        railfalldata = result.json()
        for item in railfalldata["records"]["location"]:
            if station in item["locationName"]:
                msg += "目前雨量：" + \
                    item["weatherElement"][7]["elementValue"] + "mm\n"
                if item["weatherElement"][3]["elementValue"] == "-998.00":
                    msg += "三小時雨量：0.00mm\n"
                else:
                    msg += "三小時雨量：" + \
                        item["weatherElement"][3]["elementValue"] + "mm\n"
                msg += "日雨量：" + \
                    item["weatherElement"][6]["elementValue"] + "mm\n"
                return msg
        return "沒有這個測站啦"


def waterlevel():
    
    msg = ''
    for i in range(1, 7):
        r = requests.get('http://59.127.202.74:8080/challenger/getval.jsp?sql=' + str(i) + '@Currenty_Display_Hi')

        msg += '台西'+ str(i) + '號水位:' + r.text + '%\n'

    return msg
    


def weather_message(event):

    
    cmd = event.message.text.split(" ")
    
    if cmd[0] == "天氣":
        station = cmd[1]
        weathermsg = makeweather(station)

        if not weathermsg:
            weathermsg = "沒這個氣象站啦"

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=weathermsg))
        return True
    else:
        return False 

    if cmd[0] == "雨量":
        station = cmd[1]
        railfallmsg = makerailfall(station)

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=railfallmsg))
        return True
    else:
        return False

    if cmd[0] == '水位':
        waterlevelmsg = waterlevel()

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=waterlevelmsg))
        return True
    else:
        return False
        
    

         