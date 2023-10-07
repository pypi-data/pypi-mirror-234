# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""MMDetection modules."""

import torch
import numpy as np

from dataclasses import dataclass
from mmcv import Config, concat_list
from pathlib import Path
from torch import nn, Tensor
from torch.nn.utils.rnn import pad_sequence
from typing import Dict, List, Union, Any, Tuple
from common_constants import MmDetectionDatasetLiterals
from common_utils import get_current_device


@dataclass
class ImageMetadata:
    """Dataclass for maintaining the metadata dictionary as required for MM detection models.
    The keys of metadata dictionary is same as the property name."""

    ori_shape: Tuple[int, int, int]         # Dimension of the transformed image H x W x C. This is the shape of the
    # image after resizing and padding. If we set it to the original image shape i.e. shape before transformation
    # then the MMD model is not able to learn and the eval_mAP is always 0.0.
    img_shape: Tuple[int, int, int] = None  # Dimension of the image after ConstraintResize transformation.
    pad_shape: Tuple[int, int, int] = None  # Dimension of the tranformed image after padding. Please note that padding
    # is applied after ConstraintResize transformation, so pad_shape is always greater than or equal to img_shape.
    raw_dimensions: Tuple[int, int] = None   # Dimension of the raw image H x W. This is used to resize the predicted
    # mask to the original image size.
    scale_factor: np.ndarray = np.array([1, 1, 1, 1])
    flip: bool = False
    flip_direction: str = None
    filename: str = None
    ori_filename: str = None

    def __post_init__(self):
        """If image shape after resizing and padding is not provided then assign it with original shape"""
        self.img_shape = self.img_shape or self.ori_shape
        self.pad_shape = self.pad_shape or self.ori_shape


class ObjectDetectionModelWrapper(nn.Module):
    """Wrapper class over object detection model of MMDetection."""
    def __init__(
        self,
        mm_object_detection_model: nn.Module,
        config: Config,
        model_name_or_path: str = None,
    ):
        """Wrapper class over object detection model of MMDetection.

        :param mm_object_detection_model: MM object detection model
        :type mm_object_detection_model: nn.Module
        :param config: MM Detection model configuration
        :type config: MMCV Config
        :param model_name_or_path: model name or path
        :type model_name_or_path: str
        """

        super().__init__()
        self.model = mm_object_detection_model
        self.config = config
        self.model_name = Path(model_name_or_path).stem

    @classmethod
    def _get_bboxes_and_labels(
            cls, predicted_bbox: List[np.ndarray], img_meta: Dict
    ) -> Tuple[Tensor, Tensor]:
        """
        Map the MM detection model"s predicted label to the bbox and labels
        :param predicted_bbox: bbox of shape [Number of labels, Number of boxes, 5 [tl_x, tl_y, br_x, br_y,
        box_score]] format.
        :type predicted_bbox: List[np.ndarray]
        :param img_meta: Image metadata
        :type img_meta: Dict
        :return: bounding boxes of shape [Number of boxes, 5 [tl_x, tl_y, br_x, br_y, box_score]] and labels of
        shape [Number of boxes, label id]
        :rtype: Tuple[Tensor, Tensor]
        """
        bboxes = torch.as_tensor(np.vstack(predicted_bbox))
        height, width, _ = img_meta[MmDetectionDatasetLiterals.IMAGE_SHAPE]
        for bbox in bboxes:
            # Normalize bounding box
            bbox[0] = bbox[0] / width
            bbox[1] = bbox[1] / height
            bbox[2] = bbox[2] / width
            bbox[3] = bbox[3] / height

        labels = [
            np.full(bbox.shape[0], i, dtype=np.int32)
            for i, bbox in enumerate(predicted_bbox)
        ]
        labels = torch.as_tensor(np.concatenate(labels))
        return bboxes, labels

    @classmethod
    def _pad_sequence(cls, sequences: Tensor, padding_value: float = -1, batch_first: bool = True) -> Tensor:
        """
        It stacks a list of Tensors sequences, and pads them to equal length.
        :param sequences: list of variable length sequences.
        :type sequences: Tensor
        :param padding_value: value for padded elements
        :type padding_value: float
        :param batch_first: output will be in B x T x * if True, or in T x B x * otherwise
        :type batch_first: bool
        :return: Tensor of size ``B x T x *`` if batch_first is True
        :rtype: Tensor
        """
        rt_tensor = pad_sequence(sequences, padding_value=padding_value, batch_first=batch_first)
        rt_tensor = rt_tensor.to(device=get_current_device())
        return rt_tensor

    def _organize_predictions_for_trainer(
        self, batch_predictions: List[List[np.ndarray]], img_metas: List[Dict]
    ) -> Dict[str, Tensor]:
        """
        Transform the batch of predicted labels as required by the HF trainer.
        :param batch_predictions: batch of predicted labels
        :type batch_predictions: List of bbox list for each image
        :param img_metas: batch of predicted labels
        :type img_metas: List of image metadata dictionary
        :return: Dict of predicted labels in tensor format
        :rtype: Dict[str, Tensor]

        Note: Same reasoning like _organize_ground_truth_for_trainer function but for predicted label
        """
        batch_bboxes, batch_labels = [], []
        for prediction, img_meta in zip(batch_predictions, img_metas):
            bboxes, labels = ObjectDetectionModelWrapper._get_bboxes_and_labels(
                prediction, img_meta
            )
            batch_bboxes.append(bboxes)
            batch_labels.append(labels)

        output = dict()
        output[MmDetectionDatasetLiterals.BBOXES] = ObjectDetectionModelWrapper._pad_sequence(batch_bboxes)
        output[MmDetectionDatasetLiterals.LABELS] = ObjectDetectionModelWrapper._pad_sequence(batch_labels)
        return output

    def forward(
        self, **data
    ) -> Union[Dict[str, Any], Tuple[Tensor, Dict[str, Tensor]]]:
        """
        Model forward pass for training and validation mode
        :param data: Input data to model
        :type data: Dict
        :return: A dictionary of loss components in training mode OR Tuple of dictionary of predicted and ground
        labels in validation mode
        :rtype: Dict[str, Any] in training mode; Tuple[Tensor, Dict[str, Tensor]] in validation mode;

        Note: Input data dictionary consist of
            img: Tensor of shape (N, C, H, W) encoding input images.
            img_metas: list of image info dict where each dict has: "img_shape", "scale_factor", "flip",
             and may also contain "filename", "ori_shape", "pad_shape", and "img_norm_cfg". For details on the values
             of these keys see `mmdet/datasets/pipelines/formatting.py:Collect`.
            gt_bboxes - Ground truth bboxes for each image with shape (num_gts, 4) in [tl_x, tl_y, br_x, br_y] format.
            gt_labels - List of class indices corresponding to each box
            gt_crowds - List of "is crowds" (boolean) to each box
            gt_masks - List of masks (type BitmapMasks) for each image if task is instance_segmentation
        """
        # test mode
        img = data[MmDetectionDatasetLiterals.IMG]
        img_metas = data[MmDetectionDatasetLiterals.IMG_METAS]
        batch_predictions = self.model(
            img=[img], img_metas=[img_metas], return_loss=False
        )
        output: dict = self._organize_predictions_for_trainer(
            batch_predictions, img_metas
        )

        return torch.asarray([], device=get_current_device()), output


class InstanceSegmentationModelWrapper(ObjectDetectionModelWrapper):
    """Wrapper class over mm instance segmentation model of MMDetection framework."""
    def __init__(
        self,
        mm_instance_segmentation_model: nn.Module,
        config: Config,
        model_name_or_path: str,
    ):
        """Wrapper class over mm instance segmentation model of MMDetection framework.

        :param mm_instance_segmentation_model: MM instance segmentation model
        :type mm_instance_segmentation_model: nn.Module
        :param config: MM Instance segmentation model configuration
        :type config: MMCV Config
        :param model_name_or_path: model name or path
        :type model_name_or_path: str
        """
        self.max_image_size = 0
        super(InstanceSegmentationModelWrapper, self).__init__(
            mm_instance_segmentation_model, config, model_name_or_path
        )

    @classmethod
    def _get_segmentation_masks(cls, mask_result: List[np.ndarray]) -> Tensor:
        """
        Map the model's predicted segmentation masks to the format required by the HF trainer
        :param mask_result:
        :type mask_result: List of masks
        :return: mask in tensor format
        :rtype: Tensor
        """
        mask = concat_list(
            mask_result
        )  # Concatenate a list of list into a single list.
        if isinstance(mask[0], torch.Tensor):
            mask = torch.stack(mask, dim=0)
        else:
            mask = torch.as_tensor(np.stack(mask, axis=0))
        return mask

    def _organize_predictions_for_trainer(
            self,
            batch_predictions: List[Tuple[List[np.ndarray], List[np.ndarray]]],
            img_metas: List[Dict],
    ) -> Dict[str, Tensor]:
        """
        Transform the batch of predicted labels as required by the HF trainer.

        :param batch_predictions: batch of predicted labels
        :type batch_predictions: List of tuple containing list of bboxes and masks
        :param img_metas: batch of predicted labels
        :type img_metas: List of image metadata dictionary
        :return: Dict of predicted labels in tensor format
        :rtype: Dict[str, Tensor]
        """
        batch_bboxes, batch_labels, batch_masks, batch_original_img_shapes = [], [], [], []
        batch_original_mask_shapes = []
        for (predicted_bbox, predicted_mask), img_meta in zip(batch_predictions, img_metas):
            if isinstance(predicted_mask, tuple):
                predicted_mask = predicted_mask[0]  # ms rcnn

            bboxes, labels = super()._get_bboxes_and_labels(predicted_bbox, img_meta)
            original_mask_shape = (0, 0, 0)
            if predicted_mask is not None and len(labels) > 0:
                masks = InstanceSegmentationModelWrapper._get_segmentation_masks(
                    predicted_mask
                )
                # HF Trainer stack the predictions of all batches together. Since prediction masks could be of
                # different size, We are padding the masks to the max possible image size and we are removing the
                # padding when we parse the instance segmentation outputs.
                padded_masks = torch.empty(len(masks), self.max_image_size, self.max_image_size, dtype=torch.bool)
                padded_masks[:, :masks.shape[-2], :masks.shape[-1]] = masks
                original_mask_shape = masks.shape
            else:
                # The case when all predictions are below the box score threshold. Add empty mask tensor to satisfy
                # the pad_sequence criteria.
                padded_masks = torch.empty(0, self.max_image_size, self.max_image_size)
            batch_bboxes.append(bboxes)
            batch_labels.append(labels)
            batch_masks.append(padded_masks)
            batch_original_img_shapes.append(img_meta[MmDetectionDatasetLiterals.RAW_DIMENSIONS])
            batch_original_mask_shapes.append(original_mask_shape)

        output = dict()
        output[MmDetectionDatasetLiterals.BBOXES] = super()._pad_sequence(batch_bboxes)
        output[MmDetectionDatasetLiterals.LABELS] = super()._pad_sequence(batch_labels)
        output[MmDetectionDatasetLiterals.MASKS] = super()._pad_sequence(batch_masks)
        output[MmDetectionDatasetLiterals.RAW_DIMENSIONS] = \
            torch.tensor(batch_original_img_shapes, device=get_current_device())
        output[MmDetectionDatasetLiterals.RAW_MASK_DIMENSIONS] = \
            torch.tensor(batch_original_mask_shapes, device=get_current_device())
        return output
