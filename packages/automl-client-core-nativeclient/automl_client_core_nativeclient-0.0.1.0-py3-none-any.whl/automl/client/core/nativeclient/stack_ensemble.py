# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Module for ensembling previous AutoML iterations."""
from typing import Any, cast, Dict, Union
import logging


from azureml.automl.runtime import stack_ensemble_base
from . import ensemble_helper
from .nativeclient_settings import AutoMLNativeClientSettings


logger = logging.getLogger(__name__)


class StackEnsemble(stack_ensemble_base.StackEnsembleBase):
    """
    Class for creating a StackEnsemble out of previous AutoML iterations.

    The StackEnsemble pipeline is initialized from a collection of already fitted pipelines.
    """

    def __init__(self, automl_settings: Union[str, Dict[str, Any], AutoMLNativeClientSettings],
                 ensemble_run_id: str, **kwargs: Any):
        """Create an Ensemble pipeline out of a collection of already fitted pipelines."""
        super().__init__(automl_settings, AutoMLNativeClientSettings)
        self.helper = ensemble_helper.EnsembleHelper(
            cast(AutoMLNativeClientSettings, self._automl_settings), ensemble_run_id)

    def _get_ensemble_and_parent_run(self):
        return self.helper.get_ensemble_and_parent_run()
