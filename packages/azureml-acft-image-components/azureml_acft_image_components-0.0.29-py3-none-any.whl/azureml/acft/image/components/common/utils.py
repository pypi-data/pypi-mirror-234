# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Common utils."""

import urllib.request

from azureml.automl.core.automl_utils import retry_with_backoff
from azureml.core import Workspace
from azureml.core.run import Run

from azureml.acft.common_components.utils.logging_utils import get_logger_app

logger = get_logger_app(__name__)


def get_workspace() -> Workspace:
    """Get current workspace either from Run or Config.

    :return: Current workspace
    :rtype: Workspace
    """
    try:
        ws = Run.get_context().experiment.workspace
        return ws
    except Exception:
        return Workspace.from_config()


@retry_with_backoff(retries=3)
def download_file(url: str, destination: str):
    """Download file from url to destination.
    :param url: Url to download from.
    :type url: str
    :param destination: Destination to download to.
    :type destination: str
    :raises Exception: If download fails.
    """
    urllib.request.urlretrieve(url, destination)
    logger.info(f"Downloaded {url} to {destination}.")
