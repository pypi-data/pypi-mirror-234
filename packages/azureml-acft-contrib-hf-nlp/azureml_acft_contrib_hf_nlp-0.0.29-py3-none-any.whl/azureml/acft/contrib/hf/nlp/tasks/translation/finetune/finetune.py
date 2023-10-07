# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
# Copyright 2020 The HuggingFace Inc. team. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ---------------------------------------------------------

import json
import numpy as np
from pathlib import Path
from functools import partial

from typing import Any, Dict, List, Tuple, Optional

from ..preprocess.base import TranslationDataset
from ....constants.constants import SaveFileConstants, MLFlowHFFlavourConstants, TaskConstants, Tasks
from ....nlp_auto.model import AzuremlAutoModelForTranslation
from ....nlp_auto.tokenizer import AzuremlAutoTokenizer
from ....utils.mlflow_utils import SaveMLflowModelCallback, replace_mlflow_weights_with_pytorch_weights_zero3
from ....metrics.load_metric import load_acft_metric

import torch.nn as nn

from azureml.acft.accelerator.finetune import AzuremlFinetuneArgs, AzuremlDatasetArgs
from azureml.acft.accelerator.finetune import AzuremlTrainer
from azureml.acft.accelerator.constants import HfTrainerType
from azureml.acft.common_components import get_logger_app

from transformers.tokenization_utils_base import PreTrainedTokenizerBase
from transformers.trainer_utils import EvalPrediction
from transformers.models.mbart.tokenization_mbart import MBartTokenizer
from transformers.models.mbart.tokenization_mbart_fast import MBartTokenizerFast
from transformers.models.mbart50.tokenization_mbart50 import MBart50Tokenizer
from transformers.models.mbart50.tokenization_mbart50_fast import MBart50TokenizerFast
from transformers.models.m2m_100.tokenization_m2m_100 import M2M100Tokenizer
from transformers.deepspeed import is_deepspeed_zero3_enabled

from peft import TaskType


MULTILINGUAL_TOKENIZERS = [MBartTokenizer, MBartTokenizerFast, MBart50Tokenizer, MBart50TokenizerFast]


logger = get_logger_app(__name__)


class TranslationFinetune:

    def __init__(self, finetune_params: Dict[str, Any]) -> None:
        # finetune params is finetune component args + args saved as part of preprocess
        self.finetune_params = finetune_params
        self.ft_config = finetune_params.get("finetune_config", {})

        logger.info(f"Task name: {Tasks.TRANSLATION}")

        # set predict_with_generate=True for Translation
        self.finetune_params["predict_with_generate"] = True

        # set log_metrics_at_root=False to not to log to parent
        self.finetune_params["log_metrics_at_root"] = False

    def _get_finetune_args(self, model_type: str) -> AzuremlFinetuneArgs:

        self.finetune_params["model_type"] = model_type
        self.finetune_params["peft_task_type"] = TaskType.SEQ_2_SEQ_LM
        azml_trainer_finetune_args = AzuremlFinetuneArgs(
            self.finetune_params,
            trainer_type=HfTrainerType.SEQ2SEQ,
        )

        return azml_trainer_finetune_args

    def _get_dataset_args(self, tokenizer: Optional[PreTrainedTokenizerBase] = None) -> AzuremlDatasetArgs:

        encoded_train_ds = TranslationDataset(
            str(Path(self.finetune_params["preprocess_output"], self.finetune_params["encoded_train_data_fname"])),
            tokenizer=tokenizer
        )
        encoded_validation_ds = TranslationDataset(
            str(Path(self.finetune_params["preprocess_output"], self.finetune_params["encoded_validation_data_fname"])),
        )
        azml_trainer_dataset_args = AzuremlDatasetArgs(
            train_dataset=encoded_train_ds.dataset,
            validation_dataset=encoded_validation_ds.dataset,
            data_collator=encoded_train_ds.get_collation_function()
        )

        return azml_trainer_dataset_args

    def _load_model(self, tokenizer: PreTrainedTokenizerBase) -> Tuple[nn.Module, str, List[str]]:

        model_params = {
            "tok_prefix": self.finetune_params["tok_prefix"],
            "source_lang": self.finetune_params["source_lang"],
            "target_lang": self.finetune_params["target_lang"],
            "ignore_mismatched_sizes": self.finetune_params["ignore_mismatched_sizes"],
            "resume_from_checkpoint": self.finetune_params["resume_from_checkpoint"],
            "load_in_8bit": self.finetune_params["finetune_in_8bit"],
            "load_in_4bit": self.finetune_params["finetune_in_4bit"],
        }

        if isinstance(tokenizer, MBartTokenizer):
            model_params.update(
                {
                    "decoder_start_token_id": tokenizer.lang_code_to_id[tokenizer.tgt_lang]
                }
            )
            logger.info(f'decoder_start_token_id is set to {model_params["decoder_start_token_id"]}')
        elif isinstance(tokenizer, MBartTokenizerFast):
            model_params.update(
                {
                    "decoder_start_token_id": tokenizer.convert_tokens_to_ids(tokenizer.tgt_lang)
                }
            )
            logger.info(f'decoder_start_token_id is set to {model_params["decoder_start_token_id"]}')

        model_params.update(self.ft_config.get("load_model_kwargs", {}))
        model_params.update({"load_config_kwargs": self.ft_config.get("load_config_kwargs", {})})
        logger.info(f"Loading model with following args: {model_params}")

        # load the model
        model, model_type, new_initalized_layers = AzuremlAutoModelForTranslation.from_pretrained(
            self.finetune_params["model_name_or_path"], **model_params,
        )

        if isinstance(tokenizer, tuple(MULTILINGUAL_TOKENIZERS)) and model.config.decoder_start_token_id is None:
            raise ValueError("Make sure that `config.decoder_start_token_id` is correctly defined")

        # For multilingual translation models like mBART-50 and M2M100 we need to force the target language token
        # as the first generated token.
        if isinstance(tokenizer, (MBart50Tokenizer, MBart50TokenizerFast, M2M100Tokenizer)):
            if model.config.decoder_start_token_id is None:
                raise ValueError("Make sure that `config.decoder_start_token_id` is correctly defined")
            model.config.forced_bos_token_id = model.config.decoder_start_token_id

        return model, model_type, new_initalized_layers

    def _get_tokenizer(self) -> PreTrainedTokenizerBase:
        """This method loads the tokenizer as is w/o any modifications to it"""

        tokenizer_params = {
            "apply_adjust": False,
            "task_name": self.finetune_params["task_name"],
        }

        tokenizer_params.update(self.ft_config.get("load_tokenizer_kwargs", {}))
        tokenizer_params.update({"load_config_kwargs": self.ft_config.get("load_config_kwargs", {})})
        logger.info(f"Loading tokenizer with following params: {tokenizer_params}")

        return AzuremlAutoTokenizer.from_pretrained(self.finetune_params["preprocess_output"], **tokenizer_params)

    def finetune(self) -> None:

        # configure MLflow save callback
        mlflow_infer_params_file_path = Path(
            self.finetune_params["preprocess_output"], MLFlowHFFlavourConstants.INFERENCE_PARAMS_SAVE_NAME_WITH_EXT
        )
        save_mlflow_callback = SaveMLflowModelCallback(
            mlflow_infer_params_file_path=mlflow_infer_params_file_path,
            mlflow_model_save_path=self.finetune_params["mlflow_model_folder"],
            pytorch_model_save_path=(
                self.finetune_params["pytorch_model_folder"]
                if self.finetune_params["apply_lora"] else
                None
            ),
            mlflow_task_type=self.finetune_params["mlflow_task_type"],
            model_name=self.finetune_params["model_name"],
            model_name_or_path=self.finetune_params["model_name_or_path"],
            **{
                "mlflow_hf_args": {
                    "hf_config_class": "AutoConfig",
                    "hf_tokenizer_class": "AutoTokenizer",
                    "hf_pretrained_class": "AutoModelForSeq2SeqLM",
                },
                "mlflow_ft_conf": self.ft_config.get("mlflow_ft_conf", {}),
            },
        )

        # load the tokenizer
        tokenizer = self._get_tokenizer()
        # load the model
        # Initializing the finetune args with dummy_model_type to enable the
        # deepspeed stage3 which is used in :meth _load_model
        finetune_args = self._get_finetune_args("dummy_model_type")
        model, model_type, new_initialized_params = self._load_model(tokenizer)
        # Replacing the dummy_model_type -> original model_type information
        setattr(finetune_args.optimization_args, "model_type", model_type)
        trainer = AzuremlTrainer(
            finetune_args=finetune_args,
            dataset_args=self._get_dataset_args(tokenizer),
            model=model,
            tokenizer=tokenizer,
            metric_func=partial(
                translation_metrics_func,
                tokenizer=tokenizer
            ),
            new_initalized_layers=new_initialized_params,
            custom_trainer_callbacks=[save_mlflow_callback],
        )

        # Torch barrier is used to complete the training on a distributed setup
        # Use callbacks for adding steps to be done at the end of training
        # NOTE Avoid adding any logic after trainer.train()
        # Test the distributed scenario in case you add any logic beyond trainer.train()
        trainer.train()

        # replace pytorch weights for lora / deep speed zero3 optimization
        if trainer.should_save and is_deepspeed_zero3_enabled():
            logger.info("Replacing dummy MLflow weights ")
            replace_mlflow_weights_with_pytorch_weights_zero3(
                self.finetune_params["pytorch_model_folder"],
                self.finetune_params["mlflow_model_folder"]
            )

        # save files only once by Rank-0 process
        if trainer.should_save:
            # save finetune args
            Path(self.finetune_params["pytorch_model_folder"]).mkdir(exist_ok=True, parents=True)
            finetune_args_path = Path(
                self.finetune_params["pytorch_model_folder"], SaveFileConstants.FINETUNE_ARGS_SAVE_PATH)
            self.finetune_params["model_name_or_path"] = str(self.finetune_params["model_name_or_path"])
            with open(finetune_args_path, 'w') as rptr:
                json.dump(self.finetune_params, rptr, indent=2)


def translation_metrics_func(eval_pred: EvalPrediction, tokenizer: PreTrainedTokenizerBase):
    """
    compute and return metrics for translation
    """
    def postprocess_text(preds, labels):
        preds = [pred.strip() for pred in preds]
        labels = [[label.strip()] for label in labels]

        return preds, labels

    metric = load_acft_metric("sacrebleu")
    preds, labels = eval_pred
    if isinstance(preds, tuple):
        preds = preds[0]
    decoded_preds = tokenizer.batch_decode(preds, skip_special_tokens=True)

    # Replace -100 in the labels as we can't decode them.
    labels = np.where(labels != TaskConstants.TRANSLATION_IGNORE_INDEX, labels, tokenizer.pad_token_id)
    decoded_labels = tokenizer.batch_decode(labels, skip_special_tokens=True)

    # Some simple post-processing
    decoded_preds, decoded_labels = postprocess_text(decoded_preds, decoded_labels)
    logger.info(f"Predictions count: {len(decoded_preds)} | References count: {len(decoded_labels)}")

    result = metric.compute(predictions=decoded_preds, references=decoded_labels)
    result = {"bleu": result["score"]}

    prediction_lens = [np.count_nonzero(pred != tokenizer.pad_token_id) for pred in preds]
    result["gen_len"] = np.mean(prediction_lens)
    result = {k: round(v, 4) for k, v in result.items()}

    return result
