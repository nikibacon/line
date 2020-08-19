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



def sticker_reply(event):

    try:

        sticker_message = StickerSendMessage(
        package_id = '1',
        sticker_id = f'{str(random.randint(401, 430))}'
        )

        line_bot_api.reply_message(
            event.reply_token,
            sticker_message
        )

        return True
    
    except:
        return False





def hi_message(event):

    msg = event.message.text

    try:
        if msg in ['hi', 'Hi', '嗨']:
            r = 'hi,最近過得如何?'
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=r)
            )
        elif '吃飯了嗎' in msg:
            r = '還沒, 你勒?'
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=r)
            )
        elif '你是誰' in msg:
            r = '我是你的機器人好朋友'
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=r)
            )
        elif '訂位' in msg:
            r = '你想訂位,是嗎?'
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=r)
            )
        elif 'id' in msg:
            r = '這是你的line ID:', str(event.source.user_id)
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=r)
            )
    
        return True
    
    except:
        return False
