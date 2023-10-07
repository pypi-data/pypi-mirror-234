# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""
File containing HF model related functions
"""
import os
from pathlib import Path

from typing import List, Tuple

import torch

from transformers.models.auto.modeling_auto import (
    AutoModelForSequenceClassification,
    AutoModelForTokenClassification,
    AutoModelForSeq2SeqLM,
    AutoModelForQuestionAnswering,
    AutoModelForCausalLM,
)
from transformers.utils import WEIGHTS_NAME
from transformers.modeling_utils import PreTrainedModel

from transformers import BitsAndBytesConfig

from azureml.acft.common_components import get_logger_app

from .config import AzuremlAutoConfig


logger = get_logger_app(__name__)


# not using Inheritance for Azureml class as while loading auto classes for `trust_remote_code=True` the
# huggingface classes checks for the parent class name and they must be pre-defined Auto classes of transformers
# library not any other unknown custom classes
class AzuremlAutoModelForSequenceClassification():

    @classmethod
    def from_pretrained(cls, hf_model_name_or_path: str, **kwargs) -> Tuple[PreTrainedModel, str, List[str]]:
        """Apply model specific hacks before calling the Base tokenizer"""

        # Initialize the config
        problem_type = kwargs.pop("problem_type", None)
        num_labels = kwargs.pop("num_labels", None)
        label2id = kwargs.pop("label2id", None)
        id2label = kwargs.pop("id2label", None)
        load_config_kwargs = kwargs.pop("load_config_kwargs", {})
        load_in_8bit = kwargs.get("load_in_8bit", False)
        load_in_4bit = kwargs.pop("load_in_4bit", False)
        if load_in_8bit or load_in_4bit:
            # Setting device_map to None or {"": torch.cuda.current_device()} is trying to load
            # the model in GPU 0 always. To avoid that and load the model in all GPUs, :env
            # variable LOCAL_RANK is passed explicitly
            kwargs["device_map"] = {"": int(os.environ["LOCAL_RANK"])}
            logger.info(f'Setting the device map to use the current device GPU: {kwargs["device_map"]}')

        config = AzuremlAutoConfig.from_pretrained(
            hf_model_name_or_path,
            problem_type=problem_type,
            num_labels=num_labels,
            id2label=id2label,
            label2id=label2id,
            output_attentions=False,
            output_hidden_states=False,
            **load_config_kwargs,
        )
        bnb_config = None
        if load_in_4bit:
            bnb_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_use_double_quant=True,
                bnb_4bit_compute_dtype=torch.bfloat16,
            )

        # Initialize the model
        resume_from_checkpoint = kwargs.pop("resume_from_checkpoint", None)
        model_type = AzuremlAutoConfig.get_model_type(config, **load_config_kwargs)
        if resume_from_checkpoint:
            # First load the state dictionary to find the keys of pretrained weights
            # and delete it so that the memory is efficiently used
            weights_path = Path(hf_model_name_or_path, WEIGHTS_NAME)
            pretrained_weights_state_dict = torch.load(weights_path, map_location="cpu")
            pretrained_weights_keys = set(pretrained_weights_state_dict.keys())
            del pretrained_weights_state_dict

            # will load the model using resume_from_checkpoint of HF TrainingArgs
            # so instantiating model with random weights for now
            model = AutoModelForSequenceClassification.from_config(config=config, **kwargs)

            # find the newly initialized layers in the model
            missing_keys = set(model.state_dict().keys()).difference(pretrained_weights_keys)

            return model, model_type, list(missing_keys)
        else:
            model, model_loading_metadata = AutoModelForSequenceClassification.from_pretrained(
                hf_model_name_or_path,
                config=config,
                quantization_config=bnb_config,
                ignore_mismatched_sizes=kwargs.pop("ignore_mismatched_sizes", False),
                output_loading_info=True,
                **kwargs,
            )

            return model, model_type, model_loading_metadata["missing_keys"]


# not using Inheritance for Azureml class as while loading auto classes for `trust_remote_code=True` the 
# huggingface classes checks for the parent class name and they must be pre-defined Auto classes of transformers 
# library not any other unknown custom classes
class AzuremlAutoModelForTokenClassification():

    @classmethod
    def from_pretrained(cls, hf_model_name_or_path: str, **kwargs) -> Tuple[PreTrainedModel, str, List[str]]:
        """Apply model specific hacks before calling the Base tokenizer"""

        # Initialize the config
        problem_type = kwargs.pop("problem_type", None)
        num_labels = kwargs.pop("num_labels", None)
        label2id = kwargs.pop("label2id", None)
        id2label = kwargs.pop("id2label", None)
        load_config_kwargs = kwargs.pop("load_config_kwargs", {})
        load_in_8bit = kwargs.get("load_in_8bit", False)
        load_in_4bit = kwargs.pop("load_in_4bit", False)
        if load_in_8bit or load_in_4bit:
            # Setting device_map to None or {"": torch.cuda.current_device()} is trying to load
            # the model in GPU 0 always. To avoid that and load the model in all GPUs, :env
            # variable LOCAL_RANK is passed explicitly
            kwargs["device_map"] = {"": int(os.environ["LOCAL_RANK"])}
            logger.info(f'Setting the device map to use the current device GPU: {kwargs["device_map"]}')
        bnb_config = None
        if load_in_4bit:
            bnb_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_use_double_quant=True,
                bnb_4bit_compute_dtype=(
                    torch.bfloat16
                    if torch.cuda.is_bf16_supported() else
                    torch.float16
                ),
            )

        config = AzuremlAutoConfig.from_pretrained(
            hf_model_name_or_path,
            problem_type=problem_type,
            num_labels=num_labels,
            id2label=id2label,
            label2id=label2id,
            output_attentions=False,
            output_hidden_states=False,
            **load_config_kwargs,
        )

        # Initialize the model
        resume_from_checkpoint = kwargs.pop("resume_from_checkpoint", None)
        model_type = AzuremlAutoConfig.get_model_type(config, **load_config_kwargs)
        if resume_from_checkpoint:
            # First load the state dictionary to find the keys of pretrained weights
            # and delete it so that the memory is efficiently used
            weights_path = Path(hf_model_name_or_path, WEIGHTS_NAME)
            pretrained_weights_state_dict = torch.load(weights_path, map_location="cpu")
            pretrained_weights_keys = set(pretrained_weights_state_dict.keys())
            del pretrained_weights_state_dict

            # will load the model using resume_from_checkpoint of HF TrainingArgs
            # so instantiating model with random weights for now
            model = AutoModelForTokenClassification.from_config(config=config, **kwargs)

            # find the newly initialized layers in the model
            missing_keys = set(model.state_dict().keys()).difference(pretrained_weights_keys)

            return model, model_type, list(missing_keys)
        else:
            model, model_loading_metadata = AutoModelForTokenClassification.from_pretrained(
                hf_model_name_or_path,
                config=config,
                quantization_config=bnb_config,
                ignore_mismatched_sizes=kwargs.pop("ignore_mismatched_sizes", False),
                output_loading_info=True,
                **kwargs,
            )
            return model, model_type, model_loading_metadata["missing_keys"]


# not using Inheritance for Azureml class as while loading auto classes for `trust_remote_code=True` the 
# huggingface classes checks for the parent class name and they must be pre-defined Auto classes of transformers 
# library not any other unknown custom classes
class AzuremlAutoModelForSummarization():

    @classmethod
    def from_pretrained(cls, hf_model_name_or_path: str, **kwargs) -> Tuple[PreTrainedModel, str, List[str]]:
        """Apply model specific hacks before calling the Base tokenizer"""

        # Initialize the config
        problem_type = kwargs.pop("problem_type", None)
        label2id = kwargs.pop("label2id", None)
        id2label = kwargs.pop("id2label", None)
        # not None for t5 models
        tok_prefix = kwargs.pop("tok_prefix", None)
        load_config_kwargs = kwargs.pop("load_config_kwargs", {})
        load_in_8bit = kwargs.get("load_in_8bit", False)
        load_in_4bit = kwargs.pop("load_in_4bit", False)
        if load_in_8bit or load_in_4bit:
            # Setting device_map to None or {"": torch.cuda.current_device()} is trying to load
            # the model in GPU 0 always. To avoid that and load the model in all GPUs, :env
            # variable LOCAL_RANK is passed explicitly
            kwargs["device_map"] = {"": int(os.environ["LOCAL_RANK"])}
            logger.info(f'Setting the device map to use the current device GPU: {kwargs["device_map"]}')

        bnb_config = None
        if load_in_4bit:
            bnb_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_use_double_quant=True,
                bnb_4bit_compute_dtype=torch.bfloat16,
            )

        config_params = {
            "problem_type": problem_type,
            "id2label": id2label,
            "label2id": label2id,
            "output_attentions": False,
            "output_hidden_states": False,
            **load_config_kwargs,
        }

        if tok_prefix is not None:
            config_params["prefix"] = tok_prefix

        config = AzuremlAutoConfig.from_pretrained(hf_model_name_or_path, **config_params)

        # summarization task specific params
        task_specific_key = "summarization"
        task_specific_params = {
            "early_stopping": False,
            "length_penalty": 1.0,
            "min_length": 0,
            "no_repeat_ngram_size": 0,
            "num_beams": 1,
        }

        if config.task_specific_params is None:
            config.task_specific_params = {}

        if task_specific_key in config.task_specific_params:
            config.task_specific_params[task_specific_key].update(task_specific_params)
        else:
            config.task_specific_params[task_specific_key] = task_specific_params

        # Initialize the model
        resume_from_checkpoint = kwargs.pop("resume_from_checkpoint", None)
        model_type = AzuremlAutoConfig.get_model_type(config, **load_config_kwargs)
        if resume_from_checkpoint:
            # First load the state dictionary to find the keys of pretrained weights
            # and delete it so that the memory is efficiently used
            weights_path = Path(hf_model_name_or_path, WEIGHTS_NAME)
            pretrained_weights_state_dict = torch.load(weights_path, map_location="cpu")
            pretrained_weights_keys = set(pretrained_weights_state_dict.keys())
            del pretrained_weights_state_dict

            # will load the model using resume_from_checkpoint of HF TrainingArgs
            # so instantiating model with random weights for now
            model = AutoModelForSeq2SeqLM.from_config(config=config, **kwargs)

            # find the newly initialized layers in the model
            missing_keys = set(model.state_dict().keys()).difference(pretrained_weights_keys)

            return model, model_type, list(missing_keys)
        else:
            model, model_loading_metadata = AutoModelForSeq2SeqLM.from_pretrained(
                hf_model_name_or_path,
                config=config,
                quantization_config=bnb_config,
                ignore_mismatched_sizes=kwargs.pop("ignore_mismatched_sizes", False),
                output_loading_info=True,
                **kwargs,
            )
            return model, model_type, model_loading_metadata["missing_keys"]


# not using Inheritance for Azureml class as while loading auto classes for `trust_remote_code=True` the 
# huggingface classes checks for the parent class name and they must be pre-defined Auto classes of transformers 
# library not any other unknown custom classes
class AzuremlAutoModelForTranslation():

    @classmethod
    def from_pretrained(cls, hf_model_name_or_path: str, **kwargs) -> Tuple[PreTrainedModel, str, List[str]]:
        """Apply model specific hacks before calling the Base tokenizer"""

        # Initialize the config
        problem_type = kwargs.pop("problem_type", None)
        label2id = kwargs.pop("label2id", None)
        id2label = kwargs.pop("id2label", None)
        source_lang = kwargs.pop("source_lang", None)
        target_lang = kwargs.pop("target_lang", None)
        # not None for t5 models
        tok_prefix = kwargs.pop("tok_prefix", None)
        # not None for Mbart models
        decoder_start_token_id = kwargs.pop("decoder_start_token_id", None)
        load_config_kwargs = kwargs.pop("load_config_kwargs", {})
        load_in_8bit = kwargs.get("load_in_8bit", False)
        load_in_4bit = kwargs.pop("load_in_4bit", False)
        if load_in_8bit or load_in_4bit:
            # Setting device_map to None or {"": torch.cuda.current_device()} is trying to load
            # the model in GPU 0 always. To avoid that and load the model in all GPUs, :env
            # variable LOCAL_RANK is passed explicitly
            kwargs["device_map"] = {"": int(os.environ["LOCAL_RANK"])}
            logger.info(f'Setting the device map to use the current device GPU: {kwargs["device_map"]}')

        bnb_config = None
        if load_in_4bit:
            bnb_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_use_double_quant=True,
                bnb_4bit_compute_dtype=torch.bfloat16,
            )

        config_params = {
            "problem_type": problem_type,
            "id2label": id2label,
            "label2id": label2id,
            "output_attentions": False,
            "output_hidden_states": False,
            **load_config_kwargs,
        }

        if tok_prefix is not None:
            config_params["prefix"] = tok_prefix
        if decoder_start_token_id is not None:
            config_params["decoder_start_token_id"] = decoder_start_token_id

        config = AzuremlAutoConfig.from_pretrained(hf_model_name_or_path, **config_params)

        task_specific_key = f"translation_{source_lang}_to_{target_lang}"
        task_specific_params = {
            "early_stopping": False,
            "num_beams": 1,
        }

        if config.task_specific_params is None:
            config.task_specific_params = {}

        if task_specific_key in config.task_specific_params:
            config.task_specific_params[task_specific_key].update(task_specific_params)
        else:
            config.task_specific_params[task_specific_key] = task_specific_params

        # Initialize the model
        resume_from_checkpoint = kwargs.pop("resume_from_checkpoint", None)
        model_type = AzuremlAutoConfig.get_model_type(config, **load_config_kwargs)
        if resume_from_checkpoint:
            # First load the state dictionary to find the keys of pretrained weights
            # and delete it so that the memory is efficiently used
            weights_path = Path(hf_model_name_or_path, WEIGHTS_NAME)
            pretrained_weights_state_dict = torch.load(weights_path, map_location="cpu")
            pretrained_weights_keys = set(pretrained_weights_state_dict.keys())
            del pretrained_weights_state_dict

            # will load the model using resume_from_checkpoint of HF TrainingArgs
            # so instantiating model with random weights for now
            model = AutoModelForSeq2SeqLM.from_config(config=config, **kwargs)

            # find the newly initialized layers in the model
            missing_keys = set(model.state_dict().keys()).difference(pretrained_weights_keys)

            return model, model_type, list(missing_keys)
        else:
            model, model_loading_metadata = AutoModelForSeq2SeqLM.from_pretrained(
                hf_model_name_or_path,
                config=config,
                quantization_config=bnb_config,
                ignore_mismatched_sizes=kwargs.pop("ignore_mismatched_sizes", False),
                output_loading_info=True,
                **kwargs,
            )
            return model, model_type, model_loading_metadata["missing_keys"]


# not using Inheritance for Azureml class as while loading auto classes for `trust_remote_code=True` the 
# huggingface classes checks for the parent class name and they must be pre-defined Auto classes of transformers 
# library not any other unknown custom classes
class AzuremlAutoModelForQnA():

    @classmethod
    def from_pretrained(cls, hf_model_name_or_path: str, **kwargs) -> Tuple[PreTrainedModel, str, List[str]]:
        """Apply model specific hacks before calling the Base tokenizer"""

        # Initialize the config
        problem_type = kwargs.pop("problem_type", None)
        # Extractive QnA predicts the start and end logits => number of labels to be 2
        # The class names is hardcoded here to allow finetuning models that were trained with classes != 2
        # Refer to this issue for more information https://github.com/huggingface/transformers/issues/22601
        num_labels = 2
        load_config_kwargs = kwargs.pop("load_config_kwargs", {})
        load_in_8bit = kwargs.get("load_in_8bit", False)
        load_in_4bit = kwargs.pop("load_in_4bit", False)
        if load_in_8bit or load_in_4bit:
            # Setting device_map to None or {"": torch.cuda.current_device()} is trying to load
            # the model in GPU 0 always. To avoid that and load the model in all GPUs, :env
            # variable LOCAL_RANK is passed explicitly
            kwargs["device_map"] = {"": int(os.environ["LOCAL_RANK"])}
            logger.info(f'Setting the device map to use the current device GPU: {kwargs["device_map"]}')
        bnb_config = None
        if load_in_4bit:
            bnb_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_use_double_quant=True,
                bnb_4bit_compute_dtype=torch.bfloat16,
            )

        config = AzuremlAutoConfig.from_pretrained(
            hf_model_name_or_path,
            problem_type=problem_type,
            num_labels=num_labels,
            output_attentions=False,
            output_hidden_states=False,
            **load_config_kwargs,
        )

        # Initialize the model
        resume_from_checkpoint = kwargs.pop("resume_from_checkpoint", None)
        model_type = AzuremlAutoConfig.get_model_type(config, **load_config_kwargs)
        if resume_from_checkpoint:
            # First load the state dictionary to find the keys of pretrained weights
            # and delete it so that the memory is efficiently used
            weights_path = Path(hf_model_name_or_path, WEIGHTS_NAME)
            pretrained_weights_state_dict = torch.load(weights_path, map_location="cpu")
            pretrained_weights_keys = set(pretrained_weights_state_dict.keys())
            del pretrained_weights_state_dict

            # will load the model using resume_from_checkpoint of HF TrainingArgs
            # so instantiating model with random weights for now
            model = AutoModelForQuestionAnswering.from_config(config=config, **kwargs)

            # find the newly initialized layers in the model
            missing_keys = set(model.state_dict().keys()).difference(pretrained_weights_keys)

            return model, model_type, list(missing_keys)
        else:
            model, model_loading_metadata = AutoModelForQuestionAnswering.from_pretrained(
                hf_model_name_or_path,
                config=config,
                ignore_mismatched_sizes=kwargs.pop("ignore_mismatched_sizes", False),
                quantization_config=bnb_config,
                output_loading_info=True,
                **kwargs,
            )
            return model, model_type, model_loading_metadata["missing_keys"]


# not using Inheritance for Azureml class as while loading auto classes for `trust_remote_code=True` the 
# huggingface classes checks for the parent class name and they must be pre-defined Auto classes of transformers 
# library not any other unknown custom classes
class AzuremlAutoModelForCausalLM():

    @classmethod
    def from_pretrained(cls, hf_model_name_or_path: str, **kwargs) -> Tuple[PreTrainedModel, str, List[str]]:
        """Apply model specific hacks before calling the Base tokenizer"""

        # Initialize the config
        problem_type = kwargs.pop("problem_type", None)
        load_config_kwargs = kwargs.pop("load_config_kwargs", {})
        load_in_8bit = kwargs.get("load_in_8bit", False)
        load_in_4bit = kwargs.pop("load_in_4bit", False)
        if load_in_8bit or load_in_4bit:
            # Setting device_map to None or {"": torch.cuda.current_device()} is trying to load
            # the model in GPU 0 always. To avoid that and load the model in all GPUs, :env
            # variable LOCAL_RANK is passed explicitly
            kwargs["device_map"] = {"": int(os.environ["LOCAL_RANK"])}
            logger.info(f'Setting the device map to use the current device GPU: {kwargs["device_map"]}')
        bnb_config = None
        if load_in_4bit:
            bnb_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_use_double_quant=True,
                bnb_4bit_compute_dtype=torch.bfloat16,
            )

        config = AzuremlAutoConfig.from_pretrained(
            hf_model_name_or_path,
            problem_type=problem_type,
            output_attentions=False,
            output_hidden_states=False,
            **load_config_kwargs,
        )

        # Initialize the model
        resume_from_checkpoint = kwargs.pop("resume_from_checkpoint", None)
        model_type = AzuremlAutoConfig.get_model_type(config, **load_config_kwargs)
        if resume_from_checkpoint:
            # First load the state dictionary to find the keys of pretrained weights
            # and delete it so that the memory is efficiently used
            weights_path = Path(hf_model_name_or_path, WEIGHTS_NAME)
            pretrained_weights_state_dict = torch.load(weights_path, map_location="cpu")
            pretrained_weights_keys = set(pretrained_weights_state_dict.keys())
            del pretrained_weights_state_dict

            # will load the model using resume_from_checkpoint of HF TrainingArgs
            # so instantiating model with random weights for now
            model = AutoModelForCausalLM.from_config(config=config, **kwargs)

            # find the newly initialized layers in the model
            missing_keys = set(model.state_dict().keys()).difference(pretrained_weights_keys)

            return model, model_type, list(missing_keys)
        else:
            model, model_loading_metadata = AutoModelForCausalLM.from_pretrained(
                hf_model_name_or_path,
                config=config,
                quantization_config=bnb_config,
                ignore_mismatched_sizes=kwargs.pop("ignore_mismatched_sizes", False),
                output_loading_info=True,
                **kwargs,
            )
            return model, model_type, model_loading_metadata["missing_keys"]
