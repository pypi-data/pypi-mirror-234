import json
import os
import time

import datasets
from tqdm import tqdm
from ailab.atp_evaluation.benchmarks.base import AILabBenchmark
from ailab.atp_evaluation.build import BenchmarkRg
from ailab.atp_evaluation.constant import BenchMarkType
from ailab.atp_evaluation.models.base import AILabModel
from ailab.log import logger

subject_list = {
    "high_school_physics": "高中物理",
    "fire_engineer": "注册消防工程师",
    "computer_network": "计算机网络",
    "advanced_mathematics": "高等数学",
    "logic": "逻辑学",
    "middle_school_physics": "初中物理",
    "clinical_medicine": "临床医学",
    "probability_and_statistics": "概率统计",
    "ideological_and_moral_cultivation": "思想道德修养与法律基础",
    "operating_system": "操作系统",
    "middle_school_mathematics": "初中数学",
    "chinese_language_and_literature": "中国语言文学",
    "electrical_engineer": "注册电气工程师",
    "business_administration": "工商管理",
    "high_school_geography": "高中地理",
    "modern_chinese_history": "近代史纲要",
    "legal_professional": "法律职业资格",
    "middle_school_geography": "初中地理",
    "middle_school_chemistry": "初中化学",
    "high_school_biology": "高中生物",
    "high_school_chemistry": "高中化学",
    "physician": "医师资格",
    "high_school_chinese": "高中语文",
    "tax_accountant": "税务师",
    "high_school_history": "高中历史",
    "mao_zedong_thought": "毛泽东思想和中国特色社会主义理论概论",
    "high_school_mathematics": "高中数学",
    "professional_tour_guide": "导游资格",
    "veterinary_medicine": "兽医学",
    "environmental_impact_assessment_engineer": "环境影响评价工程师",
    "basic_medicine": "基础医学",
    "education_science": "教育学",
    "urban_and_rural_planner": "注册城乡规划师",
    "middle_school_biology": "初中生物",
    "plant_protection": "植物保护",
    "middle_school_history": "初中历史",
    "high_school_politics": "高中政治",
    "metrology_engineer": "注册计量师",
    "art_studies": "艺术学",
    "college_economics": "大学经济学",
    "college_chemistry": "大学化学",
    "law": "法学",
    "sports_science": "体育学",
    "civil_servant": "公务员",
    "college_programming": "大学编程",
    "middle_school_politics": "初中政治",
    "teacher_qualification": "教师资格",
    "computer_architecture": "计算机组成",
    "college_physics": "大学物理",
    "discrete_mathematics": "离散数学",
    "marxism": "马克思主义基本原理",
    "accountant": "注册会计师",
}

@BenchmarkRg.register(BenchMarkType.ceval)
class CEVALBenchmark(AILabBenchmark):
    DATASET_PATH = "ceval/ceval-exam"
    def __init__(self, model: AILabModel, dataset_dir: str, ntrain: int, output_dir: str, **kwargs) -> None:
        super().__init__()
        outpath = os.path.join(output_dir, r"ceval")
        if not os.path.exists(outpath):
            os.mkdir(outpath)
        run_date = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(time.time()))
        logger.info(model.model_name)
        result_dir_prefix = model.model_name.replace("/", "_")
        self._result_dir = os.path.join(outpath, f"{result_dir_prefix}_{run_date}")
        os.mkdir(self._result_dir)
        if not os.path.exists(dataset_dir):
            raise TypeError(f'{dataset_dir} is not exist')
        self._dataset_dir = dataset_dir
        self._kshot = ntrain if ntrain is not None else 5
        self._model = model
        self._result_file = f'ceval_{result_dir_prefix}_{self._kshot}_shot.json'
        
    def evaluate(self):
        results = dict()
        for sub_name in list(sorted(subject_list.keys())):
            logger.info(f"start eval {sub_name}")
            data_path = self.DATASET_PATH
            if self._dataset_dir is not None:
                data_path = os.path.join(self._dataset_dir, self.DATASET_PATH)
            self.dataset = datasets.load_dataset(
                path=data_path,
                name=sub_name)
            test_df = self.dataset["test"]
            dev_df = self.dataset["dev"]
            self._kshot = min(self._kshot, dev_df.shape[0])
            sub_results = self.__eval_subject(sub_name, test_df, dev_df, self._kshot)
            results.update({sub_name:sub_results})
            json.dump(results, open(os.path.join(self._result_dir, self._result_file), 'w'), indent=True, ensure_ascii=False)
    
    def __eval_subject(self, subject_name, test_df, dev_df=None, kshot=-1):
        results = {}
        train_prompt = self.__gen_few_shot_prompt(dev_df, subject_name, kshot)
        for i in tqdm(range(test_df.shape[0])):
            question = self.__format_example(test_df, i, include_answer=False)
            prompt = train_prompt + question
            # logger.info(prompt)
            ans = self._model.get_answer_of_multiple_choices_question(prompt, self._choices)
            # logger.info(ans)
            idx = test_df[i]['id']
            results[str(idx)] = ans
        return results
    
    def __format_example(self, df, idx, include_answer=True):
        prompt = df[idx]['question']
        for choice in self._choices:
            option_data = df[idx][choice]
            prompt += f'\n{choice}. {option_data}'
        prompt += "\n答案："
        if include_answer:
            prompt += " {}\n\n".format(df[idx]['answer'])
        return prompt

    def __gen_few_shot_prompt(self, train_df, subject, k=-1):
        prompt = f"以下是中国关于{subject_list[subject]}考试的单项选择题，请选出其中的正确答案。\n\n"
        if k == -1:
            k = train_df.shape[0]
        for i in range(k):
            prompt += self.__format_example(train_df, i)
        return prompt