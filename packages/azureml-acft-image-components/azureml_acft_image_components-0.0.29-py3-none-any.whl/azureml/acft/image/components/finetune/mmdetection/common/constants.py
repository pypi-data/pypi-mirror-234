# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""File for adding all the constants required for MMDetection."""


class MmDetectionDatasetLiterals:
    """Constants for MMDetection dataset."""
    IMG = "img"
    IMG_METAS = "img_metas"
    GT_BBOXES = 'gt_bboxes'
    GT_LABELS = 'gt_labels'
    GT_CROWDS = 'gt_crowds'
    GT_MASKS = "gt_masks"
    PROPOSALS = "proposals"
    MASKS = "masks"
    BBOXES = "bboxes"
    LABELS = "labels"
    IMAGE_ORIGINAL_SHAPE = "ori_shape"
    DUMMY_LABELS = "dummy_labels"


class MmDetectionConfigLiterals:
    """Constants for MMDetection config."""
    NUM_CLASSES = "num_classes"
    BOX_SCORE_THRESHOLD = "score_thr"
    IOU_THRESHOLD = "iou_threshold"
    TRAIN_PIPELINE = "train_pipeline"
    COLLECT = "Collect"
    TYPE = "type"
    KEYS = "keys"
    CLASSES = "CLASSES"
    META = "meta"
    STATE_DICT = "state_dict"
