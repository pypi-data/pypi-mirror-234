#!/usr/bin/env python
# coding:utf-8
"""
@license: Apache License2
@file: wrapper.py
@time: 2023-03-02 18:58:48.583182
@project: yolo
@project: ./
"""

import sys
import hashlib
import json
from aiges.core.types import *
from aiges.dto import Response, ResponseData, DataListNode, DataListCls

from aiges.sdk import WrapperBase, \
    StringParamField, \
    ImageBodyField, \
    StringBodyField
from aiges.utils.log import log

########
# 请在此区域导入您的依赖库

# Todo
# for example: import numpy
#import os
#import sys
#import io

import argparse
import platform
import torch
import base64
import numpy as np
from pathlib import Path
from models.common import DetectMultiBackend
from utils.dataloaders import IMG_FORMATS, VID_FORMATS, LoadImages, LoadScreenshots, LoadStreams
from utils.general import (LOGGER, Profile, check_file, check_img_size, check_imshow, check_requirements, colorstr, cv2,
                           increment_path, non_max_suppression, print_args, scale_boxes, strip_optimizer, xyxy2xywh)
from utils.augmentations import (Albumentations, augment_hsv, classify_albumentations, classify_transforms, copy_paste,
                                 letterbox, mixup, random_perspective)
from utils.plots import Annotator, colors, save_one_box
from utils.torch_utils import select_device, smart_inference_mode
#要记得把 models utils 这两个文件夹拷过去

########


# 定义模型的超参数和输入参数
class UserRequest(object):
    input1 = ImageBodyField(key="img", path="test_data/bus.jpg")


class UserResponse(object):
    accept1 = StringBodyField(key="img")

class Wrapper(WrapperBase):
    serviceId = "yolo"
    version = "v1"
    requestCls = UserRequest()
    responseCls = UserResponse()
    model = None

    #加载模型
    def wrapperInit(cls, config: {}) -> int:
        log.info(config)
        log.info("Initializing ...")
        device = select_device('cpu')
        cls.model = DetectMultiBackend('./yolov5s.pt', device=device, dnn=False, data=False, fp16=False)
        return 0

    def wrapperOnceExec(cls, params: {}, reqData: DataListCls) -> Response:
        #log.info("got reqdata , %s" % reqData.list)
        for req in reqData.list:
            log.info("reqData key: %s , size is %d" % (req.key, len(req.data)))
        log.warning("reqData bytes md5sum is %s" % hashlib.md5(reqData.list[0].data).hexdigest())
        log.info("I am infer logic...please inplement")
        log.info("Testing reqData get: ")
        rg = reqData.get("img")
        log.info("get key: %s" % rg.key)
        log.info("get key: %d" % len(rg.data))

        # read pic
        stride, names, pt = cls.model.stride, cls.model.names, cls.model.pt
        imagebytes = reqData.get("img").data
        #img = base64.b64decode(imagebytes)
        imgarr = np.frombuffer(imagebytes, np.uint8)  # 转换np序列
        im0s = cv2.imdecode(imgarr, cv2.IMREAD_COLOR) # change to opencv BGR
        im = letterbox(im0s, 640, stride=stride, auto=pt)[0]  # padded resize
        im = im.transpose((2, 0, 1))[::-1]  # HWC to CHW, BGR to RGB
        im = np.ascontiguousarray(im)  # contiguous

        # inference
        im = torch.from_numpy(im).to(cls.model.device)
        im = im.float()  # uint8 to fp16/32
        im /= 255  # 0 - 255 to 0.0 - 1.0
        if len(im.shape) == 3:
            im = im[None]  # expand for batch dim
        pred = cls.model(im, augment=False, visualize=False)
        pred = non_max_suppression(pred, 0.25, 0.45, None, False, max_det=1000)

        for i, det in enumerate(pred):  # per image
            im0 = im0s.copy()
            gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
            imc = im0
            annotator = Annotator(im0, line_width=3, example=str(names))
            if len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_boxes(im.shape[2:], det[:, :4], im0.shape).round()
                for *xyxy, conf, clas in reversed(det):
                    c = int(clas)  # integer class
                    label = names[c]
                    annotator.box_label(xyxy, label, color=colors(c, True))
        im0 = annotator.result()

        # response
        img_base64 = base64.b64encode(im0)
        result_msg = {
            "img": "the result is: %s" % img_base64
        }
        res = Response()
        resd = ResponseData()
        resd.key = "img"
        resd.setDataType(DataText)
        resd.status = Once
        resd.setData(json.dumps(result_msg).encode("utf-8"))
        res.list = [resd]
        return res

    def wrapperFini(cls) -> int:
        return 0

    def wrapperError(cls, ret: int) -> str:
        if ret == 100:
            return "user error defined here"
        return ""

    def wrapperTestFunc(cls, data: [], respData: []):
        pass


if __name__ == '__main__':
    m = Wrapper()
    m.schema()
    m.run()
