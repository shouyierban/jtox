# !/usr/bin/python3
# -*- encoding: utf-8 -*-
# @File    :   app.py
# @Time    :   2024/03/15 13:06:15
# @Author  :   Plate • Lets 
# @Version :   Pythin 3.10.0
# @Contact :   Plate_Lets@gmail.com
# @License :   (C)Copyright 2022-2024
# @Desc    :   None

# ----here put the import lib----
from miss import miss_main
from show import shows
import os
import sys
import json

def main(de_url, tv_url, wh_url, chat_id, proxy_url, lua_url):
    event_path = os.getenv('GITHUB_EVENT_PATH')
    if not event_path:
        print("GITHUB_EVENT_PATH variable is not set.")
        exit(1)
    # 读取文件内容
    with open(event_path, 'r') as event_file:
        event_data = json.load(event_file)
    # 检查是否有 script 字段
    if 'client_payload' in event_data:
        client_payload = event_data['client_payload']
        if 'script' in client_payload:
            keywords = client_payload['script']
            # 根据 keywords 来执行命令
            if keywords == "miss":
                miss_main(proxy_url, wh_url, chat_id)
                
            elif keywords == "lives":
                shows(de_url, tv_url, lua_url, wh_url, chat_id)
            else:
                print("Invalid keywords option.")
        else:
            print("No 'script' found in client_payload.")
            sys.exit(1)
    else:
        print("No 'client_payload' found in event data.")
        sys.exit(1)

if __name__ == "__main__":
    wh_url = os.environ.get("WH_URL", "")
    chat_id = os.environ.get("CHAT_ID", "")
    lua_url = os.environ.get("LUA_RUL", "")
    proxy_url = os.environ.get("PROXY_URL", "")
    de_url = os.environ.get("DE_RUL", "")
    tv_url = os.environ.get("TV_RUL", "")
    main(de_url, tv_url, wh_url, chat_id, proxy_url, lua_url)

