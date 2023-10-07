# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""
code utils
"""


from pathlib import Path
import shutil
from typing import List

from azureml.acft.common_components import get_logger_app


logger = get_logger_app(__name__)


def get_absolute_path(relative_path: str):
    """returns absolute path of a given path"""
    return str(Path(relative_path).resolve())


def get_model_custom_code_files(model_name_or_path: str, model):
    """return list of custom code files from model directory"""

    code_files_list = []

    if hasattr(model, "config") and not hasattr(model.config, "auto_map"):
        return code_files_list

    if Path(model_name_or_path).is_dir():
        model_path = model_name_or_path
    else:
        import transformers_modules
        model_path = str(Path(transformers_modules.__path__[0], *type(model).__module__.split('.')[1:-1]))

    # convert relative to absolute path
    model_path = get_absolute_path(model_path)

    logger.info(f"Searching in {model_path} for code files")
    code_files_list = [file for file in Path(model_path).glob("*.py")]

    logger.info(f"Found code files - {code_files_list}")

    return code_files_list


def copy_code_files(code_files_list: List, destination_paths: List):
    """copies list of files to list of destination folders"""
    for code_file in code_files_list:
        for dst_folder in destination_paths:
            shutil.copy(code_file, get_absolute_path(dst_folder))
