# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Regressor wrapper for AutoML client object"""
from azureml.automl.core.shared import constants
from ._automlclientproxy import AutoMLClientProxy


class AutoMLRegressor(AutoMLClientProxy):
    """
    Client to run AutoML regression experiments
    """

    def __init__(
            self,
            client=None,
            primary_metric=constants.Metric.NormRMSE,
            y_min=None,
            y_max=None,
            **kwargs):
        """
        Constructor for the AutomlRegressor
        :param client: The backend client to use
        :param primary_metric: The metric you want to optimize the pipeline for
        :param y_min:
        :param y_max:
        :param kwargs: dictionary of keyword args
        """
        super().__init__(client=client,
                         task_type=constants.Tasks.REGRESSION,
                         primary_metric=primary_metric,
                         y_min=y_min,
                         y_max=y_max,
                         **kwargs)
