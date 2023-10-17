#!/usr/bin/env python
# coding:utf-8
"""
@license: Apache License2
@file: wrapper.py
@time: 2022-08-19 02:05:07.467170
@project: mnist
@project: ./
"""
import json
import torch
import os.path
import threading
from aiges.core.types import *
try:
    from aiges_embed import ResponseData, Response, DataListNode, DataListCls  # c++
except:
    from aiges.dto import Response, ResponseData, DataListNode, DataListCls

from aiges.sdk import WrapperBase, \
    ImageBodyField, \
    StringBodyField, StringParamField
from aiges.utils.log import log, getFileLogger
from ailab.log import logger

# 定义模型的超参数和输入参数
class UserRequest(object):
    input1 = StringBodyField(key="text", value=b"I have a problem with my iphone that needs to be resolved asap!!")


# 定义模型的输出参数
class UserResponse(object):
    accept1 = StringBodyField(key="result")


# 定义服务推理逻辑
class Wrapper(WrapperBase):
    serviceId = "chatglm"
    version = "v1"
    requestCls = UserRequest()
    responseCls = UserResponse()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = None
        self.tokenizer = None
        self.resid_map = {}
        self.filelogger = None
        self.first_load_lora = True
        self.lock = threading.Lock()

    def wrapperInit(self, config: {}) -> int:
        logger.info("Initializing ...")
        from transformers import AutoTokenizer, AutoModel, AutoConfig
        base_model = os.environ.get("PRETRAINED_MODEL_NAME")
        tokenizer_path = os.environ.get("TOKENIZER_PATH")

        if not base_model or not tokenizer_path:
            log.error("should have environ(BASE_MODEL,MODEL_PATH(lora weight dir.),TOKENIZER_PATH)")
            return -1

        tokenizer = AutoTokenizer.from_pretrained(
            base_model,
            use_fast=False,
            padding_side="left",
            trust_remote_code=True
        )

        config = AutoConfig.from_pretrained(base_model,trust_remote_code=True)
        model = AutoModel.from_pretrained(base_model, config=config, 
                                        trust_remote_code=True, device_map={"": 0})
        assert tokenizer.eos_token_id is not None, "Please update the *.json and *.py files of ChatGLM-6B from HuggingFace."

        self.model = model
        self.tokenizer = tokenizer
        self.filelogger = getFileLogger()
        return 0
    
    def wrapperLoadRes(self, reqData: DataListCls, patch_id: int) -> int:
        from peft import PeftModel
        if patch_id in self.resid_map:
            log.error("resid has exist.Please first to UnloadRes")
            return -1
        lora_weight_path = "/home/.atp/lora_weight/"
        lora_weight_path = os.path.join(lora_weight_path, str(patch_id))
        if os.path.exists(lora_weight_path):
            log.error("zip file has exist.Please first to UnloadRes")
            return -1
        
        import io
        import zipfile
        byte_stream = io.BytesIO(reqData.list[0].data)
        # 解压缩 zip 文件到指定目录
        with zipfile.ZipFile(byte_stream, 'r') as zip_ref:
            zip_ref.extractall(lora_weight_path)

        self.lock.acquire()
        adapter_name = str(patch_id)
        if self.first_load_lora == True:
            self.model = PeftModel.from_pretrained(self.model, lora_weight_path, adapter_name=adapter_name)
            self.first_load_lora = False
        else:
            self.model.load_adapter(lora_weight_path, adapter_name)

        self.model.requires_grad_(False) # fix all model params
        self.model = self.model.half() # cast all params to float16 for inference
        self.model = self.model.cuda()
        self.model.eval()
        self.resid_map[patch_id] = lora_weight_path
        self.lock.release()
        return 0
    
    def wrapperUnloadRes(self, presid: int) -> int:
        if presid not in self.resid_map:
            log.error("resid not exist")
            return -1
        lora_weight_path = self.resid_map[presid]
        if not os.path.exists(lora_weight_path):
            log.error("lora weigth path not exist")
            return -1
        
        self.lock.acquire()
        import shutil
        shutil.rmtree(lora_weight_path)
        del self.resid_map[presid]
        self.lock.release()

    def _base_model_inference(self, reqData: DataListCls) -> str:
        tokenizer = self.tokenizer
        model = self.model

        if hasattr(model, 'disable_adapter'):
            model.disable_adapter()

        input_text = reqData.get("text").data.decode('utf-8')
        self.filelogger.info("got input_text , %s" % input_text)
        response, history = model.chat(tokenizer, input_text, history=[])
        return response

    def _lora_model_infence(self, reqData: DataListCls, patch_id:int) -> str:
        if patch_id not in self.resid_map:
            log.error("resid not exist")
            return -1
        tokenizer = self.tokenizer
        model = self.model
        model.set_adapter(str(patch_id))

        history = []

        generating_args = {
            "do_sample":True,
            "temperature":0.95,
            "top_p":0.7,
            "top_k":50,
            "num_beams":1,
            "max_length":2048,
            "max_new_tokens":None,
            "repetition_penalty":1.0,
        }

        instruction = reqData.get("text").data.decode('utf-8')
        for _, history in model.stream_chat(tokenizer, instruction, history=history, **generating_args):
            pass
        for query, response in history:
            pass
        logger.info(f'instruction {instruction}')
        logger.info(f'response {response}')

        result = response
        return result
    
    def wrapperOnceExec(self, params: {}, reqData: DataListCls, presid: int) -> Response:
        patch_id = params.get("atp_patch_id", 0)
        self.filelogger.info("got reqdata , %s" % reqData.list)

        self.lock.acquire()
        if patch_id == 0 or patch_id == "0":
            result = self._base_model_inference(reqData)
        else:
            result = self._lora_model_infence(reqData, patch_id)
        self.lock.release()

        if not result:
            return -1
        
        self.filelogger.info("got result , %s" % result)
        # 使用Response封装result
        res = Response()
        resd = ResponseData()
        resd.key = "result"
        resd.setDataType(DataText)
        resd.status = Once
        resd.setData(result.encode("utf-8"))
        res.list = [resd]
        return res

    def wrapperFini(cls) -> int:
        return 0

    def wrapperError(cls, ret: int) -> str:
        if ret == 100:
            return "user error defined here"
        return ""

    '''
        此函数保留测试用，不可删除
    '''

    def wrapperTestFunc(cls, data: [], respData: []):
        pass


if __name__ == '__main__':
    m = Wrapper()
    m.run()
