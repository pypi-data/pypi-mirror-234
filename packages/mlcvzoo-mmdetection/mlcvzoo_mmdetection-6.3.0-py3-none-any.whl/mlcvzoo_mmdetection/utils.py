# Copyright Open Logistics Foundation
#
# Licensed under the Open Logistics Foundation License 1.3.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: OLFL-1.3

"""
Module for handling utility methods that are used across the
mlcvzoo_mmdetection package.
"""

import logging
from typing import Any, Dict, Optional

from mmengine.config import Config

from mlcvzoo_mmdetection.configuration import MMConfig

logger = logging.getLogger(__name__)


def init_mmdetection_config(
    config_path: str,
    cfg_options: Optional[Dict[str, Any]] = None,
) -> Config:
    """
    Note: This function is deprecated and will be removed in future versions. Please use
    'mlcvzoo_mmdetection.utils.init_mm_config' instead.

    Initialize an mmengine.config.Config object from a given mmdetection .py config file.

    Args:
        config_path: Filepath of the mmdetection .py config file.
        cfg_options: Overwrite / additional options to load into the mmengine Config object.

    Returns:
        The mmengine Config object.
    """
    logger.warning(
        "DeprecationWarning: 'mlcvzoo_mmdetection.utils.init_mmdetection_config' "
        "is deprecated and will be removed in future versions. Please use "
        "'mlcvzoo_mmdetection.utils.init_mm_config' instead."
    )

    return init_mm_config(
        mm_config=MMConfig(config_path=config_path, cfg_options=cfg_options)
    )


def init_mm_config(mm_config: MMConfig) -> Config:
    """
    Initialize an mmengine.config.Config object from a given mmlcvzoo_mmdetection.configuration.MMConfig
    object. Currently, the object can be initialized from its mmdetection .py config file as well as from a python
    dictionary. Please note that initialization from .py config files will be removed in future releases (cf.
    documentation for 'mlcvzoo_mmdetection.utils.init_mmdetection_config'.

    Args:
        mm_config: The MMConfig object.

    Returns:
        The mmengine Config object.
    """
    if mm_config.config_path is not None:
        # Build config from .py configuration file
        logger.info(
            "Load mmdetection config from config-path: %s", mm_config.config_path
        )
        cfg = Config.fromfile(mm_config.config_path)
    elif mm_config.config_dict is not None:
        logger.info(
            "Load mmdetection config from config-dict: %s", mm_config.config_dict
        )
        cfg = Config(cfg_dict=mm_config.config_dict)
    else:
        raise ValueError(
            "Can not build mmengine config, either config-path or config-dict have to be"
            "provided in mm_config"
        )

    if mm_config.cfg_options:
        cfg.merge_from_dict(mm_config.cfg_options)

    return cfg


def modify_config(config_path: str, string_replacement_map: Dict[str, str]) -> str:
    """
    Note: This function is deprecated and will be removed in future versions.

    Load a mmdetection .py config file via its filepath and replace all matching keys
    (= placeholder / environment variables) in the file with their corresponding values in the string_replacement_map.
    The replaced file content is then stored in a *_local.py file in the same directory.

    Args:
        config_path: Path to the .py config file.
        string_replacement_map: Dictionary with string replacement values, e.g.
                                {"PROJECT_ROOT_DIR": "your/local/project/dir"}

    Returns:
        The filepath of the modified *_local.py file.
    """
    with open(file=config_path, mode="r", encoding="'utf-8") as config_file:
        config_file_content = config_file.readlines()

    new_config_file_content = list()
    for config_content in config_file_content:
        new_config_content = config_content

        for replacement_key, replacement_value in string_replacement_map.items():
            if replacement_key in config_content:
                new_config_content = new_config_content.replace(
                    replacement_key, replacement_value
                )

                logger.info(
                    "Replace '%s' in config-line '%s' with '%s'",
                    replacement_key,
                    new_config_content,
                    replacement_value,
                )

        new_config_file_content.append(new_config_content)

    new_config_path = config_path.replace(".py", "_local.py")
    with open(file=new_config_path, mode="w+", encoding="'utf-8") as new_config_file:
        new_config_file.writelines(new_config_file_content)

    return new_config_path
