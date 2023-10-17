#!/usr/bin/env python
# coding:utf-8
""" 
@author: nivic ybyang7
@license: Apache Licence 
@file: down
@time: 2023/09/27
@contact: ybyang7@iflytek.com
@site:  
@software: PyCharm 

# code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.
              ┏┓      ┏┓
            ┏┛┻━━━┛┻┓
            ┃      ☃      ┃
            ┃  ┳┛  ┗┳  ┃
            ┃      ┻      ┃
            ┗━┓      ┏━┛
                ┃      ┗━━━┓
                ┃  神兽保佑    ┣┓
                ┃　永无BUG！   ┏┛
                ┗┓┓┏━┳┓┏┛
                  ┃┫┫  ┃┫┫
                  ┗┻┛  ┗┻┛ 
"""

#  Copyright (c) 2022. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.
import json

import requests
url = "https://datasets-server.huggingface.co/rows?dataset=erhwenkuo%2Fopenorca-chinese-zhtw&config=default&split=train&offset={index}&limit=100"
from zhconv import convert

def run():
    for i in  range(10):
        wurl = url.format(index=str(i))
        res = requests.get(wurl)
        with open(f"test_{i}.json","wb") as f:
            f.write(res.content)
            f.close()

def pasrs():
    out =  open(f'merged_cn.jsonl', 'w', encoding='utf-8')
    data = {'instruction': '', 'input': '', 'output': ''}
    for i in range(10):

        with open(f"test_{i}.json","rb") as f:
            c = json.load(f)
            for rrow in c['rows']:
                row = rrow['row']
                data['instruction'] = convert(row['system_prompt'], 'zh-hans')
                data['input'] =   convert(row['question'], 'zh-hans')
                # data['input'] = '选项为:\n' + 'A.' + row['A'] + '\n' + 'B.' + row['B'] + '\n' + 'C.' + row[
                #     'C'] + '\n' + 'D.' + row[
                #                     'D'] + '\n'
                if 'explanation' in row:
                    data['output'] = row['response'] + '\n' + row['explanation']
                else:
                    data['output'] =  convert(row['response'], 'zh-hans')
                out.write(json.dumps(data, ensure_ascii=False) + '\n')
    out.close()
if __name__ == '__main__':
    pasrs()