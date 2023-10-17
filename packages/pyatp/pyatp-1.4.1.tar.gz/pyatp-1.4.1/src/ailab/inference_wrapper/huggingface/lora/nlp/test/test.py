from aiges.dto import Response, ResponseData, DataListNode, DataListCls

"""personal param"""
model_name = 'baichuan_7b'
pretrain_model_name = '/home/sdk_models/baichuan_7b/'
token_path = '/home/sdk_models/baichuan_7b/'
zip_path = '/opt/ailab_sdk/src/test/ailabmodel/my_baichuan_model/baichuan.zip'
module_name = 'efficient'
""""""

import sys
print(sys.path)

import importlib
module_path = f'ailab.inference_wrapper.huggingface.lora.nlp.{module_name}.wrapper.wrapper'
wrapper_module = importlib.import_module(module_path)
Wrapper = getattr(wrapper_module, 'Wrapper')
wrapper = Wrapper()

def Init():
    import os
    os.environ['PRETRAINED_MODEL_NAME'] = pretrain_model_name
    os.environ['TOKENIZER_PATH'] = token_path
    wrapper.wrapperInit({})

def LoadRes(key):
    zip_file_path = zip_path
    with open(zip_file_path, 'rb') as zip_file:
        # 读取压缩包的二进制数据
        zip_data = zip_file.read()
        # 计算数据长度
        zip_data_length = len(zip_data)

    list_node = DataListNode()
    list_node.key = str(key)
    list_node.data = zip_data
    list_node.len = zip_data_length

    req_data = DataListCls()
    req_data.list.append(list_node)
    wrapper.wrapperLoadRes(req_data, key)

def Once(key, text):
    http_node = DataListNode()
    http_node.key = 'text'
    text_data = text
    text_data = text_data.encode('utf-8')
    http_node.data = text_data 
    http_data = DataListCls()
    http_data.list.append(http_node)

    import os
    os.environ['PetrainedModel'] = model_name
    wrapper.wrapperOnceExec({"atp_patch_id":key}, http_data, key)

def UnloadRes(key):
    wrapper.wrapperUnloadRes(key)


if __name__ == '__main__' :
    Init()
    Once(0, '自然语言处理是什么')
    LoadRes(1)
    Once(1, '自然语言处理是什么')
    UnloadRes(1)


