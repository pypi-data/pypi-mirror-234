# Copyright Open Logistics Foundation
#
# Licensed under the Open Logistics Foundation License 1.3.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: OLFL-1.3

"""
Model that wraps all objection detection models of mmdetection
"""
from __future__ import annotations

import argparse
import inspect
import logging
import os
import shlex
import subprocess
import sys
from abc import ABC
from threading import Thread
from typing import IO, Any, Callable, Dict, Optional, TypeVar

import torch
import torch.nn
import yaml
from mlcvzoo_base.api.interfaces import NetBased, Trainable
from mlcvzoo_base.api.model import Model
from mmdet.apis.det_inferencer import DetInferencer
from mmdet.registry import DATASETS
from mmdet.utils import setup_cache_size_limit_of_dynamo
from mmengine.config import Config
from mmengine.runner import Runner, load_checkpoint
from nptyping import Int, NDArray, Shape

from mlcvzoo_mmdetection.configuration import (
    MMDetectionConfig,
    MMDetectionInferenceConfig,
)
from mlcvzoo_mmdetection.mlcvzoo_mmdet_dataset import MLCVZooMMDetDataset
from mlcvzoo_mmdetection.utils import init_mm_config, modify_config

logger = logging.getLogger(__name__)

ImageType = NDArray[Shape["Height, Width, Any"], Int]

MMDetectionInferenceConfigType = TypeVar(
    "MMDetectionInferenceConfigType", bound=MMDetectionInferenceConfig
)


class MMDetectionModel(
    Model[Any, Any, Any],
    NetBased[torch.nn.Module, MMDetectionInferenceConfigType],
    Trainable,
    ABC,
):
    """
    Class for wrapping mmdetection models
    """

    def __init__(
        self,
        from_yaml: Optional[str] = None,
        configuration: Optional[MMDetectionConfig] = None,
        string_replacement_map: Optional[Dict[str, str]] = None,
        init_for_inference: bool = False,
        is_multi_gpu_instance: bool = False,
    ) -> None:
        self.net: Optional[torch.nn.Module] = None
        self.inferencer: Optional[DetInferencer] = None

        self.yaml_config_path: Optional[str] = from_yaml
        self.is_multi_gpu_instance: bool = is_multi_gpu_instance

        self.configuration: MMDetectionConfig = self.create_configuration(
            from_yaml=from_yaml,
            configuration=configuration,
            string_replacement_map=string_replacement_map,
        )
        self.configuration.recursive_string_replacement(
            string_replacement_map=string_replacement_map
        )
        self._register_dataset()

        self.__update_mm_config(init_for_inference=init_for_inference)

        # config path to mmdetection specific .py file is set
        if self.configuration.mm_config.config_path:
            if string_replacement_map:
                self.configuration.mm_config.config_path = modify_config(
                    config_path=self.configuration.mm_config.config_path,
                    string_replacement_map=string_replacement_map,
                )

        self.cfg = init_mm_config(
            mm_config=self.configuration.mm_config,
        )

        self.__init_dataloader()
        Model.__init__(
            self,
            configuration=self.configuration,
            init_for_inference=init_for_inference,
        )
        NetBased.__init__(self, net=self.net)
        Trainable.__init__(self)

    def get_checkpoint_filename_suffix(self) -> str:
        return ".pth"

    def get_training_output_dir(self) -> str:
        return self.configuration.train_config.argparse_config.work_dir

    @staticmethod
    def _get_dataset_type() -> str:
        return "MLCVZooMMDetDataset"

    def get_net(self) -> Optional[torch.nn.Module]:
        return self.net

    def __update_mm_config(self, init_for_inference: bool) -> None:
        """
        Backward compatibility handling for self.configuration.mm_config.
        Update relevant attributes from deprecated parameters.

        Args:
            init_for_inference:  Whether to update the config for training or inference

        Returns:
            None
        """
        if init_for_inference:
            if self.configuration.mm_config.config_path is None:
                self.configuration.mm_config.config_path = (
                    self.configuration.inference_config.config_path
                )
        else:
            if self.configuration.mm_config.config_path is None:
                self.configuration.mm_config.config_path = (
                    self.configuration.train_config.argparse_config.config
                )

        if self.configuration.mm_config.cfg_options is None:
            self.configuration.mm_config.cfg_options = (
                self.configuration.train_config.argparse_config.cfg_options
            )

    def __init_dataloader(self) -> None:
        dataset_type = self._get_dataset_type()
        # TODO: Handle ConcatDataset => More than one dataset
        for data_loader in ["train_dataloader", "val_dataloader", "test_dataloader"]:
            if (
                data_loader in self.cfg
                and self.cfg[data_loader] is not None
                and self.cfg[data_loader].dataset.type == dataset_type
            ):
                if self.configuration.class_mapping is not None:
                    self.cfg[
                        data_loader
                    ].dataset.class_mapping_config = (
                        self.configuration.class_mapping.to_dict()
                    )

    def _init_inference_model(self) -> None:
        if self.net is None:
            self.inferencer = DetInferencer(
                self.cfg,
                weights=None,
                device=self.configuration.inference_config.device_string,
            )
            self.net = self.inferencer.model

            if self.configuration.inference_config.checkpoint_path != "":
                self.restore(
                    checkpoint_path=self.configuration.inference_config.checkpoint_path
                )

    def _init_training_model(self) -> None:
        # load config
        self.cfg.launcher = self.configuration.train_config.argparse_config.launcher
        self.cfg.experiment_name = self.unique_name
        # We always define the work_dir in the configuration file
        self.cfg.work_dir = self.configuration.train_config.argparse_config.work_dir

        # enable automatic-mixed-precision training
        if self.configuration.train_config.argparse_config.amp is True:
            optim_wrapper = self.cfg.optim_wrapper.type
            if optim_wrapper == "AmpOptimWrapper":
                logger.warning(
                    "AMP training is already enabled in your config.",
                )
            else:
                assert optim_wrapper == "OptimWrapper", (
                    "`--amp` is only supported when the optimizer wrapper type is "
                    f"`OptimWrapper` but got {optim_wrapper}."
                )
                self.cfg.optim_wrapper.type = "AmpOptimWrapper"
                self.cfg.optim_wrapper.loss_scale = "dynamic"

        # enable automatically scaling LR
        if self.configuration.train_config.argparse_config.auto_scale_lr:
            if (
                "auto_scale_lr" in self.cfg
                and "enable" in self.cfg.auto_scale_lr
                and "base_batch_size" in self.cfg.auto_scale_lr
            ):
                self.cfg.auto_scale_lr.enable = True
            else:
                raise RuntimeError(
                    'Can not find "auto_scale_lr" or '
                    '"auto_scale_lr.enable" or '
                    '"auto_scale_lr.base_batch_size" in your'
                    " configuration file."
                )

    def store(self, checkpoint_path: str) -> None:
        pass

    def restore(self, checkpoint_path: str) -> None:
        if self.net is None:
            raise ValueError(
                "In order to restore a checkpoint, the net attribute has"
                "to be initialized!"
            )

        logger.info(
            "Load model for %s from %s",
            self.unique_name,
            checkpoint_path,
        )

        checkpoint = load_checkpoint(
            self.net,
            checkpoint_path,
            map_location="cpu",
        )

        if "CLASSES" in checkpoint.get("meta", {}):
            self.net.CLASSES = checkpoint["meta"]["CLASSES"]

    def save_reduced_checkpoint(
        self, input_checkpoint_path: str, output_checkpoint_path: str
    ) -> None:
        """
        Saves a reduced version of a stored checkpoint that does not contain optimizer states
        anymore. Therefore, it keeps the weights and meta information of the source checkpoint.

        Args:
            input_checkpoint_path: Path to source checkpoint file
            output_checkpoint_path: Path to where the checkpoint is saved
        """

        runner = MMDetectionModel._build_runner(cfg=self.cfg)

        # Load input checkpoint dict from and extract the metadata for the output checkpoint.
        # Save reduced checkpoint with metadata of full checkpoint to target directory.
        runner.save_checkpoint(
            out_dir=os.path.dirname(output_checkpoint_path),
            filename=os.path.basename(output_checkpoint_path),
            save_optimizer=False,
            save_param_scheduler=False,
            meta=runner.load_checkpoint(filename=input_checkpoint_path)["meta"],
        )

        logger.info(
            "Saved checkpoint from '%s' in a reduced version to '%s'.",
            input_checkpoint_path,
            output_checkpoint_path,
        )

    def train(self) -> None:
        if (
            self.configuration.train_config.multi_gpu_config is None
            or "LOCAL_RANK" in os.environ
        ):
            # Don't start a distributed training if called without a multi GPU config,
            # or run as a worker via torch.distributed as indicated by the presence of a local rank
            logger.info("Training model")
            self._train()
        else:
            logger.info("Training distributed model")
            self._train_multi_gpu()

    @staticmethod
    def _register_dataset() -> None:
        """
        Register the custom dataset of the MLCVZoo in the registry of mmcv

        Returns:
            None
        """
        DATASETS.register_module(
            MLCVZooMMDetDataset.__name__, module=MLCVZooMMDetDataset, force=True
        )

    def _train_multi_gpu(
        self,
    ) -> None:
        """
        Run mmdet multi-gpu/distributed training.

        Returns:
            None
        """
        if self.configuration.train_config.multi_gpu_config is None:
            raise RuntimeError("No multi GPU config provided")

        distributed_model_config_path = os.path.join(
            self.get_training_output_dir(),
            "{}-worker.yaml".format(self.configuration.unique_name),
        )
        os.makedirs(os.path.dirname(distributed_model_config_path), exist_ok=True)
        with open(distributed_model_config_path, "w+") as yaml_file:
            self.configuration.to_yaml(
                yaml_package=yaml, dumper_cls=yaml.Dumper, stream=yaml_file
            )

        command = (
            f"{sys.executable} -u "
            "-m torch.distributed.run "
            f"--nproc_per_node={self.configuration.train_config.multi_gpu_config.nproc_per_node} "
            f"--master_port={self.configuration.train_config.multi_gpu_config.master_port} "
            f"--master_addr={self.configuration.train_config.multi_gpu_config.master_address} "
            f"--nnodes={self.configuration.train_config.multi_gpu_config.nnodes} "
            f"--node_rank={self.configuration.train_config.multi_gpu_config.node_rank} "
            f"{inspect.getfile(self.__class__)} "
            f"{distributed_model_config_path} "
        )

        subproc_env = dict(os.environ.copy())
        subproc_env["LOGLEVEL"] = "INFO"

        logger.debug("Run command: %s", command)
        result = subprocess.Popen(
            shlex.split(command),
            env=subproc_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=False,
        )
        Thread(
            target=self.__pipe_to_log, args=[result.stdout, logging.INFO], daemon=True
        ).start()
        result.wait()

        if result.returncode:
            logger.error(
                "Command '%s' returned with exit code %i", command, result.returncode
            )
            raise RuntimeError(
                f"Distributed training exited with exitcode != 0, "
                f"exitcode: {result.returncode}"
            )

    @staticmethod
    def __pipe_to_log(pipe: IO[bytes], level: int) -> None:
        with pipe:
            for line in iter(pipe.readline, b""):  # b'\n'-separated lines
                logger.log(level, "Subprocess: %r", line.decode("utf-8").strip())

    @staticmethod
    def _build_runner(cfg: Config) -> Runner:
        from mmengine.registry import RUNNERS

        # build the runner from config
        if "runner_type" not in cfg:
            # build the default runner
            runner = Runner.from_cfg(cfg)
        else:
            # build customized runner from the registry
            # if 'runner_type' is set in the cfg
            runner = RUNNERS.build(cfg)

        return runner

    def _train(
        self,
    ) -> None:
        # Reduce the number of repeated compilations and improve
        # training speed.
        setup_cache_size_limit_of_dynamo()

        runner = MMDetectionModel._build_runner(cfg=self.cfg)

        # start training
        runner.train()

    @staticmethod
    def run(model_class: Callable) -> None:  # type: ignore[type-arg]
        """
        Run training with given model subclass, reading a config from file.
        This function is intended to be called during torch.distributed.run via subclass main
        functions. It expects a single command line parameter called "yaml_config_path" pointing
        to a valid YAML configuration file for the given model subclass.

        Args:
            model_class: the subclass of model.MMDetectionModel to train
        """
        parser: argparse.ArgumentParser = argparse.ArgumentParser()
        parser.add_argument(
            "yaml_config_path",
            help="Load all parameters from the given yaml configuration file",
            type=str,
        )

        args = parser.parse_args()

        mmdet_model = model_class(
            from_yaml=args.yaml_config_path,
            init_for_inference=False,
        )
        mmdet_model.train()
