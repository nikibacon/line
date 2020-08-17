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



@handler.add(MessageEvent, message=TextMessage)
def google_isch(event):
    
    if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
        msg = event.message.text
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
        else:

        # 找圖
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
                    # if '貼圖' in msg:
                    #     sticker_message = StickerSendMessage(
                    #     package_id=f'{str(random.randint(1, 3))}',
                    #     sticker_id=f'{str(random.randint(1, 250))}'
                    # )
                    #     line_bot_api.reply_message(
                    #         event.reply_token,
                    #         sticker_message)
                    #     return
                   

                    



@handler.add(MessageEvent, message=StickerMessage)
def sticker_reply(event):

    if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":

        sticker_message = StickerSendMessage(
        package_id = f'{str(random.randint(1, 2))}',
        sticker_id = f'{str(random.randint(1, 120))}'
        )

        line_bot_api.reply_message(
            event.reply_token,
            sticker_message
        )


if __name__ == "__main__":
    app.run()