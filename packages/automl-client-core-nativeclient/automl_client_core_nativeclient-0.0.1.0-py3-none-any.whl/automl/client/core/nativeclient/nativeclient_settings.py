# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import logging
import os
from azureml.automl.core.shared import constants, import_utilities
from azureml.automl.core.automl_base_settings import AutoMLBaseSettings


INSTRUMENTATION_KEY = 'e4d917c2-699a-4fb8-9f25-bd39b0a96e55'


class AutoMLNativeClientSettings(AutoMLBaseSettings):

    def __init__(self, *args, show_output=True, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.path:
            # let's set the project path to the folder where the log is being written
            if self.debug_log is not None:
                self.path = os.path.dirname(os.path.abspath(self.debug_log))
            else:
                self.path = os.getcwd()

        # Per PowerBi client request, native client should explain model after fit() instead of inside it.
        # Hence disable it
        self.model_explainability = False

        self.show_output = show_output

        # Have to check for XGBoost availability here, since we can't have JOS do it for us
        try:
            import xgboost
        except ImportError:
            self._blacklist_xgboost()

        # Have to check for Tensorflow availability here, since we can't have JOS do it for us
        if self.enable_tf:
            try:
                import tensorflow
            except ImportError:
                self._blacklist_tf()
        else:
            self._blacklist_tf()

        if self.is_timeseries:
            fbprophet = import_utilities.import_fbprophet(raise_on_fail=False)
            if fbprophet is None:
                self._blacklist_prophet()

    @property
    def _instrumentation_key(self) -> str:
        return INSTRUMENTATION_KEY

    def _blacklist_prophet(self) -> None:
        if self.blacklist_algos is None:
            self.blacklist_algos = [
                constants.SupportedModels.Forecasting.Prophet
            ]
        elif constants.SupportedModels.Forecasting.Prophet not in self.blacklist_algos:
            self.blacklist_algos.append(constants.SupportedModels.Forecasting.Prophet)

    def _blacklist_xgboost(self) -> None:
        if self.blacklist_algos is None:
            self.blacklist_algos = [
                constants.SupportedModels.Classification.XGBoostClassifier,
                constants.SupportedModels.Regression.XGBoostRegressor
            ]
        else:
            self.blacklist_algos.append(constants.SupportedModels.Classification.XGBoostClassifier)
            self.blacklist_algos.append(constants.SupportedModels.Regression.XGBoostRegressor)

    def _blacklist_tf(self) -> None:
        if self.blacklist_algos is None:
            self.blacklist_algos = [
                constants.SupportedModels.Classification.TensorFlowDNNClassifier,
                constants.SupportedModels.Classification.TensorFlowLinearClassifier,
                constants.SupportedModels.Regression.TensorFlowDNNRegressor,
                constants.SupportedModels.Regression.TensorFlowLinearRegressor
            ]
        else:
            self.blacklist_algos.append(constants.SupportedModels.Classification.XGBoostClassifier)
            self.blacklist_algos.append(constants.SupportedModels.Regression.XGBoostRegressor)
