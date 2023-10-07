# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Huggingface classification predict file for mlflow."""

import logging

import pandas as pd
import tempfile

import torch

from datasets import load_dataset
from transformers import (
    AutoImageProcessor,
    AutoModelForImageClassification,
    TrainingArguments,
    Trainer
)
from typing import List, Dict, Any, Tuple

from common_constants import (HFMiscellaneousLiterals, Tasks, MLFlowSchemaLiterals)
from common_utils import create_temp_file, process_image

logger = logging.getLogger(__name__)


def predict(input_data: pd.DataFrame, task, model, tokenizer, **kwargs) -> pd.DataFrame:
    """Perform inference on the input data.

    :param input_data: Input images for prediction.
    :type input_data: Pandas DataFrame with a first column name ["image"] of images where each
    image is in base64 String format.
    :param task: Task type of the model.
    :type task: HFTaskLiterals
    :param tokenizer: Preprocessing configuration loader.
    :type tokenizer: transformers.AutoImageProcessor
    :param model: Pytorch model weights.
    :type model: transformers.AutoModelForImageClassification
    :return: Output of inferencing
    :rtype: Pandas DataFrame with columns ["filename", "probs", "labels"] for classification and
    ["filename", "boxes"] for object detection, instance segmentation
    """
    # Decode the base64 image column
    decoded_images = input_data.loc[
        :, [MLFlowSchemaLiterals.INPUT_COLUMN_IMAGE]
    ].apply(axis=1, func=process_image)

    # arguments for Trainer
    test_args = TrainingArguments(
        output_dir=".",
        do_train=False,
        do_predict=True,
        per_device_eval_batch_size=kwargs.get(MLFlowSchemaLiterals.BATCH_SIZE_KEY, 1),
        dataloader_drop_last=False,
        remove_unused_columns=False,
    )

    # To Do: change image height and width based on kwargs.

    with tempfile.TemporaryDirectory() as tmp_output_dir:
        image_path_list = (
            decoded_images.iloc[:, 0]
            .map(lambda row: create_temp_file(row, tmp_output_dir))
            .tolist()
        )
        conf_scores = run_inference_batch(
            test_args,
            image_processor=tokenizer,
            model=model,
            image_path_list=image_path_list,
            task_type=task
        )

    df_result = pd.DataFrame(
        columns=[
            MLFlowSchemaLiterals.OUTPUT_COLUMN_PROBS,
            MLFlowSchemaLiterals.OUTPUT_COLUMN_LABELS,
        ]
    )

    labels = kwargs.get(MLFlowSchemaLiterals.TRAIN_LABEL_LIST)
    labels = [labels.tolist()] * len(conf_scores)
    df_result[MLFlowSchemaLiterals.OUTPUT_COLUMN_PROBS], df_result[MLFlowSchemaLiterals.OUTPUT_COLUMN_LABELS]\
        = (conf_scores.tolist(), labels)
    return df_result


def run_inference_batch(
    test_args: TrainingArguments,
    image_processor: AutoImageProcessor,
    model: AutoModelForImageClassification,
    image_path_list: List,
    task_type: Tasks,
) -> Tuple[torch.tensor]:
    """Perform inference on batch of input images.

    :param test_args: Training arguments path.
    :type test_args: transformers.TrainingArguments
    :param image_processor: Preprocessing configuration loader.
    :type image_processor: transformers.AutoImageProcessor
    :param model: Pytorch model weights.
    :type model: transformers.AutoModelForImageClassification
    :param image_path_list: list of image paths for inferencing.
    :type image_path_list: List
    :param task_type: Task type of the model.
    :type task_type: Tasks
    :return: Predicted probabilities
    :rtype: Tuple of torch.tensor
    """

    def collate_fn(examples: List[Dict[str, Any]]) -> Dict[str, torch.tensor]:
        """Collator function for eval dataset.

        :param examples: List of input images.
        :type examples: List
        :return: Dictionary of pixel values in torch tensor format.
        :rtype: Dict
        """
        images = [data[HFMiscellaneousLiterals.DEFAULT_IMAGE_KEY] for data in examples]
        return image_processor(images, return_tensors="pt")

    inference_dataset = load_dataset(
        "imagefolder",
        data_files={"val": image_path_list}
    )
    inference_dataset = inference_dataset["val"]

    # Initialize the trainer
    trainer = Trainer(
        model=model,
        args=test_args,
        tokenizer=image_processor,
        data_collator=collate_fn,
    )
    results = trainer.predict(inference_dataset)
    if task_type == Tasks.HF_MULTI_CLASS_IMAGE_CLASSIFICATION:
        probs = torch.nn.functional.softmax(torch.from_numpy(results.predictions), dim=1).numpy()
    elif task_type == Tasks.HF_MULTI_LABEL_IMAGE_CLASSIFICATION:
        sigmoid = torch.nn.Sigmoid()
        probs = sigmoid(torch.from_numpy(results.predictions)).numpy()
    return probs
