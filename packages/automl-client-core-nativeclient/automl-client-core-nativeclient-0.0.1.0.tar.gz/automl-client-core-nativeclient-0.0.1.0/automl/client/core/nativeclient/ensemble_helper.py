# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Module for ensembling previous AutoML iterations."""
from typing import cast
import os

from azureml.automl.core._logging import log_server
from .nativeclient_settings import AutoMLNativeClientSettings
from .run import NativeAutoMLRun


class EnsembleHelper(object):
    """
    Helper class for ensembling previous AutoML iterations.

    This helper class is used for handling NativeClient dependencies used during Ensemble iterations.
    """
    def __init__(self, automl_settings: AutoMLNativeClientSettings, ensemble_run_id: str):
        """Create an Ensemble pipeline out of a collection of already fitted pipelines."""
        self._automl_settings = automl_settings
        self._ensemble_run_id = ensemble_run_id

        self._parent_run_id_length = self._ensemble_run_id.rindex("_")
        self._parent_run_id = self._ensemble_run_id[0:self._parent_run_id_length]

    def get_ensemble_and_parent_run(self):
        ensemble_run_folder = NativeAutoMLRun.get_child_run_folder(
            self._automl_settings.path,
            self._ensemble_run_id[self._parent_run_id_length + 1:]
        )
        ensemble_run = NativeAutoMLRun(self._ensemble_run_id, ensemble_run_folder)
        parent_run = NativeAutoMLRun(self._parent_run_id, self._automl_settings.path)
        return ensemble_run, parent_run

    def get_logger(self):
        log_server.update_custom_dimensions({
            "parent_run_id": self._parent_run_id,
            "child_run_id": self._ensemble_run_id
        })

        return None
