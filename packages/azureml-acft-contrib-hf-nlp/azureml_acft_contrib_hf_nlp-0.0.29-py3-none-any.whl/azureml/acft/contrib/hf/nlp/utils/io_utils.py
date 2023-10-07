# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import re

from pathlib import Path
from typing import Optional, List

from azureml.acft.common_components import get_logger_app


logger = get_logger_app(__name__)


def find_files_with_inc_excl_pattern(
    root_folder: str,
    include_pat: Optional[str] = None,
    exclude_pat: Optional[str] = None
) -> List[str]:
    """The utility function finds the files recursively searching the root folder that match the patterns specified
    in the include pattern after removing the files matching the exclude pattern.

    :param root_folder: folder in which the files needs to be searched
    :type: str
    :param include_pat: list of file patterns to be included post the files after excluded using the
    pattern `exclude_pat`. Few examples -
        ".py$" - returns the list of the files that ends with .py
        ".py$|.csv$" - returns the list of the files that ends with .py or .csv
    In case
    :type Optional[str]
    :param exclude_pat: list of file patterns to be excluded. The files are excluded first before searching for the
    files matching the pattern. Few examples -
        folder1 - excludes the files and folders that contain the name folder1 from the search list
        folder1/remove_dir[1-2] - excludes the directories remove_dir1 and remove_dir2 in folder1 from the search list.
    :type Optional[str]
    """
    # find all the files in the root folder
    all_files = [
        fpath
        for fpath in Path(root_folder).rglob("*")
        if fpath.is_file()
    ]
    if include_pat is None and exclude_pat is None:
        return [str(fpath) for fpath in all_files]

    # files to exclude
    all_files_minus_exclude = []
    if exclude_pat is not None:
        for fpath in all_files:
            if not re.findall(exclude_pat, str(fpath)):
                all_files_minus_exclude.append(fpath)
    else:
        all_files_minus_exclude = all_files

    # include the files matching the pattern
    files_matching_pattern = []
    if include_pat is not None:
        for fpath in all_files_minus_exclude:
            if re.findall(include_pat, str(fpath)):
                files_matching_pattern.append(fpath)
    else:
        files_matching_pattern = all_files_minus_exclude

    return [str(fpath) for fpath in files_matching_pattern]
