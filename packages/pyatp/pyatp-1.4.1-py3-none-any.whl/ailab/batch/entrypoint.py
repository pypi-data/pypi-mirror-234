#!/usr/bin/env python
# coding:utf-8
""" 
@author: nivic ybyang7
@license: Apache Licence 
@file: entrypoint.py
@time: 2023/07/10
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
import sys
from ailab.log import logger

def prepare_req():
    req_str = os.environ.get("PIP_REQUIREMENTS", "")
    if not req_str:
        return
    tempfile = '/tmp/requirements.txt'
    req_list = req_str.split(",")
    with open(tempfile, 'w') as temp:
        for line in req_list:
            temp.write(line + "\n")
    temp.close()
    cmds = [
        "pip config set global.index-url https://repo.model.xfyun.cn/api/packages/administrator/pypi/simple  &&  pip config set global.extra-index-url https://pypi.tuna.tsinghua.edu.cn/simple",
        'pip install  -r  %s' % tempfile,

    ]
    for cm in cmds:
        subprocess.call(cm, shell=True)


def prepare_system():
    req_str = os.environ.get("APT_PACKAGES", "")
    if not req_str:
        return
    req_list = ' '.join(req_str.split(","))
    cmds = [
        'apt update',
        'apt install  -y  %s' % req_list,
    ]
    for cm in cmds:
        subprocess.call(cm, shell=True)


DEFAULT_CODE_DIR = '/work/'
USER_SCRIPT = "run.py"


def prepare_script():
    script_path = os.environ.get("SCRIPT_PATH", "/work/code/run.tar.gz")
    # 约定传来的是 tar.gz
    if not os.path.exists(script_path):
        logger.info(f"Not exists: %s" % script_path)
        sys.exit(-1)
    if not script_path.endswith('.tar.gz'):
        logger.info(f"script not a tar.gz")
        sys.exit(-1)
    if not os.path.exists(DEFAULT_CODE_DIR):
        os.makedirs(DEFAULT_CODE_DIR)

    unpress = "tar zxvf %s --strip-components 1 -C %s" % (script_path, DEFAULT_CODE_DIR)
    ret = subprocess.call(unpress, shell=True)
    if ret == 0:
        logger.info("Success Unpress %s" % script_path)
    else:
        logger.info("Please Check....")
        sys.exit(ret)

    # check压缩包是否有 run.py
    fpath = os.path.join(DEFAULT_CODE_DIR, USER_SCRIPT)
    if not os.path.exists(fpath):
        logger.info("Not found....%s" % USER_SCRIPT)
        sys.exit(-1)

    return fpath


def main():
    try:
        prepare_req()
        prepare_system()
    except Exception as e:
        logger.info("Warning: some packages install error. ")

    script = prepare_script()

    if not os.path.exists(script):
        logger.info(f"Error: f{script} not exists... check... ")
    elif not script.endswith(".py"):
        logger.info(f"Error: not a python file..")
    else:
        logger.info("current workdir: %s" % os.getcwd())
        ret = subprocess.call(f"python {script}", shell=True)
        if ret != 0:
            logger.info("batch inference execute error..")
            sys.exit(ret)

        logger.info("Successfully Inference Offiline Job Done")


if __name__ == '__main__':
    main()
