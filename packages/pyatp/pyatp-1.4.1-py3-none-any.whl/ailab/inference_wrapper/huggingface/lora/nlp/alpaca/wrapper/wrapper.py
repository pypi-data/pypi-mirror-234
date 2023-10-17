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
    serviceId = "standford_alpaca"
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
        from transformers import LlamaForCausalLM, LlamaTokenizer
        from peft import PeftModel
        base_model = os.environ.get("PRETRAINED_MODEL_NAME")
        tokenizer_path = os.environ.get("TOKENIZER_PATH")
        if not base_model or not tokenizer_path:
            log.error("should have environ(BASE_MODEL,LORA_WEIGHT,TOKENIZER_PATH)")
            return -1

        tokenizer = LlamaTokenizer.from_pretrained(tokenizer_path)
        tokenizer.pad_token_id = 0
        model = LlamaForCausalLM.from_pretrained(base_model,load_in_8bit=True,torch_dtype=torch.float16,device_map="auto",)
        self.model = model
        self.tokenizer = tokenizer
        self.filelogger = getFileLogger()
        self.filelogger.info("wrapperInit end")
        return 0
    
    def wrapperLoadRes(self, reqData: DataListCls, patch_id) -> int:
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
            self.model = PeftModel.from_pretrained(self.model, lora_weight_path, torch_dtype=torch.float16, adapter_name=adapter_name)
            self.first_load_lora = False
        else:
            self.model.load_adapter(lora_weight_path, adapter_name)

        self.model.config.pad_token_id = 0  # unk
        self.model.config.bos_token_id = 1
        self.model.config.eos_token_id = 2
        self.model.eval()
        self.model = torch.compile(self.model)
        self.resid_map[patch_id] = lora_weight_path
        self.lock.release()
        return 0
    
    def wrapperUnloadRes(self, presid) -> int:
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
        inputs = tokenizer(input_text, return_tensors='pt')
        inputs = inputs.to(model.device)
        
        from transformers import TextIteratorStreamer
        streamer = TextIteratorStreamer(tokenizer, timeout=60.0, skip_prompt=True, skip_special_tokens=True)
        gen_kwargs = {
                "streamer" : streamer,
                "do_sample": True,
                "temperature": 0.95,
                "top_p": 0.7,
                "top_k": 50,
                "num_beams": 1,
                "max_new_tokens": 512,
                "repetition_penalty": 1.0,
                "length_penalty": 1.0,
            }
        output = model.generate(**inputs, **gen_kwargs)
        output = tokenizer.decode(output[0].tolist(), skip_special_tokens=True)
        return output
    
    def _lora_model_infence(self, reqData: DataListCls, patch_id) -> str:
        if patch_id not in self.resid_map:
            log.error("resid not exist")
            return -1
        tokenizer = self.tokenizer
        model = self.model
        model.set_adapter(str(patch_id))

        from transformers import GenerationConfig
        prompt_template: str = "alpaca"  # The prompt template to use, will default to alpaca.
        from ailab.utils.prompter import Prompter
        prompter = Prompter(prompt_template)

        def evaluate(
            instruction,
            input=None,
            temperature=0.1,
            top_p=0.75,
            top_k=40,
            num_beams=4,
            max_new_tokens=128,
            stream_output=False,
            **kwargs,
        ):
            prompt = prompter.generate_prompt(instruction, input)
            inputs = tokenizer(prompt, return_tensors="pt")
            input_ids = inputs["input_ids"].to('cuda')
            generation_config = GenerationConfig(
                temperature=temperature,
                top_p=top_p,
                top_k=top_k,
                num_beams=num_beams,
                **kwargs,
            )

            # Without streaming
            with torch.no_grad():
                generation_output = model.generate(
                    input_ids=input_ids,
                    generation_config=generation_config,
                    return_dict_in_generate=True,
                    output_scores=True,
                    max_new_tokens=max_new_tokens,
                )
            s = generation_output.sequences[0]
            output = tokenizer.decode(s)
            response =  prompter.get_response(output)
            return response.split("### Instruction:")[0].strip()

        input_text = reqData.get("text").data.decode('utf-8')
        self.filelogger.info("got input_text , %s" % input_text)
        result = evaluate(input_text)
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
