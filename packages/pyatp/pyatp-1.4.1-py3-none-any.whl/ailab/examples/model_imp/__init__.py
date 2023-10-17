#!/usr/bin/env python
# coding:utf-8
""" 
@author: nivic ybyang7
@license: Apache Licence 
@file: __init__.py
@time: 2023/05/26
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
import os
import subprocess
from ailab.log import logger
model_name = os.path.basename(__file__)

req_file = os.path.join(os.path.dirname(__file__), "requirements.txt")

logger.info("Training %s" % model_name)

cmds = [
    "pip config set global.index-url https://repo.model.xfyun.cn/api/packages/administrator/pypi/simple  &&  pip config set global.extra-index-url https://pypi.mirrors.ustc.edu.cn/simple/",
    'pip install -r %s' % req_file]

if os.path.exists(req_file):
    for cm in cmds:
        subprocess.call(cm, shell=True)
