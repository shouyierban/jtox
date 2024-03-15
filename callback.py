# !/usr/bin/python3
# -*- encoding: utf-8 -*-
# @File    :   callback.py
# @Time    :   2024/03/14 22:23:59
# @Author  :   Plate • Lets 
# @Version :   Pythin 3.10.0
# @Contact :   Plate_Lets@gmail.com
# @License :   (C)Copyright 2022-2024
# @Desc    :   None

# ----here put the import lib----
from DrissionPage import SessionPage
import os
import datetime
import requests

def call_back_info(wh_url, chat_id):
    now_time = datetime.datetime.now()
    now_time_str = now_time.strftime("%Y-%m-%d %H:%M:%S")
    message_text = f'🔞New list: {now_time_str}\n'
    m = 1
    with open('./srct/miss.txt', 'r', encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            parts = line.split(',')
            if 'genre' in line:
                channel_genre = parts[0].strip()
                message_text += '📬from:' + channel_genre + '\n'
            else:
                m3u_name = parts[0].strip()
                message_text += f'{m}: {m3u_name}'
                m += 1
    params = {
        "chat_id": chat_id,
        "parse_mode": "markdown",
        "text": message_text
    }

    page = SessionPage(timeout=5)
    page.post(url=wh_url, params=params)
    code_info = page.response
    re_code = code_info.status_code
    # resp = requests.post(url=wh_url, params=params)
    # re_code = resp.status_code
    if re_code == 200:
        print('=====回复发送成功=====')
    else:
        print('=====回复发送失败(状态码: %s)=====' % re_code)

if __name__ == '__main__':
    wh_url = os.environ.get("WH_URL", "")
    chat_id = os.environ.get("CHAT_ID", "")
    call_back_info(wh_url, chat_id)

