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

def main(wh_url, chat_id, proxy_url, lua_url):
    # 从 stdin 中读取 payload
    payload = json.loads(sys.stdin.read())

    # 检查是否有 script 字段
    if "script" not in payload:
        print("No script field in payload.")
        sys.exit(1)

    keywords = payload["script"]
    # 根据 keywords 来执行命令
    if keywords == "miss":
        miss_main(proxy_url, wh_url, chat_id)
        
    elif keywords == "lives":
        shows(wh_url, chat_id, lua_url)
    else:
        print("Invalid keywords option.")

if __name__ == "__main__":
    wh_url = os.environ.get("WH_URL", "")
    chat_id = os.environ.get("CHAT_ID", "")
    lua_url = os.environ.get("LUA_RUL", "")
    proxy_url = os.environ.get("PROXY_URL", "")
    main(wh_url, chat_id, proxy_url, lua_url)

