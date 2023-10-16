# Copyright Open Logistics Foundation
#
# Licensed under the Open Logistics Foundation License 1.3.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: OLFL-1.3

"""
Model that wraps all objection detection models of mmdetection
"""
import logging
import typing
from typing import Dict, List, Optional, Tuple, Union

import numpy as np
import torch.nn
from mlcvzoo_base.api.data.annotation_class_mapper import AnnotationClassMapper
from mlcvzoo_base.api.data.bounding_box import BoundingBox
from mlcvzoo_base.api.data.class_identifier import ClassIdentifier
from mlcvzoo_base.api.interfaces import NetBased, Trainable
from mlcvzoo_base.api.model import ObjectDetectionModel
from mlcvzoo_base.configuration.structs import ObjectDetectionBBoxFormats
from mlcvzoo_base.configuration.utils import (
    create_configuration as create_basis_configuration,
)
from mmdet.structures.det_data_sample import DetDataSample

from mlcvzoo_mmdetection.configuration import (
    MMDetectionConfig,
    MMDetectionInferenceConfig,
)
from mlcvzoo_mmdetection.model import ImageType, MMDetectionModel

logger = logging.getLogger(__name__)


class MMObjectDetectionModel(
    MMDetectionModel[MMDetectionInferenceConfig],
    ObjectDetectionModel[MMDetectionConfig, Union[str, ImageType]],
    NetBased[torch.nn.Module, MMDetectionInferenceConfig],
    Trainable,
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
        MMDetectionModel.__init__(
            self,
            configuration=self.create_configuration(
                from_yaml, configuration, string_replacement_map
            ),
            string_replacement_map=string_replacement_map,
            init_for_inference=init_for_inference,
            is_multi_gpu_instance=is_multi_gpu_instance,
        )
        ObjectDetectionModel.__init__(
            self,
            configuration=self.configuration,
            mapper=AnnotationClassMapper(
                class_mapping=self.configuration.class_mapping,
                reduction_mapping=self.configuration.inference_config.reduction_class_mapping,
            ),
            init_for_inference=init_for_inference,
        )
        NetBased.__init__(self, net=self.net)
        Trainable.__init__(self)

    @staticmethod
    def create_configuration(
        from_yaml: Optional[str] = None,
        configuration: Optional[MMDetectionConfig] = None,
        string_replacement_map: Optional[Dict[str, str]] = None,
    ) -> MMDetectionConfig:
        return typing.cast(
            MMDetectionConfig,
            create_basis_configuration(
                configuration_class=MMDetectionConfig,
                from_yaml=from_yaml,
                input_configuration=configuration,
                string_replacement_map=string_replacement_map,
            ),
        )

    @property
    def num_classes(self) -> int:
        return self.mapper.num_classes

    def get_classes_id_dict(self) -> Dict[int, str]:
        return self.mapper.annotation_class_id_to_model_class_name_map

    def __decode_mmdet_result(self, prediction: DetDataSample) -> List[BoundingBox]:
        """
        Decode output of an object detection model from mmdetection

        Args:
            prediction: The result that the model has predicted

        Returns:
            The decoded prediction as list of bounding boxes in MLCVZoo format
        """

        bounding_boxes: List[BoundingBox] = list()
        valid_indices = (
            prediction.pred_instances.scores
            > self.configuration.inference_config.score_threshold
        )

        # Filter results according to the determined valid indices
        valid_bounding_boxes = prediction.pred_instances.bboxes[valid_indices]
        valid_class_ids = prediction.pred_instances.labels[valid_indices]
        valid_scores = prediction.pred_instances.scores[valid_indices]

        for bbox, class_id, score in zip(
            valid_bounding_boxes, valid_class_ids, valid_scores
        ):
            bbox_int = bbox.cpu().numpy().astype(np.int32)
            class_id_int = int(class_id.cpu())

            bounding_boxes.extend(
                self.build_bounding_boxes(
                    box_format=ObjectDetectionBBoxFormats.XYXY,
                    box_list=(bbox_int[0:4]),
                    class_identifiers=self.mapper.map_model_class_id_to_output_class_identifier(
                        class_id=class_id_int
                    ),
                    model_class_identifier=ClassIdentifier(
                        class_id=class_id_int,
                        class_name=self.mapper.map_annotation_class_id_to_model_class_name(
                            class_id=class_id_int
                        ),
                    ),
                    score=float(score.cpu()),
                    difficult=False,
                    occluded=False,
                    content="",
                )
            )

        return bounding_boxes

    def predict(
        self, data_item: Union[str, ImageType]
    ) -> Tuple[Union[str, ImageType], List[BoundingBox]]:
        if self.net is None:
            raise ValueError(
                "The 'net' attribute is not initialized, "
                "make sure to instantiate with init_for_inference=True"
            )
        if self.inferencer is None:
            raise ValueError(
                "The 'inferencer' attribute is not initialized, "
                "make sure to instantiate with init_for_inference=True"
            )

        # For a single data_item we only have one prediction
        return data_item, self.__decode_mmdet_result(
            prediction=self.inferencer(
                inputs=data_item, return_datasample=True, batch_size=1
            )["predictions"][0]
        )

    def predict_many(
        self, data_items: List[Union[str, ImageType]]
    ) -> List[Tuple[Union[str, ImageType], List[BoundingBox]]]:
        if self.net is None:
            raise ValueError(
                "The 'net' attribute is not initialized, "
                "make sure to instantiate with init_for_inference=True"
            )
        if self.inferencer is None:
            raise ValueError(
                "The 'inferencer' attribute is not initialized, "
                "make sure to instantiate with init_for_inference=True"
            )

        prediction_list: List[Tuple[Union[str, ImageType], List[BoundingBox]]] = []

        # TODO: add batch-size as parameter
        predictions: List[DetDataSample] = self.inferencer(
            inputs=data_items,
            return_datasample=True,
            batch_size=len(data_items),
        )["predictions"]

        for data_item, prediction in zip(data_items, predictions):
            segmentations = self.__decode_mmdet_result(prediction=prediction)

            prediction_list.append(
                (
                    data_item,
                    segmentations,
                )
            )

        return prediction_list


if __name__ == "__main__":
    MMDetectionModel.run(MMObjectDetectionModel)
