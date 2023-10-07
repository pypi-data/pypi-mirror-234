# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import os
import torch
from math import isnan

from typing import Union

from transformers.trainer_callback import TrainerCallback, TrainerControl, TrainerState
from transformers.trainer_utils import IntervalStrategy
from transformers.training_args import TrainingArguments
from transformers.tokenization_utils_base import PreTrainedTokenizerBase
from transformers.modeling_utils import PreTrainedModel
from transformers.trainer import TRAINING_ARGS_NAME

from azureml.acft.common_components import get_logger_app
from azureml.automl.core.inference.inference import AutoMLInferenceArtifactIDs, _get_model_name

from ..constants import AzuremlRunType, RunPropertyConstants, AzuremlConstants, LoraAlgo
from ..lora_wrapper.lora_wrapper import LoraWrapper
from ..lora_wrapper.peft_lora_wrapper import PeftLoraWrapper
from ..utils.model_utils import print_model_summary


logger = get_logger_app(__name__)


# Trainer call back to log metrics
# TODO move to mlflow logging
class FinetuneCallback(TrainerCallback):
    """
    A [`TrainerCallback`] that sends the logs to [AzureML](https://pypi.org/project/azureml-sdk/).
    """

    def __init__(self, azureml_run=None, log_metrics_at_root=True, set_log_prefix=True, model_name=None):
        """
        init azureml_run which is azureml Run object
        """
        self.azureml_run = azureml_run
        self.log_metrics_at_root = log_metrics_at_root
        self.set_log_prefix = set_log_prefix
        self.model_name = model_name

    def _should_log_to_parent(self):
        """
        Check if we should log to parent pipeline run.

        :return: Parent run if we should log else None.
        :rtype: azureml.core.run
        """
        parent_run = self.azureml_run.parent
        child_run = None
        while parent_run is not None and (parent_run.type == AzuremlRunType.PIPELINE_RUN or parent_run.type == AzuremlRunType.STEP_RUN):
            child_run = parent_run
            parent_run = parent_run.parent
        return child_run

    def _is_automl_child(self):
        root_pipeline_run = self._should_log_to_parent()
        if (
            root_pipeline_run is not None and
            root_pipeline_run.parent is not None and root_pipeline_run.parent.type == AzuremlRunType.HYPERDRIVE_RUN and
            root_pipeline_run.parent.parent is not None and root_pipeline_run.parent.parent.type == AzuremlRunType.AUTOML_RUN
        ):
            return root_pipeline_run
        else:
            return None

    def on_train_begin(self, args: TrainingArguments, state: TrainerState, control: TrainerControl, **kwargs):

        # Print the model summary at the beginning of the training loop
        print_model_summary(kwargs["model"], print_params=True)

    def on_init_end(self, args, state, control, **kwargs):
        """
        executes after init and sets azureml_run
        """
        from azureml.core.run import Run

        if self.azureml_run is None and state.is_world_process_zero:
            self.azureml_run = Run.get_context()
            logger.info("Initialized azureml run")

        if self.azureml_run is not None and "OfflineRun" in self.azureml_run.id:
            logger.info("Failed to get context, run as Local run")
            self.azureml_run = None

    def on_log(self, args, state, control, logs=None, **kwargs):
        """
        logs metrics to azureml
        """
        if self.azureml_run and state.is_world_process_zero:
            steps = None
            if args.logging_strategy == IntervalStrategy.STEPS:
                steps = state.global_step
            for k, v in logs.items():
                if isinstance(v, (int, float)) and not isnan(v):

                    if not self.set_log_prefix:
                        eval_prefix = 'eval_'
                        train_prefix = 'train_'
                        if k.startswith(eval_prefix):
                            k = k[len(eval_prefix):]
                        if k.startswith(train_prefix):
                            k = k[len(train_prefix):]
                            k = k + '_train'

                    self.azureml_run.log(k, v, description=k, step=steps)

                    if self.log_metrics_at_root:
                        # Check if parent is a pipeline run.
                        # If pipeline run, log all metrics to parent pipeline as well.
                        parent_run = self._should_log_to_parent()
                        if parent_run:
                            logger.info(f"Logging metrics to {parent_run}")
                            parent_run.log(k, v, description=k, step=steps)
        else:
            logger.info(f"Logging metrics for local run with step {state.global_step} - {logs}")

    def on_train_end(self, args, state, control, **kwargs):
        """
        executes at the end of training and add best metric, algorithm name to run properties
        """
        if self.azureml_run is None:
            logger.info("Local run. Not setting best metric properties")
            return

        best_metric = state.best_metric
        model_id = _get_model_name(self.azureml_run.id)
        metric_properties = {
            RunPropertyConstants.SCORE: best_metric,
            AutoMLInferenceArtifactIDs.ModelName: model_id,
            RunPropertyConstants.RUN_ALGORITHM: self.model_name,
        }

        self.azureml_run.add_properties(metric_properties)
        logger.info("Best metric properties set on run")
        parent_run = self._should_log_to_parent()
        if parent_run:
            parent_run.add_properties(metric_properties)
            logger.info("Best metric properties set on root pipeline run")

        parent_run = self._is_automl_child()
        if parent_run:
            automl_properties = {
                RunPropertyConstants.RUN_TEMPLATE: RunPropertyConstants.AUTOML_CHILD,
            }
            self.azureml_run.add_properties(automl_properties)
            logger.info("automl_child run template set on run")
            parent_run.add_properties(automl_properties)
            logger.info("automl_child run template set on root pipeline run")


class AzuremlPyTorchSaveCallback(TrainerCallback):
    """
    The callback handles saving the pytorch model when lora is enabled either through CUSTOM / PEFT algo
    """

    def __init__(
            self,
            lora_wrapper_obj: Union[LoraWrapper, PeftLoraWrapper],
            pytorch_save_folder: str,
            lora_algo: Union[str, LoraAlgo] = LoraAlgo.CUSTOM
    ):
        """
        init lora parameters
        """
        self.lora_wrapper_obj = lora_wrapper_obj
        self.pytorch_save_folder = pytorch_save_folder
        self.lora_algo = lora_algo

        logger.info(f"Lora call back initialized with lora algo: {self.lora_algo}")

    def save_model_tokenizer_and_trainer_args(
        self,
        model: PreTrainedModel,
        tokenizer: PreTrainedTokenizerBase,
        args: TrainingArguments
    ):

        model.save_pretrained(self.pytorch_save_folder)

        if tokenizer is not None:
            tokenizer.save_pretrained(self.pytorch_save_folder)

        # Good practice: save your training arguments together with the trained model
        torch.save(args, os.path.join(self.pytorch_save_folder, TRAINING_ARGS_NAME))

    def on_train_end_custom_lora(self, args: TrainingArguments, state: TrainerState, control: TrainerControl, **kwargs):
        """Save the lora model trained with custom lora implementation."""

        if state.is_world_process_zero:

            if not isinstance(self.lora_wrapper_obj, LoraWrapper):
                raise ValueError(f"Incorrect lora wrapper object found: {type(self.lora_wrapper_obj)}")

            model, tokenizer = kwargs["model"], kwargs["tokenizer"]

            lora_layer_search_strings = AzuremlConstants.LORA_LAYER_SEARCH_STRINGS
            logger.info(f"Merging the lora weights! Lora layer search strings: {lora_layer_search_strings}")

            model = self.lora_wrapper_obj.merge_lora_layers(model, lora_layer_search_strings=lora_layer_search_strings)

            # store the lora layers state dict separately
            lora_layers_state_dict = self.lora_wrapper_obj.get_lora_layers_state_dict(
                model,
                lora_layer_search_strings=lora_layer_search_strings
            )
            lora_weights_save_path = os.path.join(
                self.pytorch_save_folder, AzuremlConstants.LORA_BASE_FOLDER, AzuremlConstants.LORA_WEIGHTS_NAME)
            os.makedirs(os.path.dirname(lora_weights_save_path), exist_ok=True)
            logger.info(f"Saving the lora weights to {lora_weights_save_path}")
            torch.save(lora_layers_state_dict, lora_weights_save_path)  # save only lora weights

            # set the ignore weights to lora layers so that only HF model weights will be saved
            # TODO see if there is a way to not set the private variable
            ignore_keys = list(lora_layers_state_dict.keys())
            # TODO keys_to_ignore_on_save is not valid for nn.Module
            model._keys_to_ignore_on_save = ignore_keys
            logger.info(f"Ignoring the following keys while saving the merged lora model: {ignore_keys}")

            self.save_model_tokenizer_and_trainer_args(model, tokenizer, args)

    def on_train_end_peft_kbit(self, args: TrainingArguments, state: TrainerState, control: TrainerControl, **kwargs):
        """
        Save the lora model trained with PEFT quantization.

        NOTE: LoRA weights cannot be merged for 4bit and 8bit quantized model
        Alternate solution (round about one)
        1. save the adapter weights
        2. load the model using auto peft model in fp32
        3. merge the weights
        4. save the merged weights
        """
        if state.is_world_process_zero:

            if not isinstance(self.lora_wrapper_obj, PeftLoraWrapper):
                raise ValueError(f"Incorrect lora wrapper object found: {type(self.lora_wrapper_obj)}")

            model, tokenizer = kwargs["model"], kwargs["tokenizer"]

            # update the model in lora wrapper obj
            self.lora_wrapper_obj.model = model

            # merge the weights
            self.lora_wrapper_obj.peft_model_merge()

            # save model, tokenizer and trainer args
            self.save_model_tokenizer_and_trainer_args(self.lora_wrapper_obj.model, tokenizer, args)

    def on_train_end(self, args: TrainingArguments, state: TrainerState, control: TrainerControl, **kwargs):

        if self.lora_algo == LoraAlgo.CUSTOM:
            logger.info("Calling on_train_end callback for custom lora")
            self.on_train_end_custom_lora(args=args, state=state, control=control, **kwargs)
        elif self.lora_algo == LoraAlgo.PEFT:
            logger.info("Calling on_train_end callback for PEFT based lora")
            self.on_train_end_peft_kbit(args=args, state=state, control=control, **kwargs)
