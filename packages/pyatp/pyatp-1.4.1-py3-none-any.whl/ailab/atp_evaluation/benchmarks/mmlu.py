import os
import time
import numpy as np

import datasets
from tqdm import tqdm
from ailab.atp_evaluation.benchmarks.base import AILabBenchmark
from ailab.atp_evaluation.build import BenchmarkRg
from ailab.atp_evaluation.constant import BenchMarkType
from ailab.atp_evaluation.models.base import AILabModel
from ailab.log import logger

subcategories = {
    "abstract_algebra": ["math"],
    "anatomy": ["health"],
    "astronomy": ["physics"],
    "business_ethics": ["business"],
    "clinical_knowledge": ["health"],
    "college_biology": ["biology"],
    "college_chemistry": ["chemistry"],
    "college_computer_science": ["computer science"],
    "college_mathematics": ["math"],
    "college_medicine": ["health"],
    "college_physics": ["physics"],
    "computer_security": ["computer science"],
    "conceptual_physics": ["physics"],
    "econometrics": ["economics"],
    "electrical_engineering": ["engineering"],
    "elementary_mathematics": ["math"],
    "formal_logic": ["philosophy"],
    "global_facts": ["other"],
    "high_school_biology": ["biology"],
    "high_school_chemistry": ["chemistry"],
    "high_school_computer_science": ["computer science"],
    "high_school_european_history": ["history"],
    "high_school_geography": ["geography"],
    "high_school_government_and_politics": ["politics"],
    "high_school_macroeconomics": ["economics"],
    "high_school_mathematics": ["math"],
    "high_school_microeconomics": ["economics"],
    "high_school_physics": ["physics"],
    "high_school_psychology": ["psychology"],
    "high_school_statistics": ["math"],
    "high_school_us_history": ["history"],
    "high_school_world_history": ["history"],
    "human_aging": ["health"],
    "human_sexuality": ["culture"],
    "international_law": ["law"],
    "jurisprudence": ["law"],
    "logical_fallacies": ["philosophy"],
    "machine_learning": ["computer science"],
    "management": ["business"],
    "marketing": ["business"],
    "medical_genetics": ["health"],
    "miscellaneous": ["other"],
    "moral_disputes": ["philosophy"],
    "moral_scenarios": ["philosophy"],
    "nutrition": ["health"],
    "philosophy": ["philosophy"],
    "prehistory": ["history"],
    "professional_accounting": ["other"],
    "professional_law": ["law"],
    "professional_medicine": ["health"],
    "professional_psychology": ["psychology"],
    "public_relations": ["politics"],
    "security_studies": ["politics"],
    "sociology": ["culture"],
    "us_foreign_policy": ["politics"],
    "virology": ["health"],
    "world_religions": ["philosophy"],
}
categories = {
    "STEM": ["physics", "chemistry", "biology", "computer science", "math", "engineering"],
    "humanities": ["history", "philosophy", "law"],
    "social sciences": ["politics", "culture", "economics", "geography", "psychology"],
    "other (business, health, misc.)": ["other", "business", "health"],
}

@BenchmarkRg.register(BenchMarkType.mmlu_alt)
class MMLUBenchmark(AILabBenchmark):
    DATASET_PATH = "cais/mmlu"
    def __init__(self, model: AILabModel, dataset_dir: str, ntrain: int, output_dir: str, **kwargs) -> None:
        super().__init__()
        outpath = os.path.join(output_dir, r"mmlu")
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
        self._result_file = f'mmlu_{result_dir_prefix}_{self._kshot}_shot.txt'
    
    def evaluate(self):
        subjects = sorted(subcategories.keys())
        # logger.info(subjects)
        all_cors = []
        subcat_cors = {
            subcat: [] for subcat_lists in subcategories.values() for subcat in subcat_lists
        }
        cat_cors = {cat: [] for cat in categories}
        samples = 0
        for sub_name in subjects:
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
            cors = self.__eval_subject(sub_name, test_df, dev_df, self._kshot)
            samples += test_df.shape[0]
            acc = np.mean(cors)
            with open(os.path.join(self._result_dir, self._result_file), "a") as f:
                f.write("Average accuracy {:.3f} - {}({})\n".format(acc, sub_name, test_df.shape[0]))
            subcats = subcategories[sub_name]
            for subcat in subcats:
                subcat_cors[subcat].append(cors)
                for key in categories.keys():
                    if subcat in categories[key]:
                        cat_cors[key].append(cors)
            all_cors.append(cors)

        with open(os.path.join(self._result_dir, self._result_file), "a") as f:
            for subcat in subcat_cors:
                subcat_acc = np.mean(np.concatenate(subcat_cors[subcat]))
                f.write("Average accuracy {:.3f} - {}\n".format(subcat_acc, subcat))

            for cat in cat_cors:
                cat_acc = np.mean(np.concatenate(cat_cors[cat]))
                f.write("Average accuracy {:.3f} - {}\n".format(cat_acc, cat))

            weighted_acc = np.mean(np.concatenate(all_cors))
            f.write("Average accuracy: {:.3f}({})\n".format(weighted_acc, samples))

    def __eval_subject(self, subject_name, test_df, dev_df=None, kshot=-1):
        results = {}
        cors = []
        train_prompt = self.__gen_few_shot_prompt(dev_df, subject_name, kshot)
        for i in tqdm(range(test_df.shape[0])):
            question = self.__format_example(test_df, i, include_answer=False)
            prompt = train_prompt + question
            #logger.info(prompt)
            ans = self._model.get_answer_of_multiple_choices_question(prompt, self._choices)
            label = self._choices[test_df[i]['answer']]
            #logger.info(ans)
            cor = ans == label
            #logger.info(cor)
            cors.append(cor)
        cors = np.array(cors)
        return cors

    def __format_example(self, df, idx, include_answer=True):
        prompt = df[idx]['question']
        choice_list = df[idx]['choices']
        for j in range(len(choice_list)):
            prompt += "\n{}. {}".format(self._choices[j], choice_list[j])
        prompt += "\nAnswer:"
        if include_answer:
            prompt += " {}\n\n".format(self._choices[df[idx]['answer']])
        return prompt

    def __gen_few_shot_prompt(self, train_df, subject, k=-1):
        prompt = "The following is multiple choice question about {}.\n\n".format(
            self._format_subject(subject)
        )
        if k == -1:
            k = train_df.shape[0]
        if k > 0:
            prompt = "The following are multiple choice questions (with answers) about {}.\n\n".format(
                self._format_subject(subject)
            )
        for i in range(k):
            prompt += self.__format_example(train_df, i)
        return prompt