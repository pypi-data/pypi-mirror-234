#!/usr/bin/env python
# coding:utf-8
""" 
@author: nivic ybyang7
@license: Apache Licence 
@file: generate
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
import  os
import pandas as pd

def make_instruct_ceval(base_dir='./csv', output_dir='./'):
    instruct_template = '请根据给定的文本，从以下四个选项中选择最佳答案。\n请注意，每个选项都可能包含正确答案的一部分信息，但并非全部。\n请仔细阅读每个选项，并结合文本内容进行判断。\n'
    for csv_file in os.listdir(base_dir):
        df = pd.read_excel(f'{base_dir}/{csv_file}')
        print(df.columns)

        with open(f'{output_dir}/ttt.json', 'w', encoding='utf-8') as in_f:
            data = {'instruction': '', 'input': '', 'output': ''}
            for idx, row in df.iterrows():
                ql = row['question'].split('\n')
                data['instruction'] = instruct_template + '问题：' + ql[0] + '\n'
                data['input'] = "选项为:\n " + '\n'.join(ql[1:])
                # data['input'] = '选项为:\n' + 'A.' + row['A'] + '\n' + 'B.' + row['B'] + '\n' + 'C.' + row[
                #     'C'] + '\n' + 'D.' + row[
                #                     'D'] + '\n'
                if 'explanation' in row:
                    data['output'] = row['answer'] + '\n' + row['explanation']
                else:
                    data['output'] = row['answer']
                in_f.write(json.dumps(data, ensure_ascii=False) + '\n')


def read_excel():
   df = pd.read_excel("1111.xlsx")
   for idx, row in df.iterrows():
       print(idx,row)
    # 獲取工作表集合

if __name__ == '__main__':
    make_instruct_ceval()