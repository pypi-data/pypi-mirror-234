# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from typing import Any, Dict, List, Optional
import logging
import time

import requests

from azureml.core import Workspace
from azureml.automl.core.shared import constants
from azureml.automl.runtime.automl_pipeline import AutoMLPipeline
from azureml.automl.runtime.automl_run_context import AutoMLAbstractRunContext
from azureml.automl.runtime.fit_output import FitOutput
from azureml.automl.core.shared.exceptions import ServiceException

logger = logging.getLogger(__name__)


class MiroProxyClientV2:
    def __init__(self, workspace: Workspace, service_url: Optional[str] = None):
        """
        Create a MiroProxyClient.

        :param workspace: workspace to use for authentication and API calls
        :param service_url: URL to use instead of that retrieved via discovery service
        """
        self._workspace = workspace
        self._service_url = service_url

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

        :param experiment_id:
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

        response = self._make_request(
            self._workspace, experiment_id, input_df, headers, task_type, run_context.run_id)

        return AutoMLPipeline(
            pipeline_id=response['pipeline_id'],
            pipeline_script=response['pipeline_spec'],
            training_size=float(response.get('training_percent') or 100) / 100,
            predicted_time=float(response.get('predicted_cost') or 0.0),
            run_context=run_context)

    def _make_request(self,
                      workspace: Workspace,
                      experiment_id: str,
                      body: Any,
                      custom_headers: Dict[str, str],
                      task_type: str,
                      run_id: Optional[str] = None) -> Any:
        headers = {
            'Content-Type': 'application/json-patch+json; charset=utf-8'
        }
        service_context = workspace.service_context
        auth = service_context.get_auth()
        auth_header = auth.get_authentication_header()
        headers.update(auth_header)
        headers.update(custom_headers)

        url = self._build_url(workspace, experiment_id, task_type, run_id)

        for _ in range(3):
            r = requests.post(url, json=body, headers=headers)

            if r.status_code == 200:
                # success
                try:
                    data = r.json()
                except Exception as e:
                    raise ServiceException('Failed to parse server response.') from e

                if 'error' in data:
                    raise ServiceException('Server responded with error')

                if len(data) == 0:
                    raise ServiceException('Server did not return any pipelines.')

                return data[0]
            elif r.status_code in [408, 409, 429, 500, 502, 503, 504]:
                # retry retriable errors
                logger.warning('Server responded with status code {}, retrying after 10s...'.format(r.status_code))
                time.sleep(10)
                continue
            else:
                # everything else, we don't know how to handle
                raise ServiceException('Server responded with status code: {0}'.format(r.status_code))

    def _build_url(self,
                   workspace: Workspace,
                   experiment_id: str,
                   task_type: str,
                   runid: Optional[str] = None) -> str:
        endpoint = \
            '{base_url}/jasmine/v1.0/miro' \
            '/subscriptions/{subscription}' \
            '/resourceGroups/{resource_group}' \
            '/providers/Microsoft.MachineLearningServices' \
            '/workspaces/{workspace}' \
            '/experimentids/{experiment}' \
            '/recommended/{task_type}'.format(
                base_url=self._service_url or workspace.service_context._get_jasmine_url(),
                subscription=workspace.subscription_id,
                resource_group=workspace.resource_group,
                workspace=workspace.name,
                experiment=experiment_id or 'none',
                task_type=task_type)
        if runid is not None:
            endpoint = '{0}/childrunid/{1}'.format(endpoint, runid)
        return endpoint
