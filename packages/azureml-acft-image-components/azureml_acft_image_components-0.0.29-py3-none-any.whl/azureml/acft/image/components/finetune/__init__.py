# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""AzureML ACFT Image Components package - finetuning component."""
__path__ = __import__('pkgutil').extend_path(__path__, __name__)


# List of Huggingface models that are not supported by the fine-tuning component. The name of model should be
# exactly same as model name specified in huggingface model repository.
UNSUPPORTED_HF_MODEL = [

]


# List of MMDetection models that are not supported by the fine-tuning component. The name of model should be
# exactly same as model name specified in mmdetection metafile.yaml
# (https://github.com/open-mmlab/mmdetection/tree/v2.28.2/configs).
UNSUPPORTED_MMDETECTION_MODEL = [
    # *rcnn_convnext* models are failing due to ModuleNotFoundError: No module named 'mmcls' WI: 2503815
    "mask_rcnn_convnext-t_p4_w7_fpn_fp16_ms-crop_3x_coco",
    "cascade_mask_rcnn_convnext-t_p4_w7_fpn_giou_4conv1f_fp16_ms-crop_3x_coco",
    "cascade_mask_rcnn_convnext-s_p4_w7_fpn_giou_4conv1f_fp16_ms-crop_3x_coco",
    # centernet* models are failing with key error ['border']. WI: 2500745
    "centernet_resnet18_dcnv2_140e_coco",
    "centernet_resnet18_140e_coco",
    # ga* models are failing with assert exception in evaluation loop. WI: 2500727
    "ga_rpn_r50_caffe_fpn_1x_coco",
    "ga_rpn_r101_caffe_fpn_1x_coco",
    "ga_rpn_x101_32x4d_fpn_1x_coco",
    "ga_rpn_x101_64x4d_fpn_1x_coco",
    "ga_faster_r50_caffe_fpn_1x_coco",
    "ga_faster_r101_caffe_fpn_1x_coco",
    "ga_faster_x101_32x4d_fpn_1x_coco",
    "ga_faster_x101_64x4d_fpn_1x_coco",
    "ga_retinanet_r50_caffe_fpn_1x_coco",
    "ga_retinanet_r101_caffe_fpn_1x_coco",
    "ga_retinanet_x101_32x4d_fpn_1x_coco",
    "ga_retinanet_x101_64x4d_fpn_1x_coco",
]


UNSUPPORTED_MMTRACKING_MODEL = [
    # currently do not support joint detection and tracking methods
    "sort_faster-rcnn_fpn_4e_mot17-public-half",
    "sort_faster-rcnn_fpn_4e_mot17-private-half",
    "deepsort_faster-rcnn_fpn_4e_mot17-public-half",
    "deepsort_faster-rcnn_fpn_4e_mot17-private-half",
    "qdtrack_faster-rcnn_r50_fpn_4e_mot17-private-half",
    "qdtrack_faster-rcnn_r50_fpn_4e_crowdhuman_mot17-private-half",
    "qdtrack_faster-rcnn_r101_fpn_24e_lvis",
    "qdtrack_faster-rcnn_r101_fpn_12e_tao",
    "tracktor_faster-rcnn_r50_fpn_4e_mot15-public-half",
    "tracktor_faster-rcnn_r50_fpn_4e_mot15-private-half",
    "tracktor_faster-rcnn_r50_fpn_4e_mot16-public-half",
    "tracktor_faster-rcnn_r50_fpn_4e_mot16-private-half",
    "tracktor_faster-rcnn_r50_fpn_4e_mot17-public-half",
    "tracktor_faster-rcnn_r50_fpn_4e_mot17-private-half",
    "tracktor_faster-rcnn_r50_fpn_4e_mot17-public",
    "tracktor_faster-rcnn_r50_fpn_8e_mot20-public-half",
    "tracktor_faster-rcnn_r50_fpn_8e_mot20-public",
    "tracktor_faster-rcnn_r50_fpn_fp16_4e_mot17-private-half"
]
