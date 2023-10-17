# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from azureml.automl.core.shared import constants
from ._automlclientproxy import AutoMLClientProxy


class AutoMLClassifier(AutoMLClientProxy):
    """
    Client to run AutoML classification experiments
    """

    def __init__(
            self,
            client=None,
            primary_metric=constants.Metric.Accuracy,
            num_classes=None,
            **kwargs):
        """
        Constructor for the AutoMLClassifier
        :param client: The backend client to use
        :param primary_metric: The metric you want to optimize the pipeline for
        :param num_classes: number of classes in you label data
        :param kwargs: dictionary of keyword args
        """

        super().__init__(client=client,
                         task_type=constants.Tasks.CLASSIFICATION,
                         primary_metric=primary_metric,
                         num_classes=num_classes,
                         **kwargs)
