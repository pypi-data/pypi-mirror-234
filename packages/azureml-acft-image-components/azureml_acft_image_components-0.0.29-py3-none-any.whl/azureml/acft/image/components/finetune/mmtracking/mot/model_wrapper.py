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

"""MMtracking multi-object tracking model wrapper class."""


import numpy as np
import os
import shutil
import torch

from mmcv import Config
from pathlib import Path
from torch import nn, Tensor
from torch.nn.utils.rnn import pad_sequence
from typing import Dict, List, Union, Any, Tuple, OrderedDict

from azureml.acft.common_components import get_logger_app, ModelSelectorDefaults
from azureml.acft.image.components.finetune.common.mlflow.common_utils import get_current_device
from azureml.acft.image.components.finetune.mmtracking.common.constants import (
    MmTrackingDatasetLiterals,
)
from azureml.acft.image.components.finetune.mmdetection.object_detection.model_wrapper import (
    ObjectDetectionModelWrapper,
)
from azureml.acft.image.components.model_selector.constants import ImageModelSelectorConstants
from azureml.metrics.vision.track_eval.azureml_mot_metrics import AzureMlMOTODMetrics
from azureml.metrics import list_metrics

logger = get_logger_app(__name__)


class MultiObjectTrackingModelWrapper(ObjectDetectionModelWrapper):
    """Wrapper class over multi-object tracking model of MMTracking framework."""

    def __init__(
        self,
        mm_multi_object_tracking_model: nn.Module,
        config: Config,
        model_name_or_path: str,
        task_type: str,
        num_labels: int,
        box_score_threshold: int,
        iou_threshold: int,
        meta_file_path: str,
    ):
        """Wrapper class over multi_object_tracking model of MMTracking.
        :param mm_multi_object_tracking_model: MM multi_object_tracking model
        :type mm_multi_object_tracking_model: nn.Module
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
        super().__init__(
            mm_multi_object_tracking_model,
            config,
            model_name_or_path,
            task_type,
            num_labels,
            box_score_threshold,
            iou_threshold,
            meta_file_path
        )
        metrics_list = list_metrics(task_type)
        self.metrics_computer = AzureMlMOTODMetrics(
            num_classes=num_labels,
            iou_threshold=iou_threshold,
            metrics=metrics_list,
        )

    def _rescale_groundtruth_bboxes(self, img_metas, gt_bboxes):
        """
        Rescale ground truth bounding boxes according to image meta info.
         In the forward call, we have rescaled the output to the original size of the image,
         this is to enable tracking results in different frames could be connected and evaluated.
         The groundtruths, however, are changed due to data augmentation, so we need to rescale them back.

        :param img_metas: image meta info
        :type img_metas: list of dict
        :param gt_bboxes: ground truth bboxes
        :type gt_bboxes: list of tensor
        :return: rescaled ground truth bboxes
        :rtype: list of tensor
        """
        scale_factors = np.array([img_meta['scale_factor'] for img_meta in img_metas])
        gt_bboxes[0] /= gt_bboxes[0].new_tensor(scale_factors)
        return gt_bboxes

    def _organize_track_ground_truths_for_evaluation(self, gt_bboxes: List[Tensor],
                                                     gt_labels: List[Tensor],
                                                     gt_crowds: List[Tensor],
                                                     gt_instance_ids: List[Tensor]) -> Tuple[List[Dict], List[Dict]]:
        """
        Organize the batch of ground truth as required by the azureml-metrics package for MOTA calculations.
        :param gt_bboxes: batch of ground truth bounding boxes
        :type gt_bboxes: list of tensor
        :param gt_labels: batch of ground truth class labels
        :type gt_labels: list of tensor
        :param gt_crowds: batch of ground truth crowds flag
        :type gt_crowds: list of tensor
        :param gt_instance_ids: batch of ground truth instance ids
        :type gt_instance_ids: list of tensor
        :return: Dict of ground truth labels in Tensor type
        :rtype: Dict[str, Tensor]
        """
        bboxes_ignore = np.zeros((0, 4), dtype=np.float32)  # temp workaround for bboxes_ignore
        track_gts = dict(bboxes=gt_bboxes[0].cpu().numpy(),
                         labels=gt_labels[0].cpu().numpy(),
                         bboxes_ignore=bboxes_ignore,
                         instance_ids=gt_instance_ids[0].cpu().numpy()
                         )
        return track_gts

    def forward(self, **data) -> Union[Dict[str, Any], Tuple[Tensor, Tuple]]:
        """
        Model forward pass for training and validation mode
        :param data: Input data to model
        :type data: Dict
        :return: A dictionary of loss components in training mode OR Tuple of dictionary of predicted and ground
        labels in validation mode
        :rtype: Dict[str, Any] in training mode; Tuple[Tensor, Dict[str, Tensor]] in validation mode;

        Note: Input data dictionary consist of
            img: Tensor of shape (N, C, H, W) encoding input images.
            img_metas: list of image info dict where each dict has: 'img_shape', 'scale_factor', 'flip',
             and may also contain 'filename', 'ori_shape', 'pad_shape', and 'img_norm_cfg'. For details on the values
             of these keys see `mmdet/datasets/pipelines/formatting.py:Collect`.
            gt_bboxes - list of tensor, ground truth bboxes for each image with shape (num_gts, 4)
                            in [tl_x, tl_y, br_x, br_y] format.
            gt_labels - List of tensor, class indices corresponding to each box
            gt_instance_ids - List of tensor, instance ids corresponding to each box (validation only)
            gt_bboxes_ignore - List of "is crowds" (boolean) to each box

        Example:
            data = {"img": np.random.randint(0, 255, size = (1, 3, 800, 1440)),
                    "gt_bboxes": [torch.tensor([[  0.,   0., 100., 100.], [135, 170, 220, 260]])],
                    "gt_labels": [torch.tensor([0, 0])],
                    "gt_bboxes_ignore": [torch.tensor([False, False])],
                    "gt_instance_ids": [torch.tensor([0, 1]))], # validation only
                    "img_metas": [{'img_shape': [800, 1440, 3], 'ori_shape': [1080, 1920, 3),
                                    scale_factor': [0.7, 0.6, 0.5, 0.3], 'flip': False,
                                    'filename': 'test.jpg', 'pad_shape': [800, 1440, 3],
                                    'img_norm_cfg': {'mean': [123.675, 116.28, 103.53],
                                                     'std': [58.395, 57.12, 57.375], 'to_rgb': True}},
                                    'frame_id': 0, "video_name": "test.mp4"}]
                    }

        """
        # removing dummy_labels for forward calls
        dummy_labels = data.pop(MmTrackingDatasetLiterals.DUMMY_LABELS, None)
        if self.model.training:
            # GT_CROWDS is not required for training
            data.pop(MmTrackingDatasetLiterals.GT_CROWDS)
            return self.model.detector.train_step(data, optimizer=None)
        else:
            img = data.pop(MmTrackingDatasetLiterals.IMG)
            img = [i.unsqueeze(0).to(get_current_device()) for i in img]
            img_metas = data.pop(MmTrackingDatasetLiterals.IMG_METAS)
            gt_bboxes = data.pop(MmTrackingDatasetLiterals.GT_BBOXES)
            gt_labels = data.pop(MmTrackingDatasetLiterals.GT_LABELS)
            gt_crowds = data.pop(MmTrackingDatasetLiterals.GT_CROWDS)
            gt_instance_ids = data.pop(MmTrackingDatasetLiterals.GT_INSTANCE_IDS)

            # organize ground truth for evaluation
            gt_bboxes = self._rescale_groundtruth_bboxes(img_metas, gt_bboxes)
            od_gts, od_img_meta_infos = self._organize_ground_truths_for_evaluation(gt_bboxes, gt_labels, gt_crowds)
            track_gts = self._organize_track_ground_truths_for_evaluation(
                gt_bboxes, gt_labels, gt_crowds, gt_instance_ids)

            # organize predictions for evaluation
            batch_predictions = self.model(
                img=img, img_metas=[img_metas], return_loss=False, rescale=True)
            track_predictions = batch_predictions[MmTrackingDatasetLiterals.TRACKING_BBOXES]
            det_predictions = batch_predictions[MmTrackingDatasetLiterals.DETECTION_BBOXES]
            od_predictions: dict = self._organize_predictions_for_evaluation([det_predictions])

            self.metrics_computer.update_states(od_gts, od_predictions, od_img_meta_infos,
                                                track_gts, track_predictions, img_metas)

            dummy_loss = torch.asarray([]).to(get_current_device())
            dummy_labels = torch.asarray([]).to(get_current_device())
        return dummy_loss, dummy_labels  # output
