# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Mlflow PythonModel wrapper helper scripts."""

import logging
import torch
import numpy as np

from typing import Any, Dict, List
from datasets import load_dataset
from transformers import (AutoImageProcessor,
                          AutoModelForImageClassification, Trainer,
                          TrainingArguments)
from constants import (Tasks, HFMiscellaneousLiterals,
                       MLFlowSchemaLiterals,)


def hf_run_inference_batch(
    test_args: TrainingArguments,
    feature_extractor: AutoImageProcessor,
    model: AutoModelForImageClassification,
    inference_dataset: List,
    task_type: Tasks,
    labels: List[str] = None,
):
    """This method performs inference on the one or more input images data.

    :param test_args: Training arguments path.
    :type test_args: transformers.TrainingArguments
    :param feature_extractor: Preprocessing configuration loader.
    :type feature_extractor: transformers.AutoFeatureExtractor
    :param model: Pytorch model weights.
    :type model: transformers.AutoModelForImageClassification
    :param inference_dataset: Dataset(list of image paths) for inferencing.
    :type inference_dataset: List
    :return: Predicted probabilities, ordered label names.
    :rtype: Tuple
    """

    def collate_fn(examples: List[Dict[str, Any]]) -> Dict[str, torch.tensor]:
        """This method loads the model.

        :param examples: List of input images.
        :type examples: List
        :return: Dictionary of pixel values in torch tensor format.
        :rtype: Dict
        """
        images = [data[HFMiscellaneousLiterals.DEFAULT_IMAGE_KEY] for data in examples]
        return feature_extractor(images, return_tensors="pt")

    inference_dataset = load_dataset(
        HFMiscellaneousLiterals.IMAGE_FOLDER, data_files={HFMiscellaneousLiterals.VAL: inference_dataset}
    )
    inference_dataset = inference_dataset[HFMiscellaneousLiterals.VAL]

    # Initialize the trainer
    trainer = Trainer(
        model=model,
        args=test_args,
        tokenizer=feature_extractor,
        data_collator=collate_fn,
    )
    results = trainer.predict(inference_dataset)
    if task_type == Tasks.MULTI_CLASS_IMAGE_CLASSIFICATION:
        probs = torch.nn.functional.softmax(torch.from_numpy(results.predictions), dim=1)
        label_indices = np.argmax(results.predictions, axis=1)
        pred_labels = [labels[x] for x in label_indices]
    elif task_type == Tasks.MULTI_LABEL_CLASSIFICATION:
        sigmoid = torch.nn.Sigmoid()
        probs = sigmoid(torch.from_numpy(results.predictions))
        label_indices = np.where(results.predictions > 0.5)
        pred_labels = [
            [labels[idx] for idx, val in enumerate(row) if val]
            for row in label_indices
        ]

        output = {
            MLFlowSchemaLiterals.OUTPUT_COLUMN_PROBS: probs,
            MLFlowSchemaLiterals.OUTPUT_COLUMN_LABELS: pred_labels
        }

    return output
