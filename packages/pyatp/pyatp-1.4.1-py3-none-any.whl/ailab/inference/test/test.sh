#!/bin/bash

python -m ailab.inference \
    --pretrained_model_name chatglm2_6b \
    --pretrained_model_path /home/sdk_models/chatglm2_6b/ \
    --tokenizer_path /home/sdk_models/chatglm2_6b/ \
    --fintuned_weights /home/finetuned_models/my_chatglm2_model/ \
    --test_dataset_path /opt/ailab_sdk/src/ailab/inference/val.txt \
    --base_result_path /opt/ailab_sdk/src/ailab/inference/base.jsonl \
    --finetuned_result_path /opt/ailab_sdk/src/ailab/inference/finetune.jsonl 