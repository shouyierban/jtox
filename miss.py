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
from urllib.parse import quote
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
    
def pig_list(pl_url):
    base_url = 'https://pigav.com/%e5%9c%8b%e7%94%a2av%e7%b7%9a%e4%b8%8a%e7%9c%8b'
    l_script = f'''function main(splash, args)
    assert(splash:go("{base_url}"))
    assert(splash:wait(1))
    local data_list = {{}}
    for p = 1, 6 do
        for i = 1, 2 do
        local ram_num = math.random(1,20)
        local page_list = splash:select('#post-514045 > div > div > section > div > div > div > div > div > section > div > div > article:nth-child(' .. ram_num .. ') > div.content > div > h2 > a'):text()
        local page_url = splash:select('#post-514045 > div > div > section > div > div > div > div > div > section > div > div > article:nth-child(' .. ram_num .. ') > div.content > div > h2 > a'):info()["attributes"]["href"]
        local data_info = {{
            name = page_list,
            purl = page_url
        }}
        table.insert(data_list, data_info)
        end
        local click_num = math.random(1,30)
        for j = 1, click_num do
        local next_bt = splash:select('#post-514045 > div > div > section > div > div > div > div > div > section > div > nav > a.next.page-numbers')
        if next_bt then
            next_bt: mouse_click()
        else
            break
        end
        end
    end
    
    return {{
        data = data_list
    }}
    end
    '''
    pigurl = pl_url + f'lua_source={quote(l_script)}'
    page = SessionPage(timeout=35)
    page.get(url=pigurl)
    result = page.json
    return result

def pig_m3u(purl):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    }
    page = SessionPage()
    page.get(url=purl, headers=headers)
    code_info = page.response
    # print(code_info.status_code)
    pig_script = page.eles("xpath://script/text()")
    elem_list = ''
    for elem in pig_script:
        elem = str(elem)
        elem_list += elem
    elem_list = elem_list[-4000:-1000]
    pattern = r"videojs\('video-(.*?)'"
    code_data = re.search(pattern, elem_list)
    ex_value = code_data.group(1)
    # print(ex_value)

    # 获取shadow_root
    # pig_shadow_root = page.ele(f'css:#video-{ex_value}').html
    pig_shadow_root = page.ele(f'css:#video-{ex_value}').inner_html
    pig_pattern = r'src="(.*?)"'
    pig_matcher = re.search(pig_pattern, pig_shadow_root)
    pig_url = pig_matcher.group(1)
    return pig_url
    
def z_list(proxy, page):
    page_num = page
    url =  proxy + 'https://18av.mm-cg.com/zh/uncensored_makersr/29/Tokyo%20Hot%20(%E6%9D%B1%E4%BA%AC%E7%86%B1)/{0}.html'.format(page_num)
    page = SessionPage(timeout=10)
    page.get(url)
    resp = page.response
    # print('zp:' + str(resp.status_code))
    z_name = page.eles('xpath://div[@class="post video_9s"]/div/h3/a/text()')
    z_url = page.eles('xpath://div[@class="post video_9s"]/div/h3/a/@href')
    z_data = []
    for _ in range(0, 3):
        vio_mun = random.randint(1, 15)
        fz_name = z_name[vio_mun]
        pz_url = proxy + z_url[vio_mun]
        page.get(pz_url)
        z_resp = page.response
        # print('zfp:' + str(z_resp.status_code))

        z_code = page.eles("xpath://script/text()")
        z_code_str = ''
        for z_code_text in z_code:
            z_code_str += str(z_code_text)
        z_code_str = z_code_str[-3000:]
        # print(z_code)
        pattern = r'id=880_*_(\w+)"'
        matche_code = re.findall(pattern, z_code_str)
        if matche_code:
            fz_code = matche_code[0].split('_')
            # print(fz_code)
        else:
            print("fz_code未匹配")

        fz_code_combin = f'{fz_code[0]}' + '/' + f'{fz_code[1]}' + '/' + f'{fz_code[1]}'
        fz_url = 'https://v.imgstream2.com/' + fz_code_combin + '.m3u8'
        k_name, v_zurl = fz_name, fz_url
        z_dict = {k_name: v_zurl}
        z_data.append(z_dict)
        # print(z_data)
    return z_data

def jrate():
    page_num = random.randint(0, 58)
    r_url = 'https://www.javrate.com/menu/uncensored/5-2-{0}'.format(page_num)

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
    }

    page = SessionPage(timeout=8)
    page.get(url=r_url, headers=headers)
    r_name = page.eles('xpath://div[contains(@class, "col-md-4")]/div[2]/a/text()')
    page_url = page.eles('t:div@@class:col-md-4')
    data = []
    for _ in range(1):
        vadio_num = random.randint(1, 19)
        f_name = r_name[vadio_num].replace(';', '').strip()
        f_name = f_name.replace(':', '')
        page_url_full = page_url[vadio_num].ele("t:div@@class:text-truncate")('t:a').link
        page.get(url=page_url_full, headers=headers)
        scripts_text = page.eles("xpath://script/text()")
        elem_list = ''
        for elem in scripts_text:
            elem = str(elem)
            elem_list += elem
        elem_list = elem_list[-1800:-600]
        print(elem_list)    
        pattern = re.compile(r"url: '(.*.m3u8)',")
        match_url = pattern.search(elem_list)
        if match_url:
            fr_url = match_url.group(1)
        else:
            fr_url = None
        key, value = f_name, fr_url
        r_dict = {key: value}
        data.append(r_dict)
    print(data + '\n' + '++++++++++++++++++++++++++++')
    return data

def get_list(proxy_url, pl_url, de_url):
    data_list = []
    # try:
    #     for _ in range(2):
    #         tokey_index = random.randint(150, 210)
    #         high_index = random.randint(10, 215)
    #         base_url = proxy_url
    #         tokey_url = base_url + 'https://missav.com/dm16/tokyohot?page={0}'.format(tokey_index)
    #         high_url = base_url + 'https://missav.com/search/%E9%AB%98%E5%A6%B9?sort=released_at&page={0}'.format(high_index)

    #         url_list = [tokey_url, high_url]
    #         for url in url_list:
    #             headers = {
    #                 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    #             }
    #             page = SessionPage(timeout=5)
    #             page.get(url=url, headers=headers)

    #             for _ in range(2):
    #                 num_vid = random.randint(1, 11)        
    #                 name_list = page.eles('xpath://div[contains(@class,"my-2")]/a/text()')[num_vid].strip()
    #                 name_list = name_list.replace(",", "-")
    #                 url_list = page.eles('xpath://div[contains(@class,"my-2")]/a/@href')[num_vid].strip()
                    
    #                 if url_list:
    #                     if url == tokey_url:
    #                         f_url =  get_addr(base_url, url_list) + ',#genre#=东京'
    #                     elif url == high_url:
    #                         f_url =  get_addr(base_url, url_list) + ',#genre#=高妹'
    #                     data_list.append(f'{name_list}, {f_url}')
    #                     # print(name_list + ',' + f_url)
    # except Exception as e:
    #     print('miss错误' + e)

    # # 添加pig列表============================================
    # try:
    #     pig_json = pig_list(pl_url)
    #     if 'data' in pig_json:
    #         full_data = pig_json['data']
    #         # 解析JSON文件，获取name和url字段
    #         for key, item in full_data.items():
    #             if isinstance(item, dict):
    #                 pig_name = item.get('name')
    #                 pig_url = item.get('purl')
    #                 full_pig_url = proxy_url + pig_url
    #                 f_pig_url = pig_m3u(full_pig_url)
    #                 f_pig_url = f_pig_url + ',#genre#=PIG-国产'
    #                 data_list.append(f'{pig_name}, {f_pig_url}')
    #                 # print(pig_name + ',' + f_pig_url + '\n')
    # except Exception as e:
    #     print('pig错误' + e)

    # # 添加18tv===============================================
    # try:
    #     for _ in range(4):
    #         z_num = random.randint(1, 75)
    #         z_data = z_list(de_url, z_num)
    #         for dictionary in z_data:
    #             for key, value in dictionary.items():
    #                 z_name = key
    #                 z_url = value
    #                 z_url = z_url + ',#genre#=Z-东京'
    #                 data_list.append(f'{z_name}, {z_url}')
    # except Exception as e:
    #     print('z错误:%s'%e)

    # 添加jrate================================================
    try:
        for _ in range(1):
            j_data = jrate()
            print(j_data)
            for dictionary in j_data:
                for key, value in dictionary.items():
                    j_name = key
                    print(j_name + '\n')
                    j_url = value.scrip()
                    j_url = z_url + ',#genre#=Jrate'
                    data_list.append(f'{j_name}, {j_url}')
    except Exception as e:
        print('j错误:%s'%e)

    return data_list

def save_data(m3u_content, filename):
    # 将结果保存到文本文件
    with open(filename, "w", encoding="utf-8") as file:
        file.write(m3u_content)

def miss_main(proxy_url, wh_url, chat_id, pl_url, de_url):
    print('======txt更新开始=======')
    tv_list = get_list(proxy_url, pl_url, de_url)
    box = convert_to_m3u(tv_list)
    # 保存
    save_data(box, "./srct/miss.txt")
    print('======txt更新结束=======')
    call_back_info(wh_url, chat_id)

if __name__ == '__main__':
    wh_url = os.environ.get("WH_URL", "")
    chat_id = os.environ.get("CHAT_ID", "")
    proxy_url = os.environ.get("PROXY_URL", "")
    pl_url = os.environ.get("PL_URL", "")
    miss_main(proxy_url,)
