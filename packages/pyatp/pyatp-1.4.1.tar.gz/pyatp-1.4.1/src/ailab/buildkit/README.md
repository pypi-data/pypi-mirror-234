# docker 镜像build工具

## 依赖

```
pip install jinja2
pip install plumbum  
```

## 生成 ailab Dockerfile

内部构建:

```
 
python -m pyatp_buildkit.build generate  --inference_task text_classification --inference_script_path ailab/inference_wrapper/huggingface/transformers/nlp/text_classification/wrapper/

 

```




 