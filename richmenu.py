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



headers = {"Authorization":"Bearer b+0MFLF5nMtaQmOU+xRj34thghpJOgcxX5bosFAdRScyP5gHdjzWM3ojFM76bbC7kcvPgU5KXgngWA4DLVVcwxO6R90vmV9+Mt7bN2Y0wF3cwpW14NmVrwySo336EBv3wQ0k1yeMabpFu22akoERrwdB04t89/1O/w1cDnyilFU","Content-Type":"application/json"}

body = {
    "size": {"width": 2500, "height": 1686},
    "selected": "true",
    "name": "Controller",
    "chatBarText": "選擇項目",
    "areas":[
        {
          "bounds": {"x": 0, "y": 0, "width": 833, "height": 843},
          "action": {"type": "message", "text": "吃飽了嗎"}
        },
        {
          "bounds": {"x": 833, "y": 0, "width": 833, "height": 843},
          "action": {"type": "message", "text": "天氣 左營"}
        },
        {
          "bounds": {"x": 1666, "y": 0, "width": 833, "height": 843},
          "action": {"type": "message", "text": "雨量 左營"}
        },
        {
          "bounds": {"x": 0, "y": 843, "width": 833, "height": 843},
          "action": {"type": "message", "text": "id"}
        },
        {
          "bounds": {"x": 833, "y": 843, "width": 833, "height": 843},
          "action": {"type": "message", "text": "水位"}
        },
        {
          "bounds": {"x": 1666, "y": 843, "width": 833, "height": 843},
          "action": {"type": "message", "text": "hi"}
        }
    ]
  }

idlist=[]
req = requests.request('POST', 'https://api.line.me/v2/bot/richmenu', 
                           headers=headers,data=json.dumps(body).encode('utf-8'))

r = req.text.split(':')
r = r[1].split('"')
idlist.append(r[1])

with open(os.path.join('img', 'testjpg.jpg'), 'rb') as f:
    line_bot_api.set_rich_menu_image(idlist[0], "image/jpeg", f)

req = requests.request('POST', 'https://api.line.me/v2/bot/user/all/richmenu/' + idlist[0], 
                        headers=headers)

print(idlist[0], 'count = 0, filename = testjpg.jpg') 
print(req.text)


# idlist=[]
# count = 0 

# for file in os.listdir('img'):  
#     if file.endswith('.jpg'):
#         req = requests.request('POST', 'https://api.line.me/v2/bot/richmenu', 
#                            headers=headers,data=json.dumps(body).encode('utf-8'))

#         r = req.text.split(':')
#         r = r[1].split('"')
#         idlist.append(r[1])        
       
        
#         with open(os.path.join('img', file), 'rb') as f:
#             line_bot_api.set_rich_menu_image(idlist[count], "image/jpeg", f)

#         req = requests.request('POST', 'https://api.line.me/v2/bot/user/all/richmenu/' + idlist[count], 
#                        headers=headers)

#         print(idlist[count], "count = ", count, 'filename = ', file )    
#         count += 1



# print(req.text)
