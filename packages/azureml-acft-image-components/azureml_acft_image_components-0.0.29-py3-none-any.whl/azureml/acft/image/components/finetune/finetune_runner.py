# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
# Copyright 2020 The HuggingFace Inc. team. All rights reserved.
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

"""Finetune runner for image tasks."""

import os

from argparse import Namespace
from functools import partial
from azureml._common._error_definition.azureml_error import AzureMLError  # type: ignore
from azureml.acft.accelerator.constants import HfTrainerType
from azureml.acft.accelerator.finetune import AzuremlDatasetArgs, AzuremlFinetuneArgs
from azureml.acft.accelerator.finetune import AzuremlTrainer
from azureml.acft.common_components.utils.error_handling.error_definitions import ACFTSystemError
from azureml.acft.common_components import get_logger_app, ModelSelectorDefaults
from azureml.acft.common_components.image.runtime_common.common import distributed_utils
from azureml.acft.common_components.utils.license_utils import save_license_file
from azureml.acft.common_components.utils.error_handling.exceptions import ACFTSystemException
from azureml.acft.image.components.finetune.common.trainer.train_helper import save_pytorch_model
from azureml.acft.image.components.finetune.factory.mappings import MODEL_FAMILY_CLS
from azureml.acft.image.components.finetune.factory.model_factory import ModelFactory
from azureml.acft.image.components.finetune.common.constants.constants import (
    SettingLiterals,
    HfProcessorParamNames, SettingParameters,
)
from azureml.acft.image.components.finetune.common.mlflow.common_constants import MetricsLiterals
from azureml.evaluate import mlflow

logger = get_logger_app(__name__)


def finetune_runner(component_args: Namespace) -> None:
    """
    finetune runner for all image tasks

    :param component_args: args from the finetune component
    :type component_args: Namespace
    """

    logger.info("Starting finetune runner")
    logger.info(f"Task name: {component_args.task_name}")
    model_metafile_path = component_args.model_metafile_path if \
        hasattr(component_args, "model_metafile_path") else None
    model_factory = ModelFactory(
        component_args.model_family,
        component_args.model_name_or_path,
        task_name=component_args.task_name,
        model_metafile_path=model_metafile_path,
    )
    trainer_classes_obj = model_factory.get_trainer_classes()

    # set the trainer classes
    finetune_cls = trainer_classes_obj.finetune_cls
    image_processor = trainer_classes_obj.tokenizer_cls
    data_cls = trainer_classes_obj.dataset_cls
    model_cls = trainer_classes_obj.model_cls
    calculate_metrics = trainer_classes_obj.metrics_function
    trainer_callbacks = trainer_classes_obj.callbacks

    # call the interface
    finetune_obj = finetune_cls(vars(component_args))

    # get the component args dict
    custom_finetune_args = finetune_obj.get_finetune_args()
    component_args_dict = vars(component_args)
    component_args_dict.update(custom_finetune_args)

    # Accelerator package uses argument "pytorch_model_folder" to store the model checkpoint and best model at the
    # end of training. We want to store these models in job's "output" folder. Hence, overriding the value of
    # "pytorch_model_folder" with job's output folder name. At the end of training, we will copy the best checkpoint
    # from job's output to user specified pytorch model folder i.e., component_args.pytorch_model_folder before
    # registering it as pytorch model asset.
    component_args_dict["pytorch_best_model_folder"] = component_args.pytorch_model_folder if \
        component_args.pytorch_model_folder != component_args.output_dir else SettingParameters.DEFAULT_PYTORCH_OUTPUT
    component_args_dict["pytorch_model_folder"] = SettingParameters.DEFAULT_OUTPUT_DIR

    # get the custom trainer functions
    custom_trainer_functions = finetune_obj.get_custom_trainer_functions()

    # init the tokenizer
    tokenizer = (
        image_processor.from_pretrained(
            component_args.model_name_or_path, **component_args_dict
        )
        if image_processor
        else None
    )

    # tokenizer image width and height would be used if user provided image width and height as -1
    # This change is specifically for hugging face models.
    if component_args.model_family == MODEL_FAMILY_CLS.HUGGING_FACE_IMAGE and (
        component_args_dict[SettingLiterals.IMAGE_HEIGHT] == -1
        or component_args_dict[SettingLiterals.IMAGE_WIDTH] == -1
    ):
        if HfProcessorParamNames.HEIGHT_KEY and HfProcessorParamNames.WIDTH_KEY in tokenizer.size:
            component_args_dict[SettingLiterals.IMAGE_HEIGHT] = tokenizer.size[HfProcessorParamNames.HEIGHT_KEY]
            component_args_dict[SettingLiterals.IMAGE_WIDTH] = tokenizer.size[HfProcessorParamNames.WIDTH_KEY]
        elif (
            HfProcessorParamNames.SHORTEST_EDGE_KEY in tokenizer.size
            and HfProcessorParamNames.LONGEST_EDGE_KEY not in tokenizer.size
        ):
            component_args_dict[SettingLiterals.IMAGE_HEIGHT] = tokenizer.size[HfProcessorParamNames.SHORTEST_EDGE_KEY]
            component_args_dict[SettingLiterals.IMAGE_WIDTH] = tokenizer.size[HfProcessorParamNames.SHORTEST_EDGE_KEY]
        elif (
            HfProcessorParamNames.LONGEST_EDGE_KEY in tokenizer.size
            and HfProcessorParamNames.SHORTEST_EDGE_KEY not in tokenizer.size
        ):
            component_args_dict[SettingLiterals.IMAGE_HEIGHT] = tokenizer.size[HfProcessorParamNames.LONGEST_EDGE_KEY]
            component_args_dict[SettingLiterals.IMAGE_WIDTH] = tokenizer.size[HfProcessorParamNames.LONGEST_EDGE_KEY]
        elif (
            HfProcessorParamNames.LONGEST_EDGE_KEY in tokenizer.size
            and HfProcessorParamNames.SHORTEST_EDGE_KEY in tokenizer.size
        ):
            if (
                tokenizer.size[HfProcessorParamNames.LONGEST_EDGE_KEY]
                == tokenizer.size[HfProcessorParamNames.SHORTEST_EDGE_KEY]
            ):
                component_args_dict[SettingLiterals.IMAGE_HEIGHT] = tokenizer.size[
                    HfProcessorParamNames.LONGEST_EDGE_KEY
                ]
                component_args_dict[SettingLiterals.IMAGE_WIDTH] = tokenizer.size[
                    HfProcessorParamNames.LONGEST_EDGE_KEY
                ]
            else:
                error_string = "Longest edge and shortest edge are not equal in the tokenizer."
                raise ACFTSystemException._with_error(
                    AzureMLError.create(ACFTSystemError, pii_safe_message=error_string)
                )
        else:
            error_string = "Default image height and width are not available in the tokenizer."
            raise ACFTSystemException._with_error(AzureMLError.create(ACFTSystemError, pii_safe_message=error_string))

    # log the component args dict
    logger.info(f"Component args dict used for training: {component_args_dict}")

    data_cls = data_cls(tokenizer=tokenizer, **component_args_dict)
    # set the dataset args
    dataset_args = AzuremlDatasetArgs(
        train_dataset=data_cls.get_train_dataset(),
        validation_dataset=data_cls.get_validation_dataset(),
        data_collator=data_cls.get_collation_function(),
    )

    # init model
    model = model_cls.from_pretrained(
        component_args.model_name_or_path,
        label2id=data_cls.label2id,
        id2label=data_cls.id2label,
        num_labels=len(data_cls.label2id),
        **component_args_dict,
    )

    if isinstance(model, tuple):
        model, mismatch_info = model
        logger.info(f"Mismatch info: {mismatch_info}")

    component_args_dict[SettingLiterals.NUM_LABELS] = len(data_cls.label2id)

    azml_finetune_args = AzuremlFinetuneArgs(
        finetune_args=component_args_dict, trainer_type=HfTrainerType.DEFAULT
    )

    # Define metric func, send the arguments to the metric function
    compute_metric_func = None
    if calculate_metrics:
        # metric computer is only available for OD and IS models.
        metrics_computer = model.metrics_computer if hasattr(model, 'metrics_computer') else None
        calculate_metrics_kwargs = {
            MetricsLiterals.METRICS_COMPUTER: metrics_computer, **component_args_dict
        } if metrics_computer else component_args_dict
        compute_metric_func = partial(calculate_metrics, **calculate_metrics_kwargs)

    # init trainer
    azml_trainer = AzuremlTrainer(
        finetune_args=azml_finetune_args,
        dataset_args=dataset_args,
        model=model,
        tokenizer=tokenizer,
        metric_func=compute_metric_func,
        custom_trainer_callbacks=trainer_callbacks,
        custom_trainer_functions=custom_trainer_functions,
        new_initalized_layers=None,
    )
    master_process = distributed_utils.master_process()
    try:
        azml_trainer.train()
    except Exception:
        # Let the exception propagate to catch in exception swallow wrapper.
        raise
    finally:
        # Upload local output to job's mlflow run artifact
        if master_process:
            mlflow.log_artifacts(component_args.output_dir, SettingParameters.DEFAULT_OUTPUT_DIR)

    # saving the mlflow model
    if component_args.save_as_mlflow_model and master_process:
        logger.info("saving the mlflow model")
        if component_args.model_family == MODEL_FAMILY_CLS.HUGGING_FACE_IMAGE:

            # In new version azureml_evaluate_mlflow 0.1.0.86769376 package infer the tokenizer class.
            # Now, we don't need to pass "hf_tokenizer_class": AutoImageProcessor.__name__,

            # In train_label_list, use id2label to get label list. Avoid using label2id as label2id can be
            # inconsistent if there are two labels with same name (very rare condition). It's observed in google vit
            # model's default config.

            hf_conf = {
                "task_type": component_args.task_name,
                "train_label_list": sorted(list(model.config.id2label.values())),
                "hf_predict_module": "hf_test_predict",
            }
            mlflow_dir = os.path.join(os.path.dirname(__file__), "common", "mlflow")
            files_to_include = ['common_constants.py', 'common_utils.py', 'hf_test_predict.py']
            code_paths = [os.path.join(mlflow_dir, x) for x in files_to_include]
            from mlflow_save_utils import get_mlflow_signature
            mlflow.hftransformers.save_model(
                model,
                component_args.mlflow_model_folder,
                tokenizer=tokenizer,
                config=model.config,
                hf_conf=hf_conf,
                code_paths=code_paths,
                signature=get_mlflow_signature(component_args.task_name)
            )
        elif component_args.model_family in (MODEL_FAMILY_CLS.MMDETECTION_IMAGE, MODEL_FAMILY_CLS.MMTRACKING_VIDEO):
            # importing directly from acft package is resulting in our package dependencies.
            from mlflow_save_utils import save_mmdet_mlflow_pyfunc_model
            save_mmdet_mlflow_pyfunc_model(
                model_output_dir=component_args.output_dir,
                mlflow_output_dir=component_args.mlflow_model_folder,
                model_name=os.path.basename(component_args.model_name).split('.')[0],
                task_type=component_args.task_name,
            )
        else:
            raise NotImplementedError(f"Saving mlflow model is not implemented for this model family\
                : {component_args.model_family}")

    if master_process:
        # saving the pytorch model
        save_pytorch_model(job_output_dir=component_args.output_dir,
                           pytorch_model_folder=component_args.pytorch_best_model_folder)

        # save the license file in the pytorch, job output and mlflow model folders
        if MODEL_FAMILY_CLS.MMDETECTION_IMAGE == component_args.model_family:
            component_args.model_name_or_path = os.path.dirname(component_args.model_name_or_path)
        save_license_file(
            model_name_or_path=component_args.model_name_or_path,
            license_file_name=ModelSelectorDefaults.LICENSE_FILE_NAME,
            destination_paths=[component_args.pytorch_best_model_folder, component_args.mlflow_model_folder]
        )
