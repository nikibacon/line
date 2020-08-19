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

from models import replymsg, googleimg, wether

app = Flask(__name__)

# LINE 聊天機器人的基本資料
config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))

@app.route("/")
def home():
    return render_template("home.html")


# 接收 LINE 的資訊
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'



# headers = {"Authorization":"Bearer b+0MFLF5nMtaQmOU+xRj34thghpJOgcxX5bosFAdRScyP5gHdjzWM3ojFM76bbC7kcvPgU5KXgngWA4DLVVcwxO6R90vmV9+Mt7bN2Y0wF3cwpW14NmVrwySo336EBv3wQ0k1yeMabpFu22akoERrwdB04t89/1O/w1cDnyilFU","Content-Type":"application/json"}

# body = {
#     "size": {"width": 2500, "height": 1686},
#     "selected": "true",
#     "name": "Controller",
#     "chatBarText": "Controller",
#     "areas":[
#         {
#           "bounds": {"x": 551, "y": 325, "width": 321, "height": 321},
#           "action": {"type": "message", "text": "up"}
#         },
#         {
#           "bounds": {"x": 876, "y": 651, "width": 321, "height": 321},
#           "action": {"type": "message", "text": "right"}
#         },
#         {
#           "bounds": {"x": 551, "y": 972, "width": 321, "height": 321},
#           "action": {"type": "message", "text": "down"}
#         },
#         {
#           "bounds": {"x": 225, "y": 651, "width": 321, "height": 321},
#           "action": {"type": "message", "text": "left"}
#         },
#         {
#           "bounds": {"x": 1433, "y": 657, "width": 367, "height": 367},
#           "action": {"type": "message", "text": "btn b"}
#         },
#         {
#           "bounds": {"x": 1907, "y": 657, "width": 367, "height": 367},
#           "action": {"type": "message", "text": "btn a"}
#         }
#     ]
#   }

# req = requests.request('POST', 'https://api.line.me/v2/bot/richmenu', 
#                        headers=headers,data=json.dumps(body).encode('utf-8'))

# print(req.text)


# for file in os.listdir('img'):  
#     if file.endswith('.jpg'):
#         with open(os.path.join('img', file), 'rb') as f:
#             line_bot_api.set_rich_menu_image("richmenu-c0171d9ce96960d99989ddf29887b7ea", "image/jpeg", f)

# req = requests.request('POST', 'https://api.line.me/v2/bot/user/all/richmenu/richmenu-c0171d9ce96960d99989ddf29887b7ea', 
#                        headers=headers)

# print(req.text)



@handler.add(MessageEvent, message=StickerMessage)
def reply_sticekr_message(event):

    if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":

        sticker_message = StickerSendMessage(
            package_id = '1',
            sticker_id = f'{str(random.randint(401, 430))}'
        )

        line_bot_api.reply_message(
            event.reply_token,
            sticker_message
        )


    


@handler.add(MessageEvent, message=TextMessage)
def reply_text_message(event):

    if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":

        reply = False

        #回天氣
        if not reply:
            reply = wether.weather_message(event)

        if not reply:
            reply = replymsg.hi_message(event)

        if not reply:
            reply = googleimg.google_img(event)


 



if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)