# Copyright Open Logistics Foundation
#
# Licensed under the Open Logistics Foundation License 1.3.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: OLFL-1.3

"""
Definition of the MMDetectionConfig that is used to configure the MMDetectionModel.
"""

import logging
from typing import Any, Dict, Optional

import related
from attr import Factory, define
from config_builder import BaseConfigClass
from mlcvzoo_base.api.configuration import InferenceConfig, ModelConfiguration
from mlcvzoo_base.configuration.class_mapping_config import ClassMappingConfig
from mlcvzoo_base.configuration.reduction_mapping_config import ReductionMappingConfig

logger = logging.getLogger(__name__)


@define
class MMDetectionModelOverwriteConfig(BaseConfigClass):
    __related_strict__ = True
    num_classes: int = related.IntegerField()

    def check_values(self) -> bool:
        return self.num_classes >= 1


@define
class MMDetectionTrainArgparseConfig(BaseConfigClass):
    __related_strict__ = True
    # Gathering of all argparse parameter mmdetection/tools/train.py:

    # the dir to save logs and models
    work_dir: str = related.StringField()
    # train config file path
    config: Optional[str] = related.ChildField(cls=str, default=None, required=False)
    # enable automatic-mixed-precision training
    amp: bool = related.BooleanField(default=False)
    # enable automatically scaling LR
    auto_scale_lr: bool = related.BooleanField(required=False, default=False)
    # override some settings in the used config, the key-value pair '
    # 'in xxx=yyy format will be merged into config file. If the value to '
    # 'be overwritten is a list, it should be like key="[a,b]" or key=a,b '
    # 'It also allows nested list/tuple values, e.g. key="[(a,b),(c,d)]" '
    # 'Note that the quotation marks are necessary and that no white space '
    # 'is allowed.
    cfg_options: Optional[Dict[str, Any]] = related.ChildField(
        cls=dict, default=None, required=False
    )
    # job launcher
    launcher: str = related.StringField(default="none", required=False)

    # ======================================================================================
    # Parameters of the mmdetection/tools/train.py that are not used in mlcvzoo-mmdetection:
    #
    # If specify checkpoint path, resume from it, while if not
    # specify, try to auto resume from the latest checkpoint
    # in the work directory:
    # resume: str
    #
    # NOTE: The local_rank parameter will be set via the argparse argument
    #       in the training scripts.
    # When using PyTorch version >= 2.0.0, the `torch.distributed.launch`
    # will pass the `--local-rank` parameter to `tools/train.py` instead
    # of `--local_rank`:
    #
    # local_rank: int

    def check_values(self) -> bool:
        if self.config is not None:
            logger.warning(
                "configuration.train_config.argparse_config.config is deprecated and will be removed in "
                "future versions."
            )
        if self.cfg_options is not None:
            logger.warning(
                "configuration.train_config.argparse_config.cfg_options is deprecated and will be removed in "
                "future versions."
            )

        return self.launcher in ["none", "pytorch", "slurm", "mpi"]


@define
class MMDetectionDistributedTrainConfig(BaseConfigClass):
    """
    Definition of attributes needed to start a distributed training on multiple GPUs.
    It is leaned against the documentation of mmdetection:
    https://mmdetection.readthedocs.io/en/dev-3.x/user_guides/train.html?highlight=gpu


    TODO: Add this to the arc42 Documentation
    Launch multiple jobs simultaneously
    If you would like to launch multiple jobs on a single machine, e.g., 2 jobs of 4-GPU training
    on a machine with 8 GPUs, you need to specify different ports (29500 by default) for each job
    to avoid communication conflict.

    If you use dist_train.sh to launch training jobs, you can set the port in the commands.

    CUDA_VISIBLE_DEVICES=0,1,2,3 PORT=29500 ./tools/dist_train.sh ${CONFIG_FILE} 4
    CUDA_VISIBLE_DEVICES=4,5,6,7 PORT=29501 ./tools/dist_train.sh ${CONFIG_FILE} 4
    """

    __related_strict__ = True

    # Number of nodes, or the range of nodes in form <minimum_nodes>:<maximum_nodes>
    nnodes: str = related.StringField(default="1:1")

    # Number of workers per node; supported values: [auto, cpu, gpu, int]
    nproc_per_node = related.StringField(default="auto")

    # Rank of the node for multi-node distributed training.
    node_rank: int = related.IntegerField(default=0)

    # Synchronisation port for interprocess communication
    master_port: int = related.IntegerField(default=29500)

    # Synchronisation URI for interprocess communication
    master_address: str = related.StringField(default="localhost")


@define
class MMDetectionTrainConfig(BaseConfigClass):
    """
    argparse parameter from mmdetection/tools/train.py
    """

    __related_strict__ = True

    argparse_config: MMDetectionTrainArgparseConfig = related.ChildField(
        cls=MMDetectionTrainArgparseConfig
    )

    multi_gpu_config: Optional[MMDetectionDistributedTrainConfig] = related.ChildField(
        cls=MMDetectionDistributedTrainConfig,
        required=False,
    )


@define
class MMDetectionInferenceConfig(InferenceConfig):
    __related_strict__ = True

    config_path: Optional[str] = related.ChildField(
        cls=str, default=None, required=False
    )

    device_string: Optional[str] = related.StringField(required=False, default=None)

    reduction_class_mapping: Optional[ReductionMappingConfig] = related.ChildField(
        cls=ReductionMappingConfig, required=False, default=None
    )

    def check_values(self) -> bool:
        if self.config_path is None:
            logger.warning(
                "configuration.inference_config.config_path is deprecated and will be removed in "
                "future versions."
            )

        return 0.0 <= self.score_threshold <= 1.0


@define
class MMConfig(BaseConfigClass):
    __related_strict__ = True

    config_path: Optional[str] = related.ChildField(
        cls=str, default=None, required=False
    )

    config_dict: Optional[Dict[str, Any]] = related.ChildField(
        cls=dict, default=None, required=False
    )

    cfg_options: Optional[Dict[str, Any]] = related.ChildField(
        cls=dict, default=None, required=False
    )


@define
class MMDetectionConfig(ModelConfiguration):
    __related_strict__ = True

    class_mapping: ClassMappingConfig = related.ChildField(cls=ClassMappingConfig)

    inference_config: MMDetectionInferenceConfig = related.ChildField(
        cls=MMDetectionInferenceConfig
    )

    train_config: MMDetectionTrainConfig = related.ChildField(
        cls=MMDetectionTrainConfig
    )

    mm_config: MMConfig = related.ChildField(
        cls=MMConfig, default=Factory(MMConfig), required=False
    )
