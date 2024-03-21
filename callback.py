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

def call_back_info(wh_url, chat_id):
    now_time = datetime.datetime.now()
    now_time_str = now_time.strftime("%Y-%m-%d %H:%M:%S")
    message_text = f'🔞New list: {now_time_str}'
    with open('./srct/miss.txt', 'r', encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            parts = line.split(',')
            if 'genre' in line:
                channel_genre = parts[0].strip()
                message_text += f'\n\n📬from: {channel_genre}\n'
            else:
                m3u_name = parts[0].strip()
                if len(m3u_name) > 20:
                    m3u_name = m3u_name[:18] + '……'
                message_text += f'\n🔸{m3u_name}'
    params = {
        "chat_id": chat_id,
        "parse_mode": "markdown",
        "text": message_text
    }

    page = SessionPage(timeout=5)
    page.post(url=wh_url, params=params)
    code_info = page.response
    re_code = code_info.status_code
    if re_code == 200:
        print('=====回复发送成功=====')
    else:
        print('=====回复发送失败(状态码: %s)=====' % re_code)

def call_back_cllect(wh_url, chat_id, juger, keywords, aord):
    if juger and juger == 'True':
        j = '成功'
    else:
        j = '失败'

    if '&' in keywords:
        keywords = keywords.replace('&', ', ')
    if aord == 'add':
        p = '添加'
    elif aord == 'del':
        p = '删除'
    now_time = datetime.datetime.now()
    now_time_str = now_time.strftime("%Y-%m-%d %H:%M:%S")
    message_text = (
        f'💼收藏夹: {now_time_str}\n'
        f'\n🔸您{p}{keywords}*{j}*'
        )
    params = {
        "chat_id": chat_id,
        "parse_mode": "markdown",
        "text": message_text
    }

    page = SessionPage(timeout=5)
    page.post(url=wh_url, params=params)
    code_info = page.response
    re_code = code_info.status_code
    if re_code == 200:
        print('=====回复发送成功=====')
    else:
        print('=====回复发送失败(状态码: %s)=====' % re_code)

if __name__ == '__main__':
    wh_url = os.environ.get("WH_URL", "")
    chat_id = os.environ.get("CHAT_ID", "")
    call_back_info(wh_url, chat_id)

