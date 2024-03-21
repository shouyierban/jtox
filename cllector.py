# !/usr/bin/python3
# -*- encoding: utf-8 -*-
# @File    :   bak.py
# @Time    :   2024/03/21 13:39:45
# @Author  :   Plate • Lets 
# @Version :   Pythin 3.10.0
# @Contact :   Plate_Lets@gmail.com
# @License :   (C)Copyright 2022-2024
# @Desc    :   None

# ----here put the import lib----
class Cllector (object):
    def __init__ (self, keyword):
        self.keyword = keyword
        
    def bak_add(self):
        keyword_list = self.bak_keyword()
        for keyword in keyword_list:
            # 将关键词转换为小写
            keyword_lower = keyword.lower()

            # 用来跟踪关键词是否已经出现过的变量
            keyword_found = False

            # 读取已有的输出文件内容，将每行内容存储到一个集合中
            existing_lines = set()
            try:
                with open('./srct/bak.txt', "r", encoding="utf-8") as existing_file:
                    for line in existing_file:
                        existing_lines.add(line.strip())
            except FileNotFoundError:
                # 如果输出文件不存在，则不需要处理已有内容
                pass

            # 逐行读取文件，并将第一次包含关键词且不在输出文件中的行写入到输出文件中
            with open('./srct/miss.txt', "r", encoding="utf-8") as input_f:
                with open('./srct/bak.txt', "a", encoding="utf-8") as output_f:
                    for line in input_f:
                        # 将每行文本也转换为小写进行比较
                        if not keyword_found and keyword_lower in line.lower() and line.strip() not in existing_lines:
                            output_f.write(line)
                            keyword_found = True  # 找到关键词后将标志设为True，避免后续再次写入
        return 'True'

    def bak_del(self):
        keyword_list = self.bak_keyword()
        for keyword in keyword_list:
            # 将关键词转换为小写
            keyword_lower = keyword.lower()

            # 读取已有的输出文件内容，将每行内容存储到一个集合中
            existing_lines = set()
            try:
                with open('./srct/bak.txt', "r", encoding="utf-8") as existing_file:
                    for line in existing_file:
                        # 如果不包含关键词，则添加到集合中
                        if keyword_lower not in line.lower():
                            existing_lines.add(line.strip())
            except FileNotFoundError:
                # 如果输出文件不存在，则不需要处理已有内容
                pass

            # 将不包含关键词的行重新写入到输出文件中
            with open('./srct/bak.txt', "w", encoding="utf-8") as output_f:
                for line in existing_lines:
                    output_f.write(line + "\n")
        return 'True'

    def bak_keyword(self):
        keyword_list = []
        if '&' in self.keyword:
            bak_list = self.keyword.split('&')
            keyword_list.extend(bak_list)
        else:
            keyword_list.append(self.keyword)
        return keyword_list

if __name__ == '__main__':
    coll = Cllector("n0112&n0497")
    # coll.bak_add()
    coll.bak_del()
