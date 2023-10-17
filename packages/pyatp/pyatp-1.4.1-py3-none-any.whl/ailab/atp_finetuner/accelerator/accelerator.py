import os
import argparse
from accelerate import Accelerator
from accelerate.utils import ProjectConfiguration, set_seed

class AILabAccelerator():
    def __init__(self, accelerator) -> None:
        self._accelerator = accelerator

    @property
    def accelerator_ins(self):
        return self._accelerator
    

    @classmethod
    def from_project_config(cls, **kwargs):
        train_args = kwargs['train_args']
        output_dir = train_args.get('output_dir')
        log_dir = kwargs.get('log_dir', "logs")
        gradient_accumulation_steps = kwargs.get('gradient_accumulation_steps',4)
        mixed_precision = kwargs.get('mixed_precision', "fp16")
        seed = kwargs.get('seed', 1337)

        """
        def parse_args():
            parser = argparse.ArgumentParser(description="Simple example of a training script.")
            args = parser.parse_args()
            env_local_rank = int(os.environ.get("LOCAL_RANK", -1))
            if env_local_rank != -1 and env_local_rank != args.local_rank:
                args.local_rank = env_local_rank
            return args
        parse_args()
        """

        logging_dir = os.path.join(output_dir, log_dir)
        accelerator_project_config = ProjectConfiguration()
        accelerator = Accelerator(
            gradient_accumulation_steps=gradient_accumulation_steps,
            mixed_precision=mixed_precision,
            project_dir=logging_dir,
            project_config=accelerator_project_config,
        )

        # If passed along, set the training seed now.
        set_seed(seed)

        # Handle the repository creation
        if accelerator.is_main_process:
            os.makedirs(output_dir, exist_ok=True)
        return cls(accelerator)