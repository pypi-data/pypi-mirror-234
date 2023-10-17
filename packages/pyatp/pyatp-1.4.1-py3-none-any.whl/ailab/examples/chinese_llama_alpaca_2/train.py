#!/usr/bin/env python
# coding:utf-8
""" 
@author: nivic ybyang7
@license: Apache Licence 
@file: train.py
@time: 2023/09/06
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
import subprocess
import os
from ailab.examples.model_imp import  train

trainfile = train.__file__
def start_train():
    model_name = os.environ.get("MODEL_NAME", "")
    dataset_path = os.environ.get("DATASET_PATH")
    pretrained_model_path = os.environ.get("PRETRAINED_MODEL_PATH", f"/home/.atp/models/chinese_llama_alpaca_2")
    tokenizer_path = os.environ.get("TOKENIZER_PATH", "/home/.atp/models/chinese_llama_alpaca_2")
    epochs = os.environ.get("NUM_TRAIN_EPOCHS", 4)
    lr = os.environ.get("LEARNING_RATE", 5e-5)
    opdir = os.environ.get("OUTPUT_DIR", f"/work/train_output/{model_name}")
    env = {
        "PRETRAINED_MODEL_NAME": "chinese_llama_alpaca_2",
        "MODEL_NAME": model_name,
        "DATASET_PATH": dataset_path,
        "PRETRAINED_MODEL_PATH": pretrained_model_path,
        "TOKENIZER_PATH": tokenizer_path,
        "OUTPUT_DIR": opdir,
        "NUM_TRAIN_EPOCHS": str(epochs),
        "LEARNING_RATE": str(lr),
        "END_TO_ZIP": "True"

    }
    os.environ.update(env)

    for k,v in env.items():
        print(f"export {k}={v}")

    cmd = f'python -m ailab.examples.model_imp.train'
    ret = subprocess.call(cmd, shell=True, env=dict(os.environ))
    return ret


if __name__ == '__main__':
    exit(start_train())
