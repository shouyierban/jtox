# !/usr/bin/python3
# -*- encoding: utf-8 -*-
# @File    :   iptv.py
# @Time    :   2024/03/02 17:12:22
# @Author  :   Plate • Lets 
# @Version :   Pythin 3.10.0
# @Contact :   Plate_Lets@gmail.com
# @License :   (C)Copyright 2022-2024
# @Desc    :   None

# ----here put the import lib----
import requests
from urllib.parse import quote
import json
import os
import datetime

def convert_to_m3u(tv_list):
    # 构建m3u格式的内容
    m3u_content = '#EXTM3U x-tvg-url="http://epg.51zmt.top:8000/e.xml"\n'
        
    for line in tv_list:
        line = line.strip()
        
        # 解析频道名称和链接以及分类
        parts = line.split(',')
        channel_name = parts[0].strip()
        channel_url = parts[1].strip()
        if 'genre' in line:
            channel_genre = parts[2].replace('#genre#=', '').strip()
        else:
            channel_genre = 'Other'
        
        # 构建m3u格式的频道条目，将频道分类名称写入group-title字段
        tvg_logo = f'https://live.zhoujie218.top/taibiao/{channel_name}.png'
        m3u_entry = f'#EXTINF:-1 group-title="{channel_genre}" tvg-name="{channel_name}" tvg-logo="{tvg_logo}",{channel_name}\n{channel_url}\n'
        m3u_content += m3u_entry  
    # print(f'转换文件成功！')
    return m3u_content

def simple_out(json_data):
    data_list = []
    if 'result' in json_data:
        full_data = json_data['result']

        # 解析JSON文件，获取name和url字段
        for key, item in full_data.items():
            if isinstance(item, dict):
                name = item.get('name')
                url = item.get('addr')

                if name and url:
                    # 小写转大写
                    name = name.upper()
                    # 删除特定文字
                    name = name.replace("中央", "CCTV")
                    name = name.replace("高清", "")
                    name = name.replace("标清", "")
                    name = name.replace("频道", "")
                    name = name.replace("4K", "_4K")
                    name = name.replace("HD", "_HD")
                    name = name.replace("-", "")
                    name = name.replace(" ", "")
                    name = name.replace("PLUS", "+")
                    name = name.replace("(", "")
                    name = name.replace(")", "")

                    name = name.replace("CCTV1综合", "CCTV1")
                    name = name.replace("CCTV2财经", "CCTV2")
                    name = name.replace("CCTV3综艺", "CCTV3")
                    name = name.replace("CCTV4国际", "CCTV4")
                    name = name.replace("CCTV5体育", "CCTV5")
                    name = name.replace("CCTV6电影", "CCTV6")
                    name = name.replace("CCTV7军事", "CCTV7")
                    name = name.replace("CCTV7军农", "CCTV7")
                    name = name.replace("CCTV8电视剧", "CCTV8")
                    name = name.replace("CCTV9记录", "CCTV9")
                    name = name.replace("CCTV9纪录", "CCTV9")
                    name = name.replace("CCTV10科教", "CCTV10")
                    name = name.replace("CCTV11戏曲", "CCTV11")
                    name = name.replace("CCTV12社会与法", "CCTV12")
                    name = name.replace("CCTV13新闻", "CCTV13")
                    name = name.replace("CCTV14少儿", "CCTV14")
                    name = name.replace("CCTV15音乐", "CCTV15")
                    name = name.replace("CCTV16奥林匹克", "CCTV16")

                    name = name.replace("CCTV17农业农村", "CCTV17")
                    name = name.replace("CCTV5+体育赛视", "CCTV5+")
                    name = name.replace("CCTV5+体育赛事", "CCTV5+")
                    name = name.replace("西班牙语", "西语")
                    name = name.replace("阿拉伯语", "阿语")

                    url = url.replace(" ", "")

                    if 'C' in name:
                        genre = '#genre#=CCTV'
                    else:
                        genre = '#genre#=Local'

                    data_list.append(f"{name},{url},{genre}")

    return data_list

def save_data(m3u_content, filename):
    # 将结果保存到文本文件
    with open(filename, "w", encoding="utf-8") as file:
        file.write(m3u_content)

def shows(wh_url, chat_id, lua_url):
    # wh_url = os.environ.get("WH_URL", "")
    # chat_id = os.environ.get("CHAT_ID", "")
    # prox_url = os.environ.get("LUA_RUL", "")
    # 读取 Lua 脚本文件
    with open('list.lua', 'r', encoding='utf-8') as file:
        lua_script = file.read()

    splash_url = lua_url + f'lua_source={quote(lua_script)}'
    # 发送请求
    resp = requests.get(splash_url,timeout=50)
    result = resp.text
    st_code = resp.status_code
    down_data = json.loads(result)
    # 整理格式
    tv_list = simple_out(down_data)
    m3u = convert_to_m3u(tv_list)
    # 保存
    save_data(m3u, "./srct/tvshows.m3u8")

    # 发送回复信息
    now_time = datetime.datetime.now()
    now_time_str = now_time.strftime("%Y-%m-%d %H:%M:%S")
    if st_code == 204:
        callback_message = (
            '🔊已经成功更新了iptv列表\n'
            f'🕣更新时间: {now_time_str}\n'
            )
    else:
        callback_message = (
            '❎iptv列表更新失败\n'
            f'🕣更新时间: {now_time_str}\n'
        )
    params = {
        "chat_id": chat_id,
        "parse_mode": "markdown",
        "text": callback_message
    }
    page = requests.post(url=wh_url, params=params)
    cb_code = page.status_code
    if cb_code == 200:
        print('=====发送成功=====')
    else:
        print('=====发送失败(状态码: %s)=====' % cb_code)
    
if __name__ == '__main__':
    wh_url = os.environ.get("WH_URL", "")
    chat_id = os.environ.get("CHAT_ID", "")
    lua_url = os.environ.get("LUA_RUL", "")
    shows(wh_url, chat_id, lua_url)
