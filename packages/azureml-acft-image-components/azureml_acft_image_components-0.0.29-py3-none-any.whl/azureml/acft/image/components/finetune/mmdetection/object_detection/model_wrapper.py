# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
# Copyright 2018-2023 OpenMMLab. All rights reserved.
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

"""MMdetection object detection model wrapper class."""


import numpy as np
import os
import shutil
import torch

from mmcv import Config
from pathlib import Path
from torch import nn, Tensor
from typing import Dict, List, Union, Any, Tuple, OrderedDict

from azureml.acft.common_components import get_logger_app, ModelSelectorDefaults
from azureml.acft.image.components.finetune.common.mlflow.common_utils import get_current_device
from azureml.acft.image.components.finetune.defaults.constants import TrainingDefaultsConstants
from azureml.acft.image.components.finetune.mmdetection.common.constants import (
    MmDetectionDatasetLiterals,
    MmDetectionConfigLiterals
)
from azureml.acft.image.components.finetune.common.constants.constants import DetectionDatasetLiterals
from azureml.acft.image.components.finetune.common.mlflow.common_constants import MetricsLiterals
from azureml.acft.image.components.model_selector.constants import ImageModelSelectorConstants
from azureml.metrics.vision.od_is_eval.azureml_od_is_metrics import AzureMLODISMetrics
from azureml.metrics.constants import Tasks as MetricsTasks
from azureml.metrics import list_metrics


logger = get_logger_app(__name__)


class ObjectDetectionModelWrapper(nn.Module):
    """Wrapper class over object detection model of MMDetection framework."""

    def __init__(
        self,
        mm_object_detection_model: nn.Module,
        config: Config,
        model_name_or_path: str,
        task_type: str,
        num_labels: int,
        box_score_threshold: int,
        iou_threshold: int,
        meta_file_path: str = None,
    ):
        """Wrapper class over object detection model of MMDetection.
        :param mm_object_detection_model: MM object detection model
        :type mm_object_detection_model: nn.Module
        :param config: MM Detection model configuration
        :type config: MMCV Config
        :param model_name_or_path: model name or path
        :type model_name_or_path: str
        :param task_type: Task type either of Object Detection or Instance Segmentation
        :type task_type: str
        :param num_labels: Number of ground truth classes in the dataset
        :type num_labels: int
        :param box_score_threshold: Threshold for bounding box score
        :type box_score_threshold: float
        :param iou_threshold: Threshold for IoU(intersection over union)
        :type iou_threshold: float
        :param meta_file_path: path to meta file
        :type meta_file_path: str
        """
        super().__init__()
        self.model = mm_object_detection_model
        self.config = config
        self.model_name = Path(model_name_or_path).stem
        self.meta_file_path = meta_file_path
        self.box_score_threshold = box_score_threshold

        if os.path.isdir(model_name_or_path):
            self.model_path = model_name_or_path
        else:
            self.model_path = os.path.dirname(model_name_or_path)

        self.model_defaults_path = os.path.join(self.model_path, TrainingDefaultsConstants.MODEL_DEFAULTS_FILE)

        metrics_list = list_metrics(task_type)
        self.metrics_computer = AzureMLODISMetrics(
            task_is_detection=bool(task_type == MetricsTasks.IMAGE_OBJECT_DETECTION),
            num_classes=num_labels,
            iou_threshold=iou_threshold,
            metrics=metrics_list,
        )

    @classmethod
    def _get_bboxes_and_labels(
        cls, predicted_bbox: List[List[np.ndarray]]
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Map the MM detection model's predicted label to the bboxes and labels
        :param predicted_bbox: bbox of shape [Number of labels, Number of boxes, 5 [tl_x, tl_y, br_x, br_y,
        box_score]] format.
        :type predicted_bbox: List[List[np.ndarray]]
        :return: bounding boxes of shape [Number of boxes, 5 [tl_x, tl_y, br_x, br_y, box_score]] and labels of
        shape [Number of boxes, label id]
        :rtype: Tuple[np.ndarray, np.ndarray]

        Sample input: [[
            np.array([[11, 2, 24, 58, 0.03], [9, 4, 24, 55, 0.9]]),
            np.array([[8, 2, 23, 59, 0.5]]),
            np.empty(shape=(0, 5)),
            np.empty(shape=(0, 5)),
        ], [
            np.empty(shape=(0, 5)),
            np.empty(shape=(0, 5)),
            np.array([[13, 27, 276, 452, 0.75]]),
            np.empty(shape=(0, 5)),
        ]]

        Sample output: ([
            np.array([[11, 2, 24, 58, 0.03], [9, 4, 24, 55, 0.9], [8, 2, 23, 59, 0.5]]),
            np.array([[13, 27, 276, 452, 0.75]])
        ],
        # Labels(classes) for each bbox in the batch (0th image has 3 bboxes and 1st image has 1 bbox)
        [np.array([0, 0, 1]),np.array([2])]
        )
        """
        bboxes = np.vstack(predicted_bbox)
        labels = [
            np.full(bbox.shape[0], i, dtype=np.int32)
            for i, bbox in enumerate(predicted_bbox)
        ]
        labels = np.concatenate(labels)
        return bboxes, labels

    def get_valid_index(self, box_scores: np.ndarray) -> List[int]:
        """
        Get the index of valid bounding boxes i.e. box score above box score threshold
        :param box_scores: Optional, prediction score of bounding box
        :type box_scores: nd-array
        :return: index of valid labels
        :rtype: List

        Note: This helper function is used for preparing the model output before
        feeding to compute_metrics. (It returns the valid indices of predictions,
        we then filtered out the invalid bbox and masks).
        1. For prediction, It will only keep those indices for which
           the box scoring confidence >= box score threshold

        Sample Input: box_scores = np.array([0.03, 0.9, 0.5, 0.75])
        Sample Output: [1, 2, 3] // considering self.box_score_threshold = 0.5
        """

        if box_scores is not None:
            return [i for i, box_score in enumerate(box_scores)
                    if box_score >= self.box_score_threshold]
        return []

    def _organize_od_prediction_for_evaluation(self,
                                               predicted_bbox: List[np.ndarray]
                                               ) -> Tuple[Dict[str, np.ndarray], np.ndarray, List[int]]:
        """
        Organize predicted bounding box and labels in a format required by the compute method in azureml-metrics
        package.
        :param predicted_bbox: Predicted bounding box
        :type predicted_bbox: List[List[np.ndarray]]

        :return: Tuple of List of Transformed prediction as required by metrics compute function,
        List of labels and List of valid indices.
        :rtype: Tuple[Dict[str, np.ndarray], np.ndarray, List[int]]

        Sample input: [
                np.array([[11, 2, 24, 58, 0.03], [9, 4, 24, 55, 0.9]]),
                np.array([[8, 2, 23, 59, 0.5]]),
                np.empty(shape=(0, 5)),
                np.empty(shape=(0, 5),
        ],
        Sample output: ({
            DetectionDatasetLiterals.BOXES: np.array([[9, 4, 24, 55, 0.9], [8, 2, 23, 59, 0.5]]),
            MetricsLiterals.CLASSES: np.array([0, 1]),
            MetricsLiterals.SCORES: np.array([0.9, 0.5])
        },
            np.array([0, 1]),
            [1, 2]
        )
        """
        bboxes, labels = self._get_bboxes_and_labels(predicted_bbox)
        keep_index = self.get_valid_index(bboxes[:, 4])
        output = {
            DetectionDatasetLiterals.BOXES: bboxes[keep_index][:, :4],
            MetricsLiterals.CLASSES: labels[keep_index],
            MetricsLiterals.SCORES: bboxes[keep_index][:, 4]
        }
        return output, labels, keep_index

    def _organize_predictions_for_evaluation(
        self,
        batch_predictions: List
    ) -> List[Dict[str, np.ndarray]]:
        """
        This function transforms the predictions from HF trainer as required by the azureml-metrics function.
        It also filters out the predictions whose box score is under the box_score_threshold.
        :param predictions: model prediction containing bboxes, labels and masks
        :type predictions: Tuple
        :return: Transformed predictions as required by azureml-metrics compute method
        :rtype: List of prediction dictionary List[Dict[str, np.ndarray]]

        Sample input: [[
                np.array([[11, 2, 24, 58, 0.03], [9, 4, 24, 55, 0.9]]),
                np.array([[8, 2, 23, 59, 0.5]]),
                np.empty(shape=(0, 5), dtype=float32),
                np.empty(shape=(0, 5), dtype=float32)
            ], [
                np.empty(shape=(0, 5), dtype=float32),
                np.empty(shape=(0, 5), dtype=float32),
                np.array([[13, 27, 276, 452, 0.75]], dtype=float32),
                np.empty(shape=(0, 5), dtype=float32),
            ]
        ],
        Sample output: [{
            DetectionDatasetLiterals.BOXES: np.array([[9, 4, 24, 55, 0.9], [8, 2, 23, 59, 0.5]]),
            MetricsLiterals.CLASSES: np.array([0, 1]),
            MetricsLiterals.SCORES: np.array([0.9, 0.5])
        },{
            DetectionDatasetLiterals.BOXES: np.array([[13, 27, 276, 452, 0.75]]),
            DetectionDatasetLiterals.CLASSES: np.array([2]),
            DetectionDatasetLiterals.SCORES: np.array([0.75])
        }]
        """
        outputs = []
        for predicted_bbox in batch_predictions:
            output, _, _ = self._organize_od_prediction_for_evaluation(predicted_bbox)
            outputs.append(output)
        return outputs

    def _organize_ground_truths_for_evaluation(
        self,
        gt_bboxes: List[Tensor],
        gt_labels: List[Tensor],
        gt_crowds: List[Tensor]
    ) -> Tuple[List[Dict], List[Dict]]:
        """
        Organize the batch of ground truth as required by the azureml-metrics package for mAP calculations.
        :param gt_bboxes: batch of ground truth bounding boxes
        :type gt_bboxes: list of tensor
        :param gt_labels: batch of ground truth class labels
        :type gt_labels: list of tensor
        :param gt_crowds: batch of ground truth crowds flag
        :type gt_crowds: list of tensor
        :return: Dict of ground truth labels in Tensor type
        :rtype: Dict[str, Tensor]

        Sample input:
            gt_bboxes: [
                torch.tensor([[0, 0, 1, 1], [2, 2, 3, 3]]),
                torch.tensor([[0, 1, 3, 4]])
            ]
            gt_labels: torch.tensor([[0, 1], [0]])
            gt_crowds: torch.tensor([[False, False], [True]])

        Sample output: ([
            {
                DetectionDatasetLiterals.BOXES: np.array([[0, 0, 1, 1], [2, 2, 3, 3]]),
                MetricsLiterals.CLASSES: np.array([0, 1]),
            }, {
                DetectionDatasetLiterals.BOXES: np.array([[0, 1, 3, 4]]),
                MetricsLiterals.CLASSES: np.array([0]),
            }
        ],
        [   # Image Metas
            {DetectionDatasetLiterals.ISCROWD: np.array([False, False])},
            {DetectionDatasetLiterals.ISCROWD: np.array([True])}
        ])
        """
        batch_gt_bboxes = [gt_bbox.cpu().numpy() for gt_bbox in gt_bboxes]
        batch_gt_labels = [gt_label.cpu().numpy() for gt_label in gt_labels]
        batch_gt_crowds = [gt_crowd.cpu().numpy() for gt_crowd in gt_crowds]

        gts: List[Dict] = list()
        meta_infos: List[Dict] = list()
        for gt_bboxes, gt_labels, gt_crowds in zip(
            batch_gt_bboxes, batch_gt_labels, batch_gt_crowds
        ):
            ground_truth = {
                DetectionDatasetLiterals.BOXES: gt_bboxes,
                MetricsLiterals.CLASSES: gt_labels,
            }
            image_metadata = {DetectionDatasetLiterals.ISCROWD: gt_crowds}

            gts.append(ground_truth)
            meta_infos.append(image_metadata)
        return gts, meta_infos

    def forward(self, **data) -> Union[Dict[str, Any], Tuple[Tensor, Tensor]]:
        """
        Model forward pass for training and validation mode
        :param data: Input data to model
        :type data: Dict
        :return: A dictionary of loss components in training mode OR Tuple of dictionary of predicted and ground
        labels in validation mode
        :rtype: Dict[str, Any] in training mode; Tuple[Tensor, Tensor] in validation mode;

        Note: Input data dictionary consist of
            img: Tensor of shape (N, C, H, W) encoding input images.
            img_metas: list of image info dict where each dict has: 'img_shape', 'scale_factor', 'flip',
             and may also contain 'filename', 'ori_shape', 'pad_shape', and 'img_norm_cfg'. For details on the values
             of these keys see `mmdet/datasets/pipelines/formatting.py:Collect`.
            gt_bboxes - Ground truth bboxes for each image with shape (num_gts, 4) in [tl_x, tl_y, br_x, br_y] format.
            gt_labels - List of class indices corresponding to each box
            gt_crowds - List of "is crowds" (boolean) to each box
            gt_masks - List of masks (type BitmapMasks) for each image if task is instance_segmentation
        """
        # removing dummy_labels for forward calls
        dummy_labels = data.pop(MmDetectionDatasetLiterals.DUMMY_LABELS, None)
        if self.model.training:
            # GT_CROWDS is not required for training
            data.pop(MmDetectionDatasetLiterals.GT_CROWDS)
            return self.model.train_step(data, optimizer=None)
        else:
            img = data.pop(MmDetectionDatasetLiterals.IMG)
            img_metas = data.pop(MmDetectionDatasetLiterals.IMG_METAS)
            batch_predictions = self.model(
                img=[img], img_metas=[img_metas], return_loss=False
            )

            dummy_loss = torch.asarray([]).to(get_current_device())
            dummy_labels = torch.asarray([]).to(get_current_device())

            predictions = self._organize_predictions_for_evaluation(batch_predictions)
            gts, img_meta_infos = self._organize_ground_truths_for_evaluation(**data)
            self.metrics_computer.update_states(y_test=gts, image_meta_info=img_meta_infos, y_pred=predictions)
            # Returning dummy_loss, dummy_labels since HF-trainer eval step expects two outputs.
            return dummy_loss, dummy_labels

    def save_pretrained(self, output_dir: os.PathLike, state_dict: OrderedDict) -> None:
        """
        Save finetuned weights and model configuration
        :param output_dir: Output directory to store the model
        :type output_dir: os.PathLike
        :param state_dict: Model state dictionary
        :type state_dict: Dict
        """
        # TODO: Revisit the logic for resuming training from checkpoint. Taking user input in python script
        #  may not be a good idea from security perspective. Or, it may not affect as user machine is individual.
        os.makedirs(output_dir, exist_ok=True)
        torch.save(state_dict, os.path.join(output_dir, ModelSelectorDefaults.MODEL_CHECKPOINT_FILE_NAME))
        # saving the unwrapped version that can be directly used with mmd repo
        MMD_PATH = os.path.join(output_dir, ImageModelSelectorConstants.MMD_MODEL_CHECKPOINT_FILE_NAME)
        torch.save(
            {
                MmDetectionConfigLiterals.STATE_DICT : self.model.state_dict(),
                MmDetectionConfigLiterals.META : {
                    MmDetectionConfigLiterals.CLASSES : list(self.config.id2label.values())}
            }, MMD_PATH)
        self.config.dump(os.path.join(output_dir, self.model_name + ".py"))
        shutil.copy(self.meta_file_path,
                    os.path.join(output_dir, ImageModelSelectorConstants.MODEL_METAFILE_NAME))
        if os.path.isfile(self.model_defaults_path):
            shutil.copy(self.model_defaults_path,
                        os.path.join(output_dir, TrainingDefaultsConstants.MODEL_DEFAULTS_FILE))
        logger.info(f"Model saved at {output_dir}")
