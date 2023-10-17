# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from typing import Any, Dict, List, Optional
import logging
import re
import time

import requests

from azureml.automl.core.shared import constants, logging_utilities
from azureml.automl.runtime.automl_pipeline import AutoMLPipeline
from azureml.automl.runtime.automl_run_context import AutoMLAbstractRunContext
from azureml.automl.runtime.fit_output import FitOutput
from azureml.automl.core.shared.exceptions import ServiceException

from .abstract_nativeclient_authentication import AbstractNativeClientAuthentication

logger = logging.getLogger(__name__)


class MiroProxyClient:

    ALTERNATE_CLOUDS = {
        'api.ml.azure.us': {'usgovvirginia', 'usgovarizona'},
        'experiments.ml.azure.cn': {'chinaeast2'}
    }

    def __init__(self, authentication: AbstractNativeClientAuthentication, service_url: str) -> None:
        """
        Constructs an instance of PipelineProvider.

        :param authentication: An object implementing
            get_authentication_header()
        :param service_url: Base URL for API requests
        """
        self._authentication = authentication
        self._service_url = service_url

    @classmethod
    def get_service_url_for_region(cls, region: Optional[str]) -> str:
        """
        Given an Azure region, retrieves the URL for the closest JOS instance.
        :param region: An Azure location shortname
        :return: Endpoint base URL
        """
        for cloud in cls.ALTERNATE_CLOUDS:
            if region in cls.ALTERNATE_CLOUDS[cloud]:
                return 'https://{}.{}'.format(region, cloud)
        region_mapping = {
            'eastus': 'eastus',
            'eastus2': 'eastus2',
            'westcentralus': 'westcentralus',
            'westus2': 'westus2',
            'uksouth': 'westeurope',
            'japaneast': 'southeastasia',
            'northeurope': 'northeurope',
            'westeurope': 'westeurope',
            'australiaeast': 'australiaeast',
            'southeastasia': 'southeastasia',
            'centralus': 'southcentralus',
            'southcentralus': 'southcentralus',
            'canadacentral': 'westcentralus',
            'brazilsouth': 'southcentralus',
            'francecentral': 'westeurope',
            'centralindia': 'southeastasia',
            'koreacentral': 'southeastasia',
            'australiacentral': 'australiaeast',
            'eastus2euap': 'eastus2euap'
        }

        region = region_mapping.get(region or 'westus2', 'westus2')

        return 'https://{}.experiments.azureml.net'.format(region)

    @staticmethod
    def get_region_for_service_url(service_url: str) -> Optional[str]:
        match = re.fullmatch(r'https://(\w+)\.experiments\.azureml\.net', service_url)
        if not match:
            # Check for alternate clouds
            match = re.fullmatch(r'https://(\w+)\.experiments\.ml\.azure\.(us|cn)', service_url)
        if not match:
            return None
        return match.group(1)

    @property
    def service_url(self) -> str:
        return self._service_url

    @property
    def region(self) -> Optional[str]:
        return self.get_region_for_service_url(self.service_url)

    def get_pipeline(self,
                     experiment_id: str,
                     run_context: AutoMLAbstractRunContext,
                     task_type: str,
                     metric: str,
                     metric_operation: str,
                     num_threads: int,
                     previous_iterations: List[FitOutput],
                     previous_iteration_numbers: List[int],
                     iteration: int,
                     total_iterations: int,
                     is_sparse: bool = True,
                     num_categorical: int = 0,
                     num_features: int = 0,
                     num_classes: int = 0,
                     num_samples: int = 0,
                     time_constraint: int = constants.AutoMLDefaultTimeouts.DEFAULT_ITERATION_TIMEOUT_SECONDS,
                     blacklist_models: Optional[List[str]] = None,
                     whitelist_models: Optional[List[str]] = None,
                     cost_mode: int = constants.PipelineCost.COST_NONE,
                     headers: Optional[Dict[str, str]] = None,
                     subsampling: Optional[bool] = False,
                     customer: Optional[str] = None,
                     total_time_constraint: int = constants.AutoMLDefaultTimeouts.DEFAULT_EXPERIMENT_TIMEOUT_SECONDS,
                     max_time: int = constants.AutoMLDefaultTimeouts.DEFAULT_EXPERIMENT_TIMEOUT_SECONDS
                     ) -> AutoMLPipeline:
        """
        Fetches a new pipeline to use with AutoML.

        :param run_context: AutoMLAbstractRunContext
        :param task_type:
        :param metric:
        :param metric_operation:
        :param num_threads: number of threads that will be used for training
        :param previous_iterations: list of already tried pipelines
        :param previous_iteration_numbers: list of iteration numbers for already tried pipelines
        :param iteration: current iteration
        :param total_iterations: total number of iterations for the experiment
        :param is_sparse: whether the dataset is sparse or not
        :param num_categorical: number of categorical features
        :param num_features: number of features
        :param num_classes: number of classes
        :param num_samples: number of samples
        :param time_constraint: time constraint
        :param blacklist_models: blacklisted models
        :param whitelist_models: whitelisted models
        :param cost_mode: which pipeline cost mode Miro should use
        :param headers: custom headers to add to the request
        :param subsampling: whether subsampling should be used
        :param customer: customer
        :param total_time_constraint: total time constraint
        :param max_time: max time
        :return: AutoMLPipeline
        """

        if headers is None:
            headers = {}

        input_df = {
            'input_df': {
                'acquisition_function': None,
                'pipeline_ids': [p.pipeline_id for p in previous_iterations],
                'scores': [p.score for p in previous_iterations],
                'run_algorithms': [p.run_algorithm for p in previous_iterations],
                'run_preprocessors': [p.run_preprocessor for p in previous_iterations],
                'iteration_numbers': previous_iteration_numbers,
                'num_returned_pipelines': 1,
                'max_cores_per_iteration': num_threads,
                'metric': metric,
                'metric_operation': metric_operation,
                'time_constraint': time_constraint,
                'num_categorical': num_categorical,
                'num_features': num_features,
                'num_classes': num_classes,
                'num_samples': num_samples,
                'predicted_times': [p.predicted_time for p in previous_iterations],
                'actual_times': [p.actual_time for p in previous_iterations],
                'cost_mode': cost_mode,
                'is_sparse_data': is_sparse,
                'task': task_type,
                'model_names_blacklisted': blacklist_models,
                'model_names_whitelisted': whitelist_models,
                'subsampling': subsampling or False,
                'iteration': iteration,
                'total_iterations': total_iterations,
                'total_time_constraint': total_time_constraint,
                'max_time': max_time
            }
        }

        # Attempt retry 3 times on server error
        for _ in range(3):
            try:
                pipeline = self._make_request(self._build_url(task_type, run_context.run_id), input_df, headers)

                return AutoMLPipeline(
                    pipeline_id=pipeline['pipeline_id'],
                    pipeline_script=pipeline['pipeline_spec'],
                    training_size=float(pipeline.get('training_percent') or 100) / 100,
                    predicted_time=float(pipeline.get('predicted_cost') or 0.0),
                    run_context=run_context)
            except Exception as e:
                print(e)
                logging_utilities.log_traceback(e, logger)
                time.sleep(3)
        raise ServiceException('Failed to get a pipeline after 3 attempts.')

    def _make_request(self, url: str, body: Any, custom_headers: Dict[str, str]) -> Any:
        headers = {
            'Content-Type': 'application/json-patch+json; charset=utf-8'
        }
        headers.update(self._authentication.get_authentication_header())
        headers.update(custom_headers)
        r = requests.post(url, json=body, headers=headers)

        if r.status_code != 200:
            raise ServiceException('Server responded with status code: {0}'.format(r.status_code))

        try:
            data = r.json()
        except Exception as e:
            raise ServiceException('Failed to parse server response.') from e

        if 'error' in data:
            raise ServiceException('Server responded with error')

        if len(data) == 0:
            raise ServiceException('Server did not return any pipelines.')

        return data[0]

    def _build_url(self, task_type: str, runid: Optional[str] = None, customer: Optional[str] = None) -> str:
        endpoint = '{0}/jasmine/v1.0/pipelines/recommended/{1}'.format(self._service_url, task_type)
        if runid is not None:
            endpoint = '{0}/childrunid/{1}'.format(endpoint, runid)
        if customer is not None:
            endpoint = '{0}/customer/{1}'.format(endpoint, customer)
        return endpoint
