
# 文本分类训练


## 升级 atp python包
```bash
 pip install pyatp -i https://repo.model.xfyun.cn/api/packages/administrator/pypi/simple --upgrade
```

## 开始训练

```bash
export DATASET_PATH=/work/data/text_cls_test
#export TOKENIZER_PATH=/work/train_output/text_classification_tokenizer
#export PRETRAINED_MODEL_PATH=/work/train_output/text_classification
#export PRETRAINED_MODEL_NAME=distilbert-base-uncased
export MODEL_NAME=testtest

python -m ailab.examples.text_classification.train
```
