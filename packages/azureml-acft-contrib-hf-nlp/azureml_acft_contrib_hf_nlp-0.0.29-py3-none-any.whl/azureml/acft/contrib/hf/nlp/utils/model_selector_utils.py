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
"""
model selector utils
"""

from pathlib import Path
from typing import Dict, Any, Union
import shutil
import yaml
import json

from ..constants.constants import SaveFileConstants, MLFlowHFFlavourConstants

from azureml.acft.common_components.utils.error_handling.exceptions import ACFTSystemException, ACFTValidationException
from azureml.acft.common_components.utils.error_handling.error_definitions import ACFTSystemError, ACFTUserError

from azureml.acft.common_components import get_logger_app
from azureml._common._error_definition.azureml_error import AzureMLError  # type: ignore


logger = get_logger_app(__name__)


MODEL_REGISTRY_NAME = "azureml-preview"


def get_model_name_from_pytorch_model(model_path: str) -> str:
    """
    Fetch model_name information from pytorch model metadata file
    """
    finetune_args_file = Path(model_path, SaveFileConstants.FINETUNE_ARGS_SAVE_PATH)

    # load the metadata file
    try:
        with open(finetune_args_file, "r") as rptr:
            finetune_args = json.load(rptr)
    except Exception as e:
        raise ACFTValidationException._with_error(
            AzureMLError.create(ACFTUserError, pii_safe_message=(
                f"Failed to load {finetune_args_file}\n"
                f"{e}"
                )
            )
        )

    # check for `model_name` in metadata file
    if finetune_args and "model_name" in finetune_args:
        model_name = finetune_args["model_name"]
        logger.info(f"model name: {model_name}")
        return model_name
    else:
        raise ACFTValidationException._with_error(
            AzureMLError.create(ACFTUserError, pii_safe_message=(
                f"model_name is missing in "
                f"{SaveFileConstants.FINETUNE_ARGS_SAVE_PATH} file"
                )
            )
        )


def get_model_name_from_mlflow_model(model_path: str) -> str:
    """
    Fetch model_name information from mlflow metadata file
    """
    mlflow_config_file = Path(model_path, MLFlowHFFlavourConstants.MISC_CONFIG_FILE)

    # load mlflow config file
    try:
        with open(mlflow_config_file, "r") as rptr:
            mlflow_data = yaml.safe_load(rptr)
    except Exception as e:
        raise ACFTSystemException._with_error(
            AzureMLError.create(ACFTSystemError, pii_safe_message=(
                f"Failed to load {mlflow_config_file}\n"
                f"{e}"
                )
            )
        )

    # fetch the model name
    # TODO try to remove the hard limitation on the flavor name
    try:
        logger.info("Attempt #1 Searching with hftransformers flavor")
        model_name = mlflow_data["flavors"]["hftransformers"][MLFlowHFFlavourConstants.HUGGINGFACE_ID]
        logger.info(f"model name: {model_name}")
        return model_name
    except Exception as _:
        try:
            logger.info("Attempt #2 Searching with hftransformersv2 flavor")
            model_name = mlflow_data["flavors"]["hftransformersv2"][MLFlowHFFlavourConstants.HUGGINGFACE_ID]
            logger.info(f"model name: {model_name}")
            return model_name
        except Exception as e:
            logger.info("Huggingface_id not found in mlflow config, setting default_model_name")
            model_name = MLFlowHFFlavourConstants.DEFAULT_MODEL_NAME
            logger.info(f"model name: {model_name}")
            return model_name


def convert_mlflow_model_to_pytorch_model(mlflow_model_path: Union[str, Path], download_dir: Path):
    """
    converts mlflow model to pytorch model
    """
    download_dir.mkdir(exist_ok=True, parents=True)
    try:
        # copy the model files
        mlflow_model_dir = Path(mlflow_model_path, 'data/model')
        if mlflow_model_dir.is_dir():
            shutil.copytree(
                mlflow_model_dir,
                download_dir,
                dirs_exist_ok=True
            )
        else:
            logger.warning("Model folder is not present in `mlflow_model_folder`. Skipping the copy.")

        # copy config files
        mlflow_config_dir = Path(mlflow_model_path, 'data/config')
        if mlflow_config_dir.is_dir():
            shutil.copytree(
                mlflow_config_dir,
                download_dir,
                dirs_exist_ok=True
            )
        else:
            logger.warning("Config folder is not present in `mlflow_model_folder`. Skipping the copy.")

        # copy tokenizer files
        mlflow_tokenizer_dir = Path(mlflow_model_path, 'data/tokenizer')
        if mlflow_tokenizer_dir.is_dir():
            shutil.copytree(
                mlflow_tokenizer_dir,
                download_dir,
                dirs_exist_ok=True
            )
        else:
            logger.warning("Tokenizer folder is not present in `mlflow_model_folder`. Skipping the copy.")

        # copy code files
        mlflow_code_dir = Path(mlflow_model_path, 'code')
        if mlflow_code_dir.is_dir():
            shutil.copytree(
                mlflow_code_dir,
                download_dir,
                dirs_exist_ok=True
            )

        # copy LICENSE file
        license_file_path = Path(mlflow_model_path, MLFlowHFFlavourConstants.LICENSE_FILE)
        if license_file_path.is_file():
            shutil.copy(str(license_file_path), download_dir)

    except Exception as e:
        shutil.rmtree(download_dir, ignore_errors=True)
        raise ACFTValidationException._with_error(
            AzureMLError.create(ACFTUserError, pii_safe_message=(
                "Failed to convert mlflow model to pytorch model.\n"
                f"{e}"
                )
            )
        )


def model_selector(model_selector_args: Dict[str, Any]):
    """
    Prepares model for continual finetuning
    Save model selector args
    """
    logger.info(f"Model Selector args - {model_selector_args}")
    # pytorch model port
    pytorch_model_path = model_selector_args.get("pytorch_model_path", None)
    # mlflow model port
    mlflow_model_path = model_selector_args.get("mlflow_model_path", None)

    # if both pytorch and mlflow model ports are specified, pytorch port takes precedence
    if pytorch_model_path is not None:
        logger.info("Working with pytorch model")
        model_selector_args["mlflow_model_path"] = None
        model_selector_args["huggingface_id"] = None
        # copy model to download_dir
        model_name = get_model_name_from_pytorch_model(pytorch_model_path)
        model_selector_args["model_name"] = model_name
        download_dir = Path(model_selector_args["output_dir"], model_name)
        download_dir.mkdir(exist_ok=True, parents=True)
        try:
            shutil.copytree(pytorch_model_path, download_dir, dirs_exist_ok=True)
        except Exception as e:
            shutil.rmtree(download_dir, ignore_errors=True)
            raise ACFTSystemException._with_error(
                AzureMLError.create(
                    ACFTSystemError,
                    pii_safe_message=(
                        "shutil copy failed.\n"
                        f"{e}"
                    )
                )
            )
    elif mlflow_model_path is not None:
        logger.info("Working with Mlflow model")
        model_selector_args["huggingface_id"] = None
        model_name = get_model_name_from_mlflow_model(mlflow_model_path)
        model_selector_args["model_name"] = model_name
        # convert mlflow model to pytorch model and save it to model_save_path
        download_dir = Path(model_selector_args["output_dir"], model_name)
        convert_mlflow_model_to_pytorch_model(mlflow_model_path, download_dir)
    elif model_selector_args["model_name"]:
        logger.info(f'Will fetch {model_selector_args["model_name"]} model while fine-tuning')
    else:
        raise ACFTValidationException._with_error(
                AzureMLError.create(
                    ACFTUserError,
                    pii_safe_message=(
                        "Please provide `huggingface_id` or pass valid model to `pytorch_model_path` or `mlflow_model_path`"
                    )
                )
            )

    # Saving model selector args
    model_selector_args_save_path = str(
        Path(model_selector_args["output_dir"], SaveFileConstants.MODEL_SELECTOR_ARGS_SAVE_PATH))
    logger.info(f"Saving the model selector args to {model_selector_args_save_path}")
    with open(model_selector_args_save_path, "w") as wptr:
        json.dump(model_selector_args, wptr, indent=2)
