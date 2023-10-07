# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""File for adding all the constants"""

from dataclasses import dataclass, field
from typing import Optional

from transformers.utils import WEIGHTS_NAME


@dataclass
class ErrorConstants:

    CUDA_OUT_OF_MEMORY_ERROR = "CUDA out of memory"
    AUTO_FIND_BATCH_SIZE_MEMORY_ERROR = "No executable batch size found, reached zero"
    LOSS_SCALE_AT_MINIMUM = "Current loss scale already at minimum - cannot decrease scale anymore"


@dataclass
class SaveFileConstants:
    """
    A class to represent constants for metadata related to saving the model.
    """
    OPTIMIZATION_ARGS_SAVE_PATH = "Azureml_finetune_optimization_args.json"
    IO_ARGS_SAVE_PATH = "Azureml_io_args.json"
    LICENSE_SAVE_PATH = "LICENSE"
    ACFT_TRAINER_CHECKPOINTS_PATH = "/tmp/acft/trainer/"


@dataclass
class HfConstants:
    """
    A class to represent constants for hugging face files.
    """
    PT_WEIGHTS_FILE = "pytorch_model.bin"
    TOKENIZER_FILE = "tokenizer.json"


@dataclass
class HfTrainerType:
    SEQ2SEQ: str = "Seq2Seq"
    DEFAULT: str = "default"

    @staticmethod
    def get_fields():
        trainer_types = set()
        dataclass_fields = HfTrainerType.__dataclass_fields__
        for trainer_type in dataclass_fields:
            trainer = dataclass_fields[trainer_type]
            trainer_types.add(trainer.default)
        return trainer_types


@dataclass
class HfTrainerMethodsConstants:
    """
    A class to represent constants for overriding HF trainer class methods
    """

    AZUREML_TRAIN_SAMPLER = "AzmlTrainSampler"
    AZUREML_EVAL_SAMPLER = "AzmlEvalSampler"
    AZUREML_OPTIMIZER = "AzmlOptimizer"
    AZUREML_LR_SCHEDULER = "AzmlLrScheduler"
    AZUREML_COMPUTE_LOSS = "AzmlComputeLoss"


@dataclass
class MetricConstants:
    """
    A class to represent constants related to Metrics.
    """

    METRIC_LESSER_IS_BETTER = [
        "loss"
    ]


@dataclass
class AzuremlConstants:
    """
    General constants
    """
    LORA_LAYER_SEARCH_STRINGS = ["lora_A", "lora_B"]
    LORA_BASE_FOLDER = "Azureml_ft_lora_dir"
    LORA_WEIGHTS_NAME = WEIGHTS_NAME
    BASE_WEIGHTS_FOLDER = "Azureml_base_weights"


@dataclass
class HfModelTypes:
    GPT2 = "gpt2"
    ROBERTA = "roberta"
    DEBERTA = "deberta"
    DISTILBERT = "distilbert"
    BERT = "bert"
    BART = "bart"
    MBART = "mbart"
    T5 = "t5"
    CAMEMBERT = "camembert"
    GPT_NEOX = "gpt_neox"
    LLAMA = "llama"
    FALCON = "falcon"
    REFINEDWEBMODEL = "RefinedWebModel"


@dataclass
class LoraAlgo:
    """
    Lora algorithm to use
        1. custom lora implementation defined under :folder utils/lora_wrapper
        2. PEFT
    """
    CUSTOM = "custom"
    PEFT = "peft"


@dataclass
class _AzuremlOptimizationArgs:
    """Optimization args of azureml"""

    # Quantization parameters
    finetune_in_8bit: bool = field(
        default=False,
        metadata={
            "help": "enable 8 bit training"
        }
    )
    finetune_in_4bit: bool = field(
        default=False,
        metadata={
            "help": "enable 4 bit training"
        }
    )

    # LoRA parameters
    lora_algo: str = field(
        default=LoraAlgo.CUSTOM,
        metadata={
            "help": "lora algorithm to use - `custom` or `peft`."
            "If :param `load_in_8bit` is set to True and :param `apply_lora` is set to True."
            "`lora_algo` will be force set to LoraAlgo.PEFT"
        }
    )
    peft_task_type: Optional[str] = field(
        default=None,
        metadata={
            "help": "peft task type will help to identify which peft model to load"
        }
    )
    apply_lora: bool = field(
        default=False,
        metadata={
            "help": "If set to true, LoRA will be applied"
        },
    )
    lora_alpha: int = field(
        default=128,
        metadata={"help": "lora attn alpha"},
    )
    lora_dropout: float = field(
        default=0.0,
        metadata={"help": "lora dropout value"},
    )
    lora_r: int = field(
        default=8,
        metadata={"help": "lora dimension"},
    )
    model_type: Optional[str] = field(
        default=None,
        metadata={"help": "family of the model to which lora needs to be applied for"}
    )

    # model parameters
    model_name: Optional[str] = field(
        default=None,
        metadata={"help": "Model name"}
    )

    # ORT
    apply_ort: bool = field(
        default=False,
        metadata={
            "help": "If set to true, will use the ONNXRunTime training"
        },
    )

    # Deepspeed
    apply_deepspeed: bool = field(
        default=False,
        metadata={
            "help": "If set to true, will enable deepspeed for training"
        },
    )
    deepspeed_config: Optional[str] = field(
        default=None,
        metadata={
            "help": "Deepspeed config to be used for finetuning"
        },
    )

    # Evaluation interval
    evaluation_steps_interval: int = field(
        default=0,
        metadata={
            "help": "Steps between 2 evaluations"
        }
    )

    # Early stopping
    apply_early_stopping: bool = field(default=False, metadata={"help": "Enable early stopping"})
    early_stopping_patience: int = field(
        default=1,
        metadata={"help": "Stop training when the specified metric worsens for early_stopping_patience evaluation calls"}
    )
    early_stopping_threshold: float = field(
        default=0.0,
        metadata={"help": "Denotes how much the specified metric must improve to satisfy early stopping conditions"}
    )

    # continual finetune
    is_continual_finetune: bool = field(
        default=False,
        metadata={"help": "denotes continual finetune"}
    )

    # log_metrics_at_root to log metrics to parent job
    # need to log metrics to parent when running a sweep job
    log_metrics_at_root: bool = field(
        default=True,
        metadata={"help": "if True will log metrics to parent"}
    )

    # set_log_prefix to set 'eval' or 'train' prefix to metrics
    set_log_prefix: bool = field(
        default=True,
        metadata={"help": "if True will append prefix to metrics"}
    )


@dataclass
class _AzuremlIOArgs:
    """Input/Output args of azureml"""

    # Output
    pytorch_model_folder: str = field(
        metadata={"help": "Output directory to save pytorch model"}
    )

    # Input
    model_selector_output: str = field(
        metadata={"help": "Output directory of model selector component"}
    )


class AzuremlRunType:
    PIPELINE_RUN = "azureml.PipelineRun"
    STEP_RUN = "azureml.StepRun"
    HYPERDRIVE_RUN = "hyperdrive"
    AUTOML_RUN = "automl"


class RunPropertyConstants:
    """Run property constants (keys and values)"""

    # Keys
    SCORE = "score"
    RUN_ALGORITHM = "run_algorithm"
    RUN_TEMPLATE = "runTemplate"

    # Values
    AUTOML_CHILD = "automl_child"
