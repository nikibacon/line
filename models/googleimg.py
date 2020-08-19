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


def google_img(event):


    try:
            q_string = {'tbm': 'isch', 'q': event.message.text}
            url = f"https://www.google.com/search?{urllib.parse.urlencode(q_string)}/"
            headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'}
                
            req = urllib.request.Request(url, headers = headers)
            conn = urllib.request.urlopen(req)
            
            print('fetch conn finish')
                
            pattern = 'img data-src="\S*"'
            img_list = []
                
            for match in re.finditer(pattern, str(conn.read())):
                img_list.append(match.group()[14:-1])
                    
            random_img_url = img_list[random.randint(0, len(img_list)+1)]
            print('fetch img url finish')
            print(random_img_url)
                        
            line_bot_api.reply_message(
                event.reply_token,
                ImageSendMessage(
                    original_content_url=random_img_url,
                    preview_image_url=random_img_url
                )
            )
            # 找不到圖就告訴我 user_id
    except:
                
        r = '我看不懂你在說什麼啦(嘟'
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=r)
        )

    return True
    
