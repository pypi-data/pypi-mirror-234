# Copyright Open Logistics Foundation
#
# Licensed under the Open Logistics Foundation License 1.3.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: OLFL-1.3

"""
Model that wraps all segmentation models of mmdetection
"""
import logging
from typing import Any, Dict, List, Optional, Tuple, Union, cast

import numpy as np
import torch.nn
from mlcvzoo_base.api.data.annotation_class_mapper import AnnotationClassMapper
from mlcvzoo_base.api.data.box import Box
from mlcvzoo_base.api.data.class_identifier import ClassIdentifier
from mlcvzoo_base.api.data.segmentation import PolygonType, Segmentation
from mlcvzoo_base.api.interfaces import NetBased, Trainable
from mlcvzoo_base.api.model import SegmentationModel
from mlcvzoo_base.configuration.structs import ObjectDetectionBBoxFormats
from mlcvzoo_base.configuration.utils import (
    create_configuration as create_basis_configuration,
)
from mmdet.evaluation import INSTANCE_OFFSET
from mmdet.structures.det_data_sample import DetDataSample
from mmdet.structures.mask.structures import bitmap_to_polygon
from nptyping import Int, NDArray, Shape

from mlcvzoo_mmdetection.configuration import (
    MMDetectionConfig,
    MMDetectionInferenceConfig,
)
from mlcvzoo_mmdetection.model import MMDetectionModel

logger = logging.getLogger(__name__)

ImageType = NDArray[Shape["Height, Width, Any"], Int]


class MMSegmentationModel(
    MMDetectionModel[MMDetectionInferenceConfig],
    SegmentationModel[MMDetectionConfig, Union[str, ImageType]],
    NetBased[torch.nn.Module, MMDetectionInferenceConfig],
    Trainable,
):
    """
    Class for wrapping mmdetection segmentation models
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
        SegmentationModel.__init__(
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
        return cast(
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

    def __decode_mmdet_result(self, prediction: Any) -> List[Segmentation]:
        """
        Decode output of an object detection model from mmdetection

        Args:
            prediction: The result that the model has predicted

        Returns:
            The prediction as list of bounding boxes in MLCVZoo format
        """

        segmentations: List[Segmentation] = []

        if hasattr(prediction, "pred_panoptic_seg"):
            # Have a shape of (IMAGE_HEIGHT, IMAGE_WIDTH) with each pixel
            # stating the class of the segmentation
            pan_results = prediction.pred_panoptic_seg.sem_seg.cpu().numpy()[0]
            # Get the classes that are contained in this panoptic segmentation
            valid_indices = np.unique(pan_results)[::-1]
            # Since the panoptic result has an INSTANCE_OFFSET, we need to make
            # sure not to get the class-id which is equal to the number of classes
            legal_indices = valid_indices != self.num_classes
            valid_indices = valid_indices[legal_indices]
            pan_class_ids = np.array(
                [class_id % INSTANCE_OFFSET for class_id in valid_indices],
                dtype=np.int64,
            )
            # Using [None] index to match the shapes:
            # pan_results (H, W) => (1, H, W)
            # valid_indices (N) => (N, 1, 1)
            # panoptic_segmentations => (N, H, W) each dimension corresponds to a boolean mask
            #                                     for the specific 'valid' class
            panoptic_segmentations = pan_results[None] == valid_indices[:, None, None]

            for panoptic_segmentation, class_id in zip(
                panoptic_segmentations, pan_class_ids
            ):
                score = 1.0

                contours, with_hole = bitmap_to_polygon(panoptic_segmentation)

                segmentations.append(
                    Segmentation(
                        class_identifier=ClassIdentifier(
                            class_id=class_id,
                            class_name=self.mapper.map_annotation_class_id_to_model_class_name(
                                class_id=class_id
                            ),
                        ),
                        score=score,
                        # For now, we only take the first contour and don't expect
                        # segmentations to be split into multiple parts
                        polygon=cast(PolygonType, contours[0]),
                        difficult=False,
                        occluded=False,
                        content="",
                        box=None,
                    )
                )
        else:
            valid_indices = (
                prediction.pred_instances.scores
                > self.configuration.inference_config.score_threshold
            )

            # Filter results according to the determined valid indices
            valid_masks = prediction.pred_instances.masks[valid_indices]
            valid_bounding_boxes = prediction.pred_instances.bboxes[valid_indices]
            valid_class_ids = prediction.pred_instances.labels[valid_indices]
            valid_scores = prediction.pred_instances.scores[valid_indices]

            for i, (bbox, mask, class_id, score) in enumerate(
                zip(valid_bounding_boxes, valid_masks, valid_class_ids, valid_scores)
            ):
                np_mask = np.stack(mask.detach().cpu().numpy(), axis=0)
                contours, with_hole = bitmap_to_polygon(np_mask)

                np_bbox = bbox.cpu().numpy().astype(np.int32)
                class_id_int = int(class_id.cpu())

                # TODO: Add the 'box' parameter to build_segmentations to simplify the
                #       instantiation of the segmentations per class_identifier
                class_identifiers = (
                    self.mapper.map_model_class_id_to_output_class_identifier(
                        class_id=class_id_int
                    )
                )

                model_class_identifier = ClassIdentifier(
                    class_id=class_id_int,
                    class_name=self.mapper.map_annotation_class_id_to_model_class_name(
                        class_id=class_id_int
                    ),
                )

                for class_identifier in class_identifiers:
                    segmentations.append(
                        Segmentation(
                            class_identifier=class_identifier,
                            model_class_identifier=model_class_identifier,
                            score=float(score),
                            # For now, we only take the first contour and don't expect
                            # segmentations to be split into multiple parts
                            polygon=cast(PolygonType, contours[0]),
                            difficult=False,
                            occluded=False,
                            content="",
                            box=Box.init_format_based(
                                box_format=ObjectDetectionBBoxFormats.XYXY,
                                box_list=(np_bbox[0:4]),
                            ),
                        )
                    )

        return segmentations

    def predict(
        self, data_item: Union[str, ImageType]
    ) -> Tuple[Union[str, ImageType], List[Segmentation]]:
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

        return data_item, self.__decode_mmdet_result(
            prediction=self.inferencer(
                inputs=data_item, return_datasample=True, batch_size=1
            )["predictions"][0]
        )

    def predict_many(
        self, data_items: List[Union[str, ImageType]]
    ) -> List[Tuple[Union[str, ImageType], List[Segmentation]]]:
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

        prediction_list: List[Tuple[Union[str, ImageType], List[Segmentation]]] = []

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
    MMDetectionModel.run(MMSegmentationModel)
