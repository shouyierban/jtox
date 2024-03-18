# !/usr/bin/python3
# -*- encoding: utf-8 -*-
# @File    :   miss.py
# @Time    :   2024/03/14 22:24:21
# @Author  :   Plate • Lets 
# @Version :   Pythin 3.10.0
# @Contact :   Plate_Lets@gmail.com
# @License :   (C)Copyright 2022-2024
# @Desc    :   None

# ----here put the import lib----

from DrissionPage import SessionPage
import random
import re
import os
from callback import call_back_info

def convert_to_m3u(tv_list):
    # 获取组别
    channel_genre_list = []
    for line in tv_list:
        line = line.strip()
        parts = line.split(',')
        channel_genre_name = parts[2].replace('#genre#=', '').strip()
        channel_genre_list.append(channel_genre_name)
    channel_genre_list = list(set(channel_genre_list))
    # 分组写入
    tvbox_content = ''
    for channel_genre in channel_genre_list:
        tvbox_content += f'{channel_genre},#genre#\n'
        for text in tv_list:
            text = text.strip()
            parts = text.split(',')
            channel_name = parts[0].strip()
            channel_url = parts[1].strip()
            channel_group = parts[2].replace('#genre#=', '').strip()
            if channel_group == channel_genre:
                tvbox_content += f'{channel_name},{channel_url}\n'
    return tvbox_content

def get_addr(proxy_url, url_page):
    vid_url = proxy_url + url_page
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    }
    page = SessionPage(timeout=5)
    page.get(url=vid_url, headers=headers)
    text_list = page.eles('xpath://script/text()')
    text = ''
    for text_un in text_list:
        text += str(text_un)
    code_alllist = re.compile(r'm3u8\|(.*?)\|com')
    rate_list = re.compile(r'video\|(.*?)\|source')

    code_data = code_alllist.search(text)
    rate_data = rate_list.search(text)
    if code_data and rate_data:
        code_text = code_data.group(1)
        code_text = code_text.replace('|', '-')
        code_list = code_text.split('-')
        code_list.reverse()
        f_code = '-'.join(code_list)
        f_rate = rate_data.group(1)
        url = 'https://surrit.com/' + f_code + '/' + f_rate + '/video.m3u8'
        return url

def get_list(proxy_url):
    data_list = []
    for _ in range(8):
        tokey_index = random.randint(150, 210)
        high_index = random.randint(10, 215)
        base_url = proxy_url
        tokey_url = base_url + 'https://missav.com/dm16/tokyohot?page={0}'.format(tokey_index)
        high_url = base_url + 'https://missav.com/search/%E9%AB%98%E5%A6%B9?sort=released_at&page={0}'.format(high_index)

        url_list = [tokey_url, high_url]
        for url in url_list:
            headers = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
            }
            page = SessionPage(timeout=5)
            page.get(url=url, headers=headers)

            for _ in range(2):
                num_vid = random.randint(1, 11)        
                name_list = page.eles('xpath://div[contains(@class,"my-2")]/a/text()')[num_vid].strip()
                name_list = name_list.replace(",", "-")
                url_list = page.eles('xpath://div[contains(@class,"my-2")]/a/@href')[num_vid].strip()
                
                if url_list:
                    if url == tokey_url:
                        f_url =  get_addr(base_url, url_list) + ',#genre#=东京'
                    elif url == high_url:
                        f_url =  get_addr(base_url, url_list) + ',#genre#=高妹'
                    data_list.append(f'{name_list}, {f_url}')
                    # print(name_list + ',' + f_url)          
    return data_list

def save_data(m3u_content, filename):
    # 将结果保存到文本文件
    with open(filename, "w", encoding="utf-8") as file:
        file.write(m3u_content)

def miss_main(proxy_url, wh_url, chat_id):
    print('======txt更新开始=======')
    tv_list = get_list(proxy_url)
    box = convert_to_m3u(tv_list)
    # 保存
    save_data(box, "./srct/miss.txt")
    print('======txt更新结束=======')
    call_back_info(wh_url, chat_id)

if __name__ == '__main__':
    wh_url = os.environ.get("WH_URL", "")
    chat_id = os.environ.get("CHAT_ID", "")
    proxy_url = os.environ.get("PROXY_URL", "")
    miss_main(proxy_url,)
