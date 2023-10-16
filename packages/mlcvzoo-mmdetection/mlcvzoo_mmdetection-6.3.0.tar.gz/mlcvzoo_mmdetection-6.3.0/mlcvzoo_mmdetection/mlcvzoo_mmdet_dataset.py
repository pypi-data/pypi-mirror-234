# Copyright Open Logistics Foundation
#
# Licensed under the Open Logistics Foundation License 1.3.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: OLFL-1.3

"""
Module for providing the possibility to train a mmdetection
model on data that is provided by the annotation handler
of the MLCVZoo. This is realized by extending the 'DATASETS'
registry of mmdetection.
"""

import logging
import os
from typing import Any, Dict, List, Optional

from mlcvzoo_base.api.data.annotation import BaseAnnotation
from mlcvzoo_base.configuration.annotation_handler_config import AnnotationHandlerConfig
from mlcvzoo_base.configuration.class_mapping_config import ClassMappingConfig
from mlcvzoo_base.data_preparation.annotation_handler import AnnotationHandler
from mmdet.datasets.base_det_dataset import BaseDetDataset
from mmengine.config import Config
from related import to_model

logger = logging.getLogger(__name__)


class MLCVZooMMDetDataset(BaseDetDataset):
    """
    Implementation of a custom dataset. It follows the instructions given by:
    https://mmdetection.readthedocs.io/en/dev-3.x/advanced_guides/customize_dataset.html

    We followed an example and created our own dataset class
    which has to be compatible to the class "BaseDataset"
    of the mmdetection framework.

    Annotation format required from mmengine.dataset.base_dataset.BaseDataset:
    .. code-block:: none

        {
            "metainfo":
            {
              "dataset_type": "test_dataset",
              "task_name": "test_task"
            },
            "data_list":
            [
              {
                "img_path": "test_img.jpg",
                "height": 604,
                "width": 640,
                "instances":
                [
                  {
                    "bbox": [0, 0, 10, 20],
                    "bbox_label": 1,
                    "mask": [[0,0],[0,10],[10,20],[20,0]],
                    "extra_anns": [1,2,3]
                  },
                  {
                    "bbox": [10, 10, 110, 120],
                    "bbox_label": 2,
                    "mask": [[10,10],[10,110],[110,120],[120,10]],
                    "extra_anns": [4,5,6]
                  }
                ]
              },
            ]
        }

    """

    def __init__(
        self,
        *args: Any,
        annotation_handler_config: Optional[Config] = None,
        class_mapping_config: Optional[Config] = None,
        include_segmentation_as_bbox: bool = False,
        **kwargs: Any,
    ) -> None:
        self.annotations: List[BaseAnnotation] = []
        self.CLASSES: List[str] = []

        self._include_segmentation_as_bbox = include_segmentation_as_bbox

        if annotation_handler_config is not None:
            # Set annotation handler configuration from given annotation handler config
            configuration = to_model(AnnotationHandlerConfig, annotation_handler_config)
            # Set class mapping configuration from given class mapping config
            if class_mapping_config is not None:
                configuration.class_mapping = to_model(
                    ClassMappingConfig, class_mapping_config
                )
            # Create annotation handler, if no class mapping config was given,
            # assume it is part of the config file
            annotation_handler = AnnotationHandler(
                configuration=configuration,
            )
            # Load annotations and model classes from annotation handler
            self.annotations = annotation_handler.parse_training_annotations()
            self.CLASSES = annotation_handler.mapper.get_model_class_names()

        self._with_bbox: bool = False
        self._with_mask: bool = False
        pipeline = kwargs.get("pipeline")
        if pipeline is not None:
            annotation_pipelines = [
                p for p in pipeline if p["type"] == "LoadAnnotations"
            ]

            # Handle with_seg if we need to train panoptic segmentation models
            # self.with_seg: bool
            if len(annotation_pipelines) > 0:
                _with_bbox: Optional[bool] = annotation_pipelines[0].get("with_bbox")
                if _with_bbox is not None:
                    self._with_bbox = _with_bbox
                _with_mask: Optional[bool] = annotation_pipelines[0].get("with_mask")
                if _with_mask is not None:
                    self._with_mask = _with_mask

        BaseDetDataset.__init__(self, *args, **kwargs)

    @staticmethod
    def __generate_summary_message(base_message: str, data_dict: Dict[str, int]) -> str:
        """
        Produce a data summary message

        Args:
            base_message: Header of the message
            data_dict: Dictionary containing the summary information

        Returns:
            The generated message
        """
        message = base_message.format(sum(data_dict.values())) + "\n"

        for key, value in data_dict.items():
            message += f"{str(value).rjust(10)} | {str(key)}\n"

        return message

    def load_data_list(self) -> List[Dict[str, Any]]:
        data_list: List[Dict[str, Any]] = []
        bbox_data_dict: Dict[str, int] = {}
        segmentation_data_dict: Dict[str, int] = {}

        # TODO: Handle ignore flag if present in kwargs
        for img_id, annotation in enumerate(self.annotations):
            if not os.path.isfile(annotation.image_path):
                logger.debug(
                    "Skip annotation with path='%s' since image='%s' does not exist",
                    annotation.annotation_path,
                    annotation.image_path,
                )
                continue

            instances: List[Dict[str, Any]] = []
            if self._with_bbox and not self._with_mask:
                # Object detection training - train only on bounding boxes
                for bounding_box in annotation.get_bounding_boxes(
                    include_segmentations=self._include_segmentation_as_bbox
                ):
                    instances.append(
                        {
                            "ignore_flag": 0,
                            "ignore": 0,
                            "bbox_label": bounding_box.class_id,
                            "bbox": bounding_box.box.to_list(dst_type=float),
                        }
                    )
                    if bounding_box.class_identifier.class_name not in bbox_data_dict:
                        bbox_data_dict[bounding_box.class_identifier.class_name] = 1
                    else:
                        bbox_data_dict[bounding_box.class_identifier.class_name] += 1
            # TODO: Allow to use bbox and mask for segmentation training?!
            # elif if self._with_bbox and self._with_mask:
            elif self._with_mask:
                # Segmentation training - train with masks and bounding boxes
                for segmentation in annotation.segmentations:
                    if segmentation.box is None:
                        box = segmentation.to_bounding_box().box
                    else:
                        box = segmentation.box

                    instances.append(
                        {
                            "ignore_flag": 0,
                            "ignore": 0,
                            "bbox_label": segmentation.class_id,
                            "bbox": box.to_list(dst_type=float),
                            "mask": segmentation.to_list(dst_type=float),
                            "polygon": segmentation.to_list(dst_type=float)[0],
                        }
                    )
                    if (
                        segmentation.class_identifier.class_name
                        not in segmentation_data_dict
                    ):
                        segmentation_data_dict[
                            segmentation.class_identifier.class_name
                        ] = 1
                    else:
                        segmentation_data_dict[
                            segmentation.class_identifier.class_name
                        ] += 1

            data_list.append(
                {
                    "img_path": annotation.image_path,
                    "img_id": img_id,
                    # TODO: How to prepare for panoptic segmentation?
                    "seg_map_path": None,
                    "height": annotation.get_height(),
                    "width": annotation.get_width(),
                    "instances": instances,
                }
            )

        if len(bbox_data_dict.values()) > 0:
            logger.info(
                MLCVZooMMDetDataset.__generate_summary_message(
                    base_message="MMDetection model will be trained using {} BBoxes:",
                    data_dict=bbox_data_dict,
                )
            )

        if len(segmentation_data_dict.values()) > 0:
            logger.info(
                MLCVZooMMDetDataset.__generate_summary_message(
                    base_message="MMDetection model will be trained using {} Segmentations: ",
                    data_dict=segmentation_data_dict,
                )
            )

        return data_list
