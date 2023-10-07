# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""AzureML ACFT Image Components package - finetuning component MMDetection."""

import os
import json
from typing import Union

from mmcv import Config

from azureml._common._error_definition.azureml_error import AzureMLError  # type: ignore
from azureml.acft.common_components import get_logger_app
from azureml.acft.common_components.utils.error_handling.error_definitions import (
    TaskNotSupported,
    ModelIncompatibleWithTask,
    InvalidData
)
from azureml.acft.common_components.utils.error_handling.exceptions import (
    ACFTValidationException,
    ACFTSystemException
)

from azureml.acft.image.components.finetune.factory.mappings import MODEL_FAMILY_CLS
from azureml.acft.image.components.finetune.factory.task_definitions import Tasks
from azureml.acft.image.components.finetune.mmdetection.common.trainer_classes import (
    DetectionTrainer,
)
from azureml.acft.image.components.finetune.mmdetection.common.constants import (
    MmDetectionDatasetLiterals,
    MmDetectionConfigLiterals
)

from azureml.acft.image.components.model_selector.constants import MMDSupportedTasks
from azureml.acft.common_components.model_selector.constants import (
    ModelSelectorConstants
)

logger = get_logger_app(__name__)

MMDTaskMap = {
    MMDSupportedTasks.OBJECT_DETECTION: Tasks.MM_OBJECT_DETECTION,
    MMDSupportedTasks.INSTANCE_SEGMENTATION: Tasks.MM_INSTANCE_SEGMENTATION,
}


class TrainerClasses:
    """Trainer classes."""
    def __init__(
        self,
        model_family: MODEL_FAMILY_CLS,
        model_name_or_path: Union[str, os.PathLike],
        task_name: Tasks,
        model_metafile_path: str = None,
    ) -> None:
        """
        :param model_family: related model_family to which current task belongs
        :type model_family: azureml.acft.accelerator.mappings.MODEL_FAMILY_CLS
        :param model_name_or_path: Hugging face image model name or path
        :type model_name_or_path: Union[str, os.PathLike]
        :param task_name: related task_name
        :type task_name: azureml.acft.accelerator.constants.task_definitions.Tasks
        :param model_metafile_path: path to model metadata file
        :type model_metafile_path: str
        """
        self.model_family = model_family
        self.task_name = task_name
        self.model_name_or_path = model_name_or_path
        if os.path.exists(model_metafile_path):
            with open(model_metafile_path) as json_file:
                self.model_metadata = json.load(json_file)
        else:
            raise ACFTSystemException._with_error(
                AzureMLError.create(InvalidData,
                                    pii_safe_message=f"Model metadata file not found at {model_metafile_path}",
                                    ModelName=self.model_name_or_path,
                                    TaskName=self.task_name))
        self._is_finetuning_supported()

    def get_trainer_classes_mapping(self):
        """get trainer class based on task_name"""
        if self.task_name in [
            Tasks.MM_OBJECT_DETECTION,
            Tasks.MM_INSTANCE_SEGMENTATION,
        ]:
            return DetectionTrainer
        else:
            raise ACFTValidationException._with_error(
                AzureMLError.create(TaskNotSupported,
                                    TaskName=self.task_name))

    def _is_finetuning_supported(self):
        """check if model is supported for current task"""

        model_tasks = [MMDTaskMap[task.lower()] for task in
                       self.model_metadata[ModelSelectorConstants.FINETUNING_TASKS]]
        model_name = self.model_name_or_path.split("/")[-1][:-3]

        # raise if selected task is not in model tasks
        if self.task_name not in model_tasks:
            error_str = f"Model {self.model_name_or_path} is not compatible with task {self.task_name}. "\
                        f"Provided Model supports these tasks: {model_tasks}."
            logger.error(error_str)

            raise ACFTValidationException._with_error(
                AzureMLError.create(ModelIncompatibleWithTask,
                                    pii_safe_message=error_str,
                                    ModelName=model_name,
                                    TaskName=self.task_name))

        try:
            config = Config.fromfile(self.model_name_or_path)
        except Exception as e:
            error_str = f"Error while reading config file for model {model_name}."
            logger.error(error_str + f"Error: {e}")
            raise ACFTValidationException._with_error(
                AzureMLError.create(InvalidData,
                                    pii_safe_message=error_str,
                                    ModelName=model_name,
                                    TaskName=self.task_name))

        model_expected_keys = None
        for train_dict in config[MmDetectionConfigLiterals.TRAIN_PIPELINE]:
            if train_dict.get(MmDetectionConfigLiterals.TYPE) == MmDetectionConfigLiterals.COLLECT :
                model_expected_keys = train_dict[MmDetectionConfigLiterals.KEYS]
                break
        if model_expected_keys is None:
            error_str = f"{MmDetectionConfigLiterals.COLLECT} not found in {MmDetectionConfigLiterals.TRAIN_PIPELINE}"\
                        f"section of config file. Please check the config file."
            logger.error(error_str)
            raise ACFTValidationException._with_error(
                AzureMLError.create(InvalidData,
                                    pii_safe_message=error_str,
                                    ModelName=self.model_name_or_path,
                                    TaskName=self.task_name))

        supported_keys = [MmDetectionDatasetLiterals.IMG, MmDetectionDatasetLiterals.GT_BBOXES,
                          MmDetectionDatasetLiterals.GT_LABELS]
        if self.task_name == Tasks.MM_OBJECT_DETECTION:
            # to add proposals here after adding support for proposals
            # till then userexception will be raised if the model expects proposals
            pass
        elif self.task_name == Tasks.MM_INSTANCE_SEGMENTATION:
            supported_keys.append(MmDetectionDatasetLiterals.GT_MASKS)
        else:
            raise NotImplementedError

        # for ex: model_name res2net/htc_r2_101_fpn_20e_coco.py
        # req_keys: ['img', 'gt_bboxes', 'gt_labels', 'gt_masks', 'gt_semantic_seg']
        # finetuning_tasks: ['object_detection', 'instance_segmentation']
        # we are not passing gt_semantic_seg as input data
        for key in model_expected_keys:
            if key not in supported_keys:
                error_str = f"Model {model_name} is not compatible with task {self.task_name}. "\
                    f"Model expects key: {key} to be present in the data which is not supported for this task."
                logger.error(error_str)
                raise ACFTValidationException._with_error(
                    AzureMLError.create(ModelIncompatibleWithTask,
                                        pii_safe_message=error_str,
                                        ModelName=model_name,
                                        TaskName=self.task_name))
