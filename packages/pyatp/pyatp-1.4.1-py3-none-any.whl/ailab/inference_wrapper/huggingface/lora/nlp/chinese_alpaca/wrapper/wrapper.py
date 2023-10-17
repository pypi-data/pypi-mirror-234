#!/usr/bin/env python
# coding:utf-8
"""
@license: Apache License2
@file: wrapper.py
@time: 2022-08-19 02:05:07.467170
@project: mnist
@project: ./
"""
import os.path
from aiges.core.types import *
try:
    from aiges_embed import ResponseData, Response, DataListNode, DataListCls  # c++
except:
    from aiges.dto import Response, ResponseData, DataListNode, DataListCls

from aiges.sdk import WrapperBase, \
    ImageBodyField, \
    StringBodyField, StringParamField
from aiges.utils.log import log, getFileLogger
import threading
import torch
import copy
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
device = torch.device(0)
from peft import PeftModel


# 定义模型的超参数和输入参数
class UserRequest(object):
    input1 = StringBodyField(key="text", value='''这道试题类型属于 判断推理，类比推理，逻辑关系，逻辑关系-并列关系中的一种。 试题: QQ：微信：FaceBook
 请从下列选项选出一个最恰当的答案: A. 手提电脑：打印机：数字电视
B. 微博：论坛：互联网
C. 人民日报：工人日报：光明日报
D. 医生：护士：患者
'''.encode('utf-8'))
    input2 = StringParamField(key="atp_patch_id", value="179387562041344")


# 定义模型的输出参数
class UserResponse(object):
    accept1 = StringBodyField(key="result")


# 定义服务推理逻辑
class Wrapper(WrapperBase):
    serviceId = "effcient"
    version = "v1"
    requestCls = UserRequest()
    responseCls = UserResponse()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filelogger = None
        self.model = None
        self.tokenizer = None
        self.patch_id_map = {}
        self.first_load_lora = True
        self.lock = threading.Lock()

    def wrapperInit(self, config: {}) -> int:
        logger = log

        logger.info("Initializing ...")
        from transformers import LlamaTokenizer, LlamaForCausalLM,AutoModelForCausalLM
        #base_model_path = os.environ.get("PRETRAINED_MODEL_NAME")
        #tokenizer_path = os.environ.get("TOKENIZER_PATH")
        base_model_path = "/models/mnt/atpdata/models_hub/bigmodels/for_atp/chinese_llama_alpaca_2"
        tokenizer_path = "/models/mnt/atpdata/models_hub/bigmodels/for_atp/chinese_llama_alpaca_2"
        if not base_model_path or not tokenizer_path:
            log.error("should have environ(PRETRAINED_MODEL_NAME,MODEL_PATH(lora weight dir）,TOKENIZER_PATH)")
            return -1

        load_type = torch.float16
        tokenizer = LlamaTokenizer.from_pretrained(tokenizer_path)

        if (len(tokenizer)) == 55296: #v2 49954:v1
            from ailab.utils.attn_and_long_ctx_patches import apply_attention_patch, apply_ntk_scaling_patch
            apply_attention_patch(use_memory_efficient_attention=True)
            apply_ntk_scaling_patch(1.0)

        base_model = LlamaForCausalLM.from_pretrained(
            base_model_path,
            load_in_8bit=False,
            torch_dtype=load_type,
            low_cpu_mem_usage=True,
            device_map='auto',
            )

        model_vocab_size = base_model.get_input_embeddings().weight.size(0)
        tokenzier_vocab_size = len(tokenizer)
        logger.info(f"Vocab of the base model: {model_vocab_size}")
        logger.info(f"Vocab of the tokenizer: {tokenzier_vocab_size}")
        if model_vocab_size!=tokenzier_vocab_size:
            assert tokenzier_vocab_size > model_vocab_size
            logger.info("Resize model embeddings to fit tokenizer")
            base_model.resize_token_embeddings(tokenzier_vocab_size)

        self.model = base_model
        self.tokenizer = tokenizer
        self.filelogger = getFileLogger()
        return 0

    def testLoad(self,patch_id):
        lora_weight_path = "/home/.atp/lora_weight/"
        lora_weight_path = os.path.join(lora_weight_path, str(patch_id))
        if self.first_load_lora == True:
            self.model = PeftModel.from_pretrained(self.model, lora_weight_path, adapter_name=patch_id)
            self.first_load_lora = False
        else:
            self.model.load_adapter(lora_weight_path, patch_id)
        self.model.eval()
        self.patch_id_map[patch_id] = (patch_id,lora_weight_path)
    def wrapperLoadRes(self, reqData: DataListCls, patch_id: int) -> int:
        if patch_id in self.patch_id_map:
            log.warn("patch_id has exist.Please first to UnloadRes")
            return 0
        lora_weight_path = "/home/.atp/lora_weight/"
        lora_weight_path = os.path.join(lora_weight_path, str(patch_id))
        #if os.path.exists(lora_weight_path):
        #    log.error("zip file has exist.Please first to UnloadRes")
        #    return -1

        import io
        import zipfile
        byte_stream = io.BytesIO(reqData.list[0].data)
        # 解压缩 zip 文件到指定目录
        with zipfile.ZipFile(byte_stream, 'r') as zip_ref:
            zip_ref.extractall(lora_weight_path)

        if self.first_load_lora == True:
            self.model = PeftModel.from_pretrained(self.model, lora_weight_path, adapter_name=patch_id)
            self.first_load_lora = False
        else:
            self.model.load_adapter(lora_weight_path, patch_id)
        self.model.eval()
        self.patch_id_map[patch_id] = (patch_id,lora_weight_path)
        return 0

    def wrapperUnloadRes(self, patch_id: int) -> int:
        if patch_id not in self.patch_id_map:
            log.error("patch_id not exist")
            return 0
        lora_weight_path = self.patch_id_map[patch_id][1]
        if not os.path.exists(lora_weight_path):
            log.error("lora weigth path not exist")
            return 0
        import shutil
        shutil.rmtree(lora_weight_path)
        del self.patch_id_map[patch_id]
        return 0

    def evaluate(self, instruction: str, model , tokenizer, adapter) -> str:
        generation_config = dict(
            temperature=0.2,
            top_k=40,
            top_p=0.9,
            do_sample=True,
            num_beams=1,
            repetition_penalty=1.3,
            max_new_tokens=400
            )

        # The prompt template below is taken from llama.cpp
        # and is slightly different from the one used in training.
        # But we find it gives better results
        if (len(tokenizer)) == 49954:
            prompt_input = (
                "Below is an instruction that describes a task. "
                "Write a response that appropriately completes the request.\n\n"
                "### Instruction:\n\n{instruction}\n\n### Response:\n\n"
            )
            def generate_prompt(instruction, input=None):
                if input:
                    instruction = instruction + '\n' + input
                return prompt_input.format_map({'instruction': instruction})
        elif (len(tokenizer)) == 55296:
            prompt_input = (
                "[INST] <<SYS>>\n"
                "{system_prompt}\n"
                "<</SYS>>\n\n"
                "{instruction} [/INST]"
            )
            DEFAULT_SYSTEM_PROMPT = """You are a helpful assistant. 你是一个乐于助人的助手。"""
            def generate_prompt(instruction, system_prompt=DEFAULT_SYSTEM_PROMPT):
                return prompt_input.format_map({'instruction': instruction,'system_prompt': system_prompt})

        with torch.no_grad():
            input_text = generate_prompt(instruction=instruction)
            inputs = tokenizer(input_text,return_tensors="pt")  #add_special_tokens=False ?
            input_ids = inputs["input_ids"].to(device)
            attention_mask = inputs['attention_mask'].to(device)
            adapter_names = [adapter]
            if adapter == '0':
                adapter_names = []
                generation_output = model.generate(
                input_ids = input_ids,
                attention_mask = attention_mask,
                eos_token_id=tokenizer.eos_token_id,
                pad_token_id=tokenizer.pad_token_id,
                **generation_config
            )
            else:
                generation_output = model.generate(
                adapter_names=adapter_names,
                input_ids = input_ids,
                attention_mask = attention_mask,
                eos_token_id=tokenizer.eos_token_id,
                pad_token_id=tokenizer.pad_token_id,
                **generation_config
            )
            s = generation_output[0]
            output = tokenizer.decode(s,skip_special_tokens=True)
            if (len(tokenizer)) == 49954:
                response = output.split("### Response:")[1].strip()
            else:
                response = output.split("[/INST]")[-1].strip()
            return response

    def _base_model_inference(self, reqData: DataListCls, adapter_name) -> str:
        tokenizer = self.tokenizer
        model = self.model

        if hasattr(model, 'disable_adapter'):
            model.disable_adapter()
            
        input_text = reqData.get("text").data.decode('utf-8')
        self.filelogger.info("got input_text , %s" % input_text)

        return self.evaluate(input_text,model,tokenizer, adapter_name)

    def _lora_model_infence(self, reqData: DataListCls, adapter_name) -> str:
        if adapter_name not in self.patch_id_map:
            log.error("resid not exist")
            return ""
        tokenizer = self.tokenizer
        #model = self.patch_id_map[adapter_name][0]

        instruction = reqData.get("text").data.decode('utf-8')
        return self.evaluate(instruction,self.model,tokenizer,adapter_name)



    def wrapperOnceExec(self, params: {}, reqData: DataListCls, usrTag:str="",persId: int = 0) -> Response:
        patch_id = params.get("atp_patch_id", 0)
        self.filelogger.info("got reqdata , %s, patch_ID %s" %( reqData.list, patch_id))

        self.lock.acquire()
        if patch_id == 0 or patch_id == "0":
            result = self._base_model_inference(reqData, "0")
        else:
            result = self._lora_model_infence(reqData, patch_id)
        self.lock.release()
        if not result:
            self.filelogger.info("#####")
            return -1

        self.filelogger.info("got result , %s" % result)
        # 使用Response封装result
        res = Response()
        resd = ResponseData()
        resd.key = "result"
        resd.setDataType(DataText)
        resd.status = Once
        resd.setData(result.encode("utf-8"))
        print("###")
        self.filelogger.info("###")

        self.filelogger.info(result)
        print(result)
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

    def run_once(self):
        # 1. 模拟调用初始化引擎
        #  传入配置当前模拟为空
        self.wrapperInit(self.config)
        self.testLoad("179387562041344")

        try:
            # 2. 准备wrapperOnceExec需要的数据
            inputs_fields, inputs_body = self._parse_inputs()

            params_fields, required_params = self._parse_params()
            params = self.params_test_values
            reqData = []
            reqData.append(self.inputs_test_values)
            req = DataListCls()
            tmp = []
            for key, value in self.inputs_test_values.items():
                node = DataListNode()
                node.key = key
                node.data = value
                node.len = len(value)
                typeStr = inputs_fields[key]["dataType"]
                node.type = 0
                tmp.append(node)

            req.list = tmp
            # 3. 模拟调用 exec，并返回数据
            response = self.wrapperOnceExec(params, req)
            params['atp_patch_id'] = '0'
            response = self.wrapperOnceExec(params, req)
            params['atp_patch_id'] = '179387562041344'
            response = self.wrapperOnceExec(params, req)
            if self.check_resp(response):
                log.info("wrapper.py has been verified... Congratulations ...!")
            else:
                log.error("Sorry, Please Check The Log Output Above ...")
        except Exception as e:
            # 4. 模拟检查 wrapperOnceExec返回
            log.error(e)
            self.wrapperError(-1)

if __name__ == '__main__':
    m = Wrapper()
    m.run()
    #print(m.schema())

