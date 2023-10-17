import enum

class TaskType(enum.Enum):
    NLP = 'nlp'
    AUDIO = 'audio'
    CV = 'cv'
    MULTIMODEL = 'multimodel'

class Framework(object):
    Pytorch = 'pt'
    Tensorflow = 'tf'

class Metric(object):
    Accury = 'accuracy'

class Task(object):
    text_classification = 'text-classification'
    token_classification = 'token-classification'
    question_answering = 'question-answering'
    question_answering_cn = 'question-answering-cn'
    table_question_answering = 'table-question-answering'
    zero_shot_classification = 'zero-shot-classification'
    translation = 'translation'
    summarization = 'summarization'
    conversational = 'conversational'
    text_generation = 'text-generation'
    text_to_text_generation = 'text-to-text-generation'
    fill_mask = 'fill-mask'

    text_to_speech = 'text-to-speech'
    automatic_speech_recognition = 'automatic-speech-recognition'
    audio_to_audio = 'audio-to-audio'
    audio_classification = 'audio-classification'
    voice_activity_detection = 'voice-activity-detection'

    depth_estimation = 'depth-estimation'
    image_classification = 'image-classification'
    video_calssification = 'video-calssification'
    object_detection = 'object-detection'
    image_segmentation = 'image-segmentation'
    image_to_image = 'image-to-image'
    unconditional_image_generation = 'unconditional-image-generation'
    zero_shot_image_classification = 'zero-shot-image-classification'

    text_to_image = 'text-to-image'
    text_to_video = 'text-to-video'
    feature_extraction = 'feature-extraction'
    image_to_text = 'image-to-text'
    visual_question_answering = 'visual-question-answering'
    document_question_answering = 'document-question-answering'
    graph_machine_learning = 'graph-machine-learning'
    image_captioning = 'image-captioning'

class Model(object):
    distilbert_base_uncased = 'distilbert-base-uncased'
    chatglm_6b = 'chatglm_6b'
    chatglm2_6b = 'chatglm2_6b'
    alpaca = 'standford_alpaca'
    vicuna = 'chinese_llama_vicuna'
    chinese_alpaca = 'chinese_llama_alpaca'
    chinese_alpaca_2 = 'chinese_llama_alpaca_2'
    open_llama = 'open_llama'
    baichuan_7b = 'baichuan_7b'
    baichuan_13b = 'baichuan_13b'
    bloomz_7b1_mt = 'bloomz_7b1_mt'
    falcon_7b = 'falcon_7b'
    moss_moon_003_base = 'moss_moon_003_base' 
    llama2_7b = 'llama2_7b'
    internlm_7b = 'internlm_7b' 
    belle_7b_2m = 'belle_7b_2m'
    xverse_13b = 'xverse_13b' 
    vilt = 'dandelin/vilt-b32-finetuned-vqa'
    stable_diffusion_2_1 = 'stabilityai/stable-diffusion-2-1'
    ziya_llama_13b = 'ziya_llama_13b'

    #vertical domain
    bencao_llama = 'bencao_llama'
    lawgpt_llama = 'lawgpt_llama'
    code_geex_2 = 'code_geex_2'
    finGPT_chatglm2_v3 = 'finGPT_chatglm2_v3'
    educhat = 'educhat' 
