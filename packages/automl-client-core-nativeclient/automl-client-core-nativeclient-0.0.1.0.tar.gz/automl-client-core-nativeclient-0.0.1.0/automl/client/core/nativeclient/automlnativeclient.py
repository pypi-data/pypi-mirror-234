# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""
Legacy native client, kept for backwards compatibility. Will be removed and replaced by refactored version eventually.
"""
import gc
import json
import logging
import os
import sys
import uuid
import warnings
from datetime import datetime, timezone
from threading import Timer
from typing import cast, List, Dict, Optional, Any, Tuple, Union

import numpy as np
import scipy
import sklearn

from azureml._common._error_definition import AzureMLError
from azureml._common._error_definition.user_error import ArgumentOutOfRange, ArgumentBlankOrEmpty
from azureml.automl.core import package_utilities
from azureml.automl.core._experiment_observer import NullExperimentObserver
from azureml.automl.core._logging import log_server
from azureml.automl.core.automl_base_settings import AutoMLBaseSettings
from azureml.automl.core.console_interface import ConsoleInterface
from azureml.automl.core.console_writer import ConsoleWriter
from azureml.automl.core.onnx_convert.onnx_convert_constants import OnnxConvertConstants, SplitOnnxModelName
from azureml.automl.core.shared import constants, logging_utilities, utilities
from azureml.automl.core.shared._diagnostics.automl_error_definitions import ConflictingValueForArguments, ModelMissing
from azureml.automl.core.shared._diagnostics.contract import Contract
from azureml.automl.core.shared.exceptions import AutoMLException, ConfigException, OnnxConvertException
from azureml.automl.core.shared.limit_function_call_exceptions import TimeoutException
from azureml.automl.core.systemusage_telemetry import SystemResourceUsageTelemetryFactory
from azureml.automl.runtime import _data_transformation_utilities, data_transformation, fit_pipeline, \
    training_utilities
from azureml.automl.runtime._featurization_orchestration import orchestrate_featurization
from azureml.automl.runtime._run_history.offline_automl_run import OfflineAutoMLRunContext
from azureml.automl.runtime._runtime_params import ExperimentControlSettings, ExperimentResourceSettings, \
    ExperimentOrchestrationSettings, PipelineSelectionSettings, ExperimentDataSettings
from azureml.automl.runtime.automl_pipeline import AutoMLPipeline
from azureml.automl.runtime.automl_run_context import AutoMLAbstractRunContext
from azureml.automl.runtime.data_context import RawDataContext, TransformedDataContext, DataContextParams
from azureml.automl.runtime.experiment_store import ExperimentStore
from azureml.automl.runtime.faults_verifier import VerifierManager
from azureml.automl.runtime.fit_output import FitOutput
from azureml.automl.runtime.onnx_convert import OnnxConverter
from azureml.automl.runtime.shared import metrics
from azureml.automl.runtime.shared import pipeline_spec
from azureml.automl.runtime.shared.cache_store import CacheStore
from azureml.automl.runtime.shared.lazy_file_cache_store import LazyFileCacheStore
from . import run
from ._miroproxyclient import MiroProxyClient
from ._miroproxyclientv2 import MiroProxyClientV2
from .nativeclient_settings import AutoMLNativeClientSettings
from .run import NativeAutoMLRun

logger = logging.getLogger(__name__)


class AutoMLNativeClient:
    """
    Client for interacting without AzureML
    """

    def __init__(
            self,
            authentication=None,
            region=None,
            service_url=None,
            customer=None,
            workspace=None):
        """
        Constructor for the AutoMLNativeClient class
        :param workspace: azureml.core.Workspace object used for API calls and authentication.
        :param service_url: A URL pointing to a JOS instance. Overrides the service URL from workspace if specified.
        :param customer: A string used to classify the traffic for different customers.
        """
        self.automl_settings = cast(AutoMLNativeClientSettings, None)
        self.experiment_start_time = None

        self._status = constants.Status.NotStarted
        self._loop = None
        self._score_max = None
        self._score_min = None
        self._console_writer = ConsoleWriter()

        self.experiment_id = ''  # type: str
        self.current_iter = 0
        self.fit_outputs = []     # type: List[FitOutput]
        self.raw_experiment_data = None

        self.user_script = None
        self.subsampling = None

        self.service_url = service_url
        self.workspace = workspace
        if self.workspace:
            self._provider = \
                MiroProxyClientV2(workspace, self.service_url)     # type: Union[MiroProxyClient, MiroProxyClientV2]
        else:
            logging.warning('Custom auth/user-settable region will be deprecated in favor of passing in a workspace '
                            'object.')
            self._provider = MiroProxyClient(authentication,
                                             self.service_url or MiroProxyClient.get_service_url_for_region(region))

        self._usage_telemetry = None
        self._customer = customer
        self.child_metrics_mocks = {}   # type: Dict[int, NativeAutoMLRun]

        self.onnx_cvt = None

    def __del__(self):
        """
        Clean up AutoML loggers and close files.
        """
        try:
            if self._usage_telemetry is not None:
                self._usage_telemetry.stop()
        except Exception:
            # last chance, nothing can be done, so ignore any exception
            pass

    def initialize_client(self, **kwargs):
        self.automl_settings = AutoMLNativeClientSettings(**kwargs)
        # Per PowerBi client request, native client explain model after fit()
        #  instead of inside it.
        # Hence disable it
        self.automl_settings.model_explainability = False

        self._usage_telemetry = SystemResourceUsageTelemetryFactory.get_system_usage_telemetry()
        self._usage_telemetry.start()

        if not hasattr(self.automl_settings, 'enable_early_stopping'):
            self.automl_settings.enable_early_stopping = False
        else:
            if not hasattr(self.automl_settings, 'early_stopping_n_iters'):
                self.automl_settings.early_stopping_n_iters = 10

        if not self.automl_settings.show_warnings:
            # sklearn forces warnings, so we disable them here
            warnings.simplefilter('ignore', DeprecationWarning)
            warnings.simplefilter('ignore', RuntimeWarning)
            warnings.simplefilter('ignore', UserWarning)
            warnings.simplefilter('ignore', FutureWarning)
            warnings.simplefilter(
                'ignore', sklearn.exceptions.UndefinedMetricWarning)

    def start_experiment(self):
        self.experiment_id = 'AutoMLNativeClient_{}'.format(uuid.uuid1())
        if self.automl_settings.is_timeseries:
            task_type = "forecasting"
        else:
            task_type = self.automl_settings.task_type

        log_server.update_custom_dimensions(
            {
                "experiment_id": '[Scrubbed]',
                "task_type": task_type,
                "service_url": self.service_url
            }
        )

        from automl.client.core.nativeclient import __version__
        logger.info('Created new experiment using version: {}'.format(__version__))

        self._status = constants.Status.Started

    def cancel(self):
        self._status = constants.Status.Terminated

    def get_output(
            self,
            iteration: Optional[int] = None,
            metric: Optional[str] = None,
            whole_pipeline: bool = False,
            return_onnx_model: bool = False,
            return_split_onnx_model: Optional[SplitOnnxModelName] = None,
            **kwargs: Any) -> Union[FitOutput, Tuple[Dict[Any, Any], Any]]:
        """
        Retrieves the best pipeline tested so far with this client.
        :param iteration: The iteration number of the correspond pipeline spec and fitted model to return.
        :type iteration: int
        :param metric: The metric to use to return the best pipeline spec and fitted model to return.
        :type metric: str
        :param whole_pipeline: Flag to return the whole pipeline or a tuple of validation score and
        the model
        :type whole_pipeline: bool
        :param return_onnx_model: This method will return the converted ONNX model, if user indicated
                                  the enable_onnx_compatible_models config.
        :type return_onnx_model: bool
        :param kwargs: Not in use, to be deprecated.
        :return: A tuple of the best pipeline's validation scores as well as
        the model
        """
        # ToDo : deprecate kwargs

        with logging_utilities.log_activity(logger=logger, activity_name=constants.TelemetryConstants.OUTPUT_NAME):
            if iteration and metric:
                raise ConfigException._with_error(
                    AzureMLError.create(
                        ConflictingValueForArguments, target="iteration",
                        arguments=', '.join(['metric', 'iteration'])
                    )
                )

            if return_onnx_model and not self.automl_settings.enable_onnx_compatible_models:
                raise OnnxConvertException("Invalid parameter 'return_onnx_model' passed in.")
            if return_split_onnx_model is not None \
                    and not self.automl_settings.enable_split_onnx_featurizer_estimator_models:
                raise OnnxConvertException("Invalid parameter 'return_split_onnx_model' passed in.")

            if iteration is not None:
                total_runs = len(self.fit_outputs)

                if not isinstance(iteration, int) or iteration >= total_runs \
                        or iteration < 0:
                    raise ConfigException._with_error(
                        AzureMLError.create(
                            ArgumentOutOfRange, target="iteration",
                            argument_name="iteration ({})".format(str(iteration)), min=0, max=total_runs
                        )
                    )

                best_pipeline = self.fit_outputs[iteration]
                if whole_pipeline:
                    return best_pipeline
                if return_onnx_model:
                    result_onnx_mdl = \
                        self._get_onnx_model_from_fit_output(fit_output=best_pipeline,
                                                             return_split_onnx_model=return_split_onnx_model)
                    return best_pipeline.get_output_dict(), result_onnx_mdl
                else:
                    return best_pipeline.get_output_dict(), best_pipeline.fitted_pipeline

            if metric is None:
                metric = self.automl_settings.primary_metric

            objective = metrics.minimize_or_maximize(metric)

            _child_metrics = []
            for k, v in self.child_metrics_mocks.items():
                current_metrics_val = v.get_metrics().get(metric, np.nan)
                if current_metrics_val is not np.nan:
                    _child_metrics.append((current_metrics_val, k))

            if len(_child_metrics) == 0:
                raise AutoMLException._with_error(
                    AzureMLError.create(ModelMissing, target="metric", metric=metric)
                )

            _scores = np.array(_child_metrics)

            if objective == constants.OptimizerObjectives.MAXIMIZE:
                best_idx = np.nanargmax(_scores, axis=0)
                is_desc = True
            else:
                Contract.assert_true(
                    objective == constants.OptimizerObjectives.MINIMIZE,
                    "Maximization or Minimization could not be determined based on current metric",
                    log_safe=True
                )
                best_idx = np.nanargmin(_scores, axis=0)
                is_desc = False

            best_onnx_model = None
            if return_onnx_model:
                best_idx_onnx = None
                _child_metrics.sort(key=lambda obj: obj[0], reverse=is_desc)  # type: ignore
                for _, cur_idx in _child_metrics:
                    cur_fit_output = self.fit_outputs[cur_idx]
                    cur_onnx_model = self._get_onnx_model_from_fit_output(cur_fit_output, return_split_onnx_model)
                    if cur_onnx_model is not None:
                        best_idx_onnx = cur_idx
                        best_idx = cur_idx
                        best_onnx_model = cur_onnx_model
                        break
                if best_idx_onnx is None:
                    raise AutoMLException._with_error(
                        AzureMLError.create(ModelMissing, target="return_onnx_model", metric=metric)
                    )
            else:
                best_idx = _scores[best_idx[0]][1].astype(int)

            best_pipeline = self.fit_outputs[best_idx]

            if whole_pipeline:
                return best_pipeline

            best_pipe_output = best_pipeline.get_output_dict()
            # Add the child run iteration number into the result dict of the best run.
            if best_pipe_output is not None:
                best_pipe_output['iteration'] = best_idx
            if return_onnx_model:
                return best_pipe_output, best_onnx_model
            else:
                return best_pipe_output, best_pipeline.fitted_pipeline

    def fit(self,
            run_configuration=None,
            compute_target=None,
            X=None,
            y=None,
            sample_weight=None,
            X_valid=None,
            y_valid=None,
            sample_weight_valid=None,
            cv_splits_indices=None,
            show_output=False,
            existing_run=False,
            kwargs=None):
        """
        Start a new AutoML execution on the specified compute target
        :param run_configuration: The run confiuguration used by AutoML,
        should contain a compute target for remote
        :type run_configuration: Azureml.core RunConfiguration
        :param compute_target: The AzureML compute node to run this
        experiment on
        :type compute_target: azureml.core.compute.AbstractComputeTarget
        :param X: Training features
        :type X: pandas DataFrame, numpy ndarray or azureml.dataprep.Dataflow
        :param y: Training labels
        :type y: pandas DataFrame, numpy ndarray or azureml.dataprep.Dataflow
        :param sample_weight:
        :type sample_weight: pandas DataFrame, numpy ndarray or
        azureml.dataprep.Dataflow
        :param X_valid: validation features
        :type X_valid: pandas DataFrame, numpy ndarray or
        azureml.dataprep.Dataflow
        :param y_valid: validation labels
        :type y_valid: pandas DataFrame, numpy ndarray or
        azureml.dataprep.Dataflow
        :param sample_weight_valid:
        :type sample_weight_valid: pandas DataFrame, numpy ndarray or
        azureml.dataprep.Dataflow
        :param cv_splits_indices: Indices where to split training data for
        cross validation
        :type cv_splits_indices: list(int), or list(Dataflow) in which each
        Dataflow represent a train-valid set
                                 where 1 indicates record for training and 0
                                 indicates record for validation
        :param show_output: Flag whether to print output to console
        :type show_output: bool
        :return:
        """
        if show_output:
            self._console_writer = ConsoleWriter(sys.stdout)

        return self._fit_local(
            X=X,
            y=y,
            sample_weight=sample_weight,
            X_valid=X_valid,
            y_valid=y_valid,
            cv_splits_indices=cv_splits_indices,
            existing_run=existing_run,
            sample_weight_valid=sample_weight_valid)

    def _fit_local(
            self,
            X=None,
            y=None,
            sample_weight=None,
            X_valid=None,
            y_valid=None,
            sample_weight_valid=None,
            cv_splits_indices=None,
            existing_run=False):
        """
        Main logic for executing a local AutoML experiment
        :return: NativeAutoMLRun
        """
        with logging_utilities.log_activity(logger=logger, activity_name=constants.TelemetryConstants.TIME_FIT_NAME):
            #  Prepare data before entering for loop
            logger.info("Extracting user Data")
            verifier = VerifierManager()

            self.raw_experiment_data = training_utilities.prepare_raw_experiment_data(
                X, y, sample_weight,
                X_valid, y_valid, sample_weight_valid,
                cv_splits_indices=cv_splits_indices, user_script=self.user_script,
                automl_settings=self.automl_settings,
                verifier=verifier)
            training_utilities._validate_user_experiment_data(self.raw_experiment_data, self.automl_settings)
            training_utilities.auto_block_models(self.raw_experiment_data, self.automl_settings)

            self.subsampling = False
            if hasattr(self.automl_settings, 'enable_subsampling') and \
                    self.automl_settings.enable_subsampling:
                num_samples = self.raw_experiment_data.X.shape[0]
                # TODO: according to Evan, this function will probably need to be refactored later. Since we calculate
                #  these stats in problem info, passing that object in might be better
                self.subsampling = utilities.subsampling_recommended(num_samples)

            if not existing_run:
                self.parent_run_id = 'AutoMLNativeClient_ParentRun_{}'.format(uuid.uuid4())
                log_server.update_custom_dimension(parent_run_id=self.parent_run_id)
                self.current_run = NativeAutoMLRun(
                    self.parent_run_id,
                    self.automl_settings.path,
                    self.automl_settings
                )

            dependencies = {
                'dependencies_versions': json.dumps(package_utilities.get_sdk_dependencies())
            }

            self.current_run.add_properties(dependencies)

            self._console_writer.println("Parent Run ID: " + self.parent_run_id)
            logger.info("Parent Run ID: " + self.parent_run_id)

            self._status = constants.Status.InProgress

            if self.automl_settings.experiment_timeout_minutes is not None:
                experiment_timeout_timer = Timer(self.automl_settings.experiment_timeout_minutes * 60, self.cancel)
                experiment_timeout_timer.daemon = True
                experiment_timeout_timer.start()
                self.experiment_start_time = datetime.utcnow()

            # Init the onnx converter with the original X.
            from . import __version__
            pkg_ver = __version__
            enable_split_onnx_models = self.automl_settings.enable_split_onnx_featurizer_estimator_models
            self.onnx_cvt = OnnxConverter(version=pkg_ver,
                                          is_onnx_compatible=self.automl_settings.enable_onnx_compatible_models,
                                          enable_split_onnx_featurizer_estimator_models=enable_split_onnx_models)
            onnx_mdl_name = '{}[{}]'.format(OnnxConvertConstants.OnnxModelNamePrefix, self.parent_run_id)
            onnx_mdl_desc = {'ParentRunId': self.parent_run_id}
            self.onnx_cvt.initialize_input(X=self.raw_experiment_data.X,
                                           x_raw_column_names=self.raw_experiment_data.feature_column_names,
                                           model_name=onnx_mdl_name,
                                           model_desc=onnx_mdl_desc)

            cache_store = self._get_cache_store(self.automl_settings)
            expr_store = ExperimentStore(cache_store, read_only=False)
            try:
                transformed_data_context = self._get_transformed_context(verifier=verifier, cache_store=cache_store)

                problem_info = self.get_problem_info(
                    transformed_data_context.X,
                    transformed_data_context.y)
                logger.info('Problem info: {}'.format(json.dumps(problem_info)))

                training_utilities.build_experiment_store(
                    transformed_data_context,
                    cache_store=cache_store,
                    task_type=self.automl_settings.task_type,
                    experiment_data_settings=ExperimentDataSettings(self.automl_settings),
                    experiment_control_settings=ExperimentControlSettings(self.automl_settings),
                    init_all_stats=False,
                    keep_in_memory=False)

                expr_store.unload()
            finally:
                # Reset ExperimentStore instance to change r/w flag
                ExperimentStore.reset()

            logger.info("Initialized experiment store object from transformed_data_context. Deleting "
                        "transformed_data_context.")
            self._gc_transfromed_data_context(transformed_data_context)

            run_obj = NativeAutoMLRun(self.parent_run_id, self.automl_settings.path)
            parent_run_context = OfflineAutoMLRunContext(run_obj)
            verifier.write_result_file(parent_run_context)

            try:
                #  Set up interface to print execution progress
                ci = ConsoleInterface("score", self._console_writer)
                ci.print_guardrails(verifier.ret_dict['faults'], number_parameters_output=5)
                ci.print_descriptions()
                ci.print_columns()
            except Exception:
                raise

            self.current_iter = 0
            self.fit_outputs = []

            try:
                logger.info("Start local loop.")
                expr_store = ExperimentStore(cache_store, read_only=False)
                expr_store.load()
                while self.current_iter < self.automl_settings.iterations:
                    logger.info("Start iteration: {0}".format(self.current_iter))
                    if self._status == constants.Status.Terminated:
                        self._console_writer.println("Stopping criteria reached. Ending experiment.")
                        logger.info("Stopping criteria reached. Ending experiment.")
                        return self.current_run
                    result = self._fit_iteration(
                        ci,
                        problem_info=problem_info
                    )

                    if result is False:
                        logger.info("Service ran out of pipelines to suggest. Ending experiment.")
                        break

                # create the AutoML Run object eagerly so that we can create a
                # child iteration for ensembling (if required)
                self.current_run = NativeAutoMLRun(
                    self.parent_run_id,
                    self.automl_settings.path,
                    self.automl_settings
                )

                self._status = constants.Status.Completed
                self.current_run.complete()
            except KeyboardInterrupt:
                self._status = constants.Status.Terminated
                logger.info("[ParentRunId:{}]Received interrupt. Returning now.".format(self.parent_run_id))
                self._console_writer.println("Received interrupt. Returning now.")
            finally:
                cache_clear_status = expr_store.clear()
                if not cache_clear_status:
                    logger.warning("Failed to unload the dataset from cache store.")
                ExperimentStore.reset()

            logger.info("Run Complete.")
            return self.current_run

    def _get_transformed_context(self, cache_store: CacheStore, verifier: VerifierManager) -> \
            TransformedDataContext:
        """Convert the raw data context to transformed data context."""
        if self.raw_experiment_data is None or self.automl_settings is None:
            raise ConfigException._with_error(
                AzureMLError.create(
                    ArgumentBlankOrEmpty, target="raw_experiment_data/automl_settings",
                    argument_name="input_data/automl_settings"
                )
            )

        with logging_utilities.log_activity(logger=logger,
                                            activity_name=constants.TelemetryConstants.PRE_PROCESS_NAME):
            raw_data_context = RawDataContext(
                data_context_params=DataContextParams(self.automl_settings),
                X=self.raw_experiment_data.X,
                y=self.raw_experiment_data.y,
                X_valid=self.raw_experiment_data.X_valid,
                y_valid=self.raw_experiment_data.y_valid,
                sample_weight=self.raw_experiment_data.weights,
                sample_weight_valid=self.raw_experiment_data.weights_valid,
                x_raw_column_names=self.raw_experiment_data.feature_column_names,
                cv_splits_indices=self.raw_experiment_data.cv_splits_indices,
                data_snapshot_str=self.raw_experiment_data.data_snapshot_str
            )

            logger.info("The size of raw data is: " + str(raw_data_context._get_memory_size()))

            # TODO: This should use proper phases.
            feature_sweeped_state_container = data_transformation.get_transformers_for_full_featurization(
                raw_data_context=raw_data_context,
                cache_store=cache_store,
                is_onnx_compatible=self.automl_settings.enable_onnx_compatible_models,
                enable_dnn=self.automl_settings.enable_dnn,
                force_text_dnn=self.automl_settings.force_text_dnn,
                verifier=verifier,
                working_dir=self.automl_settings.path
            )

            transformed_data_context = orchestrate_featurization(
                enable_streaming=self.automl_settings.enable_streaming,
                is_timeseries=self.automl_settings.is_timeseries,
                path=self.automl_settings.path,
                raw_data_context=raw_data_context,
                cache_store=cache_store,
                verifier=verifier,
                experiment_observer=NullExperimentObserver(),
                feature_sweeping_config={},
                feature_sweeped_state_container=feature_sweeped_state_container
            )

            return transformed_data_context

    def _fit_iteration(self, ci, problem_info=None):
        with logging_utilities.log_activity(logger=logger,
                                            activity_name=constants.TelemetryConstants.FIT_ITERATION_NAME):
            run_folder = run.NativeAutoMLRun.get_child_run_folder(self.automl_settings.path,
                                                                  self.current_iter)
            child_run = run.NativeAutoMLRun(run_id=self.get_current_run_id(),
                                            run_folder=run_folder,
                                            settings=self.automl_settings)
            automl_run_context = OfflineAutoMLRunContext(child_run)

            start_iter_time = datetime.utcnow()
            elapsed_seconds = 0
            if self.experiment_start_time is not None:
                elapsed_seconds = int((datetime.utcnow() - self.experiment_start_time).total_seconds())
            early_stopping_reached = False

            #  Query Jasmine for the next set of pipelines to run
            logger.info("Querying Jasmine for next pipeline.")

            if self.is_early_stopping_reached():
                ensemble_pipeline_id = self._get_ensemble_pipeline_on_early_exit()
                if ensemble_pipeline_id is not None:
                    logger.info("Early stopping is reached but still need to run ensemble pipeline ({}).".format(
                        ensemble_pipeline_id))
                    automl_pipeline = self.generate_ensemble_pipeline_spec(
                        ensemble_pipeline_id,
                        automl_run_context)
                else:
                    logger.info("Early stopping is reached. Exit now.")
                    self.cancel()
                    return True
            else:
                automl_pipeline = self._get_pipeline(
                    automl_run_context, problem_info=problem_info, elapsed_seconds=elapsed_seconds)
            if automl_pipeline is None:
                return False

            """
            # TODO: Fix pipeline spec logging (#438111)
            logger.info(
                "Received pipeline: {0}".format(
                    logging_utilities.remove_blacklisted_logging_keys_from_json_str(
                        automl_pipeline.pipeline_script
                    )
                )
            )
            """
            logger.info('Received pipeline ID {}'.format(automl_pipeline.pipeline_id))

            ci.print_start(self.current_iter)
            error = None
            base_automl_run_properties = {
                "iteration": self.current_iter,
                "pipeline_id": automl_pipeline.pipeline_id,
                "pipeline_spec": automl_pipeline.pipeline_script,
                "predicted_time": automl_pipeline.predicted_time,
                "training_percent": automl_pipeline.training_percent
            }
            child_run.add_properties(base_automl_run_properties)
            self.child_metrics_mocks[self.current_iter] = child_run
            fit_output = None

            with log_server.new_log_context(run_id="_".join([self.parent_run_id, str(self.current_iter)])):
                try:
                    # TODO: implement elapsed time properly
                    fit_output = fit_pipeline.fit_pipeline(
                        automl_pipeline,
                        ExperimentControlSettings(self.automl_settings),
                        ExperimentResourceSettings(self.automl_settings),
                        ExperimentOrchestrationSettings(self.automl_settings),
                        PipelineSelectionSettings(self.automl_settings),
                        ExperimentDataSettings(self.automl_settings),
                        automl_run_context,
                        elapsed_time=int(elapsed_seconds / 60),
                        onnx_cvt=self.onnx_cvt
                    )

                    self._terminate_child_run(child_run, fit_output)

                    if len(fit_output.errors) > 0:
                        print(fit_output.errors)
                        err_type = next(iter(fit_output.errors))
                        inner_ex = fit_output.errors[err_type]
                        if isinstance(inner_ex['exception'], TimeoutException):
                            if fit_output._pipeline_run_output:
                                fit_output._pipeline_run_output._fit_time = \
                                    cast(int, self.automl_settings.iteration_timeout_minutes) * 60
                            raise TimeoutException("Fit operation exceeded provided timeout, "
                                                   "terminating and moving onto the next iteration.")
                        else:
                            # TODO: We lose the original traceback, how can we fix this?
                            if fit_output._pipeline_run_output:
                                fit_output._pipeline_run_output._fit_time = float('nan')
                            raise cast(BaseException, inner_ex['exception'])

                except Exception as e:
                    if fit_output is None:
                        fit_output = FitOutput(self.automl_settings.primary_metric,
                                               self.automl_settings.metric_operation,
                                               self.automl_settings.num_classes,
                                               automl_pipeline)
                    error = e
                    logger.error("Unknown exception raised.")

                ci.print_pipeline(fit_output.run_preprocessor, fit_output.run_algorithm, automl_pipeline.training_size)

                if self._score_max is None or np.isnan(self._score_max) or fit_output.score > self._score_max:
                    self._score_max = fit_output.score
                if self._score_min is None or np.isnan(self._score_min) or fit_output.score < self._score_min:
                    self._score_min = fit_output.score
                self.fit_outputs.append(fit_output)
                automl_run_context.save_model_output(fit_output.get_output_dict(exclude_keys=['fitted_pipeline']),
                                                     run.NativeAutoMLRun.FIT_OUTPUT_FILE_NAME,
                                                     self.automl_settings.path)

                end_iter_time = datetime.utcnow()
                start_iter_time = start_iter_time.replace(tzinfo=timezone.utc)
                end_iter_time = end_iter_time.replace(tzinfo=timezone.utc)
                iter_duration = str(end_iter_time - start_iter_time)
                ci.print_end(iter_duration,
                             fit_output.score,
                             self._get_best_pipeline_score())
                self.current_iter = self.current_iter + 1

                if error:
                    ci.print_error(error)

                if self.automl_settings.experiment_exit_score is not None:
                    if self.automl_settings.metric_operation == \
                            constants.OptimizerObjectives.MINIMIZE:
                        if fit_output.score < self.automl_settings.experiment_exit_score:
                            logger.info("Minimized score is less than the input. Exit now.")
                            self.cancel()
                    elif self.automl_settings.metric_operation == \
                            constants.OptimizerObjectives.MAXIMIZE:
                        if fit_output.score > self.automl_settings.experiment_exit_score:
                            logger.info("Maximized score is greater than the input. Exit now.")
                            self.cancel()

                if early_stopping_reached is True:
                    logger.info("The score cannot be improved. Exit now.")
                    self.cancel()

                return True

    def _get_best_pipeline_score(self):
        if self.automl_settings.metric_operation == \
                constants.OptimizerObjectives.MINIMIZE:
            return self._score_min
        elif self.automl_settings.metric_operation == \
                constants.OptimizerObjectives.MAXIMIZE:
            return self._score_max

    def _get_pipeline(self, run_context, problem_info=None, elapsed_seconds=0):
        """
        Get another pipeline to evaluate on the user's dataset

        :return: Pipeline to evaluate next
        """
        with logging_utilities.log_activity(logger=logger,
                                            activity_name=constants.TelemetryConstants.GET_PIPELINE_NAME):
            num_categorical = 0
            num_features = 0
            num_classes = 0
            num_samples = 0
            is_sparse = True

            # default time constraint is one hour per iteration
            time_constraint = constants.AutoMLDefaultTimeouts.DEFAULT_ITERATION_TIMEOUT_SECONDS
            total_time_constraint = constants.AutoMLDefaultTimeouts.DEFAULT_EXPERIMENT_TIMEOUT_SECONDS
            max_time = constants.AutoMLDefaultTimeouts.DEFAULT_EXPERIMENT_TIMEOUT_SECONDS

            if problem_info is not None:
                is_sparse = problem_info.get('is_sparse', True)
                num_categorical = problem_info.get('dataset_num_categorical', 0)
                num_classes = problem_info.get('dataset_classes', 0)
                num_features = problem_info.get('dataset_features', 0)
                num_samples = problem_info.get('dataset_samples', 0)

            if self.automl_settings.iteration_timeout_minutes is not None:
                time_constraint = \
                    self.automl_settings.iteration_timeout_minutes * 60

            if self.automl_settings.experiment_timeout_minutes is not None:
                # should be set to remaining experiment time
                total_time_constraint = \
                    (self.automl_settings.experiment_timeout_minutes * 60) - elapsed_seconds

            if self.automl_settings.experiment_timeout_minutes is not None:
                max_time = \
                    self.automl_settings.experiment_timeout_minutes * 60

            ensemble_pipeline_id = self._get_ensemble_pipeline_id_to_schedule()
            if ensemble_pipeline_id is not None:
                return self.generate_ensemble_pipeline_spec(
                    ensemble_pipeline_id,
                    run_context)

            while True:
                trace_id = str(uuid.uuid4())
                logger.info(
                    "[ExpId:{}][ParentRunId:{}][TraceId:{}][Iteration:{}] "
                    "AutoMLNativeClient: Begin to send out request.".format(
                        self.experiment_id,
                        self.parent_run_id,
                        trace_id,
                        self.current_iter))
                pipeline_candidate = self._provider.get_pipeline(
                    experiment_id=self.experiment_id,
                    run_context=run_context,
                    task_type=self.automl_settings.task_type,
                    metric=self.automl_settings.primary_metric,
                    metric_operation=self.automl_settings.metric_operation,
                    num_threads=self.automl_settings.max_cores_per_iteration,
                    previous_iterations=self.fit_outputs,
                    previous_iteration_numbers=list(range(self.current_iter)),
                    iteration=self.current_iter,
                    total_iterations=self.automl_settings.iterations,
                    is_sparse=is_sparse,
                    num_categorical=num_categorical,
                    num_features=num_features,
                    num_classes=num_classes,
                    num_samples=num_samples,
                    time_constraint=time_constraint,
                    cost_mode=self.automl_settings.cost_mode,
                    headers={
                        'X-Experiment-Id': self.experiment_id,
                        'X-Query-Trace-Id': trace_id,
                        'X-Parent-Run-Id': self.parent_run_id,
                        'X-Run-Iteration-Number': str(self.current_iter)
                    },
                    subsampling=self.subsampling,
                    blacklist_models=self.automl_settings.blacklist_algos,
                    whitelist_models=self.automl_settings.whitelist_models,
                    customer=self._customer,
                    total_time_constraint=total_time_constraint,
                    max_time=max_time
                )
                logger.info(
                    "[ExpId:{}][ParentRunId:{}][TraceId:{}][Iteration:{}] "
                    "AutoMLNativeClient: Received response.".format(
                        self.experiment_id,
                        self.parent_run_id,
                        trace_id,
                        self.current_iter))

                return pipeline_candidate

    def get_problem_info(self,
                         X,
                         y):
        """
        Determine the problem info dict to be used when talking to Miro

        :param X: Training data
        :type X: pandas DataFrame, numpy ndarray or azureml.dataprep.Dataflow
        :param y: Training labels
        :type y: pandas DataFrame, numpy ndarray or azureml.dataprep.Dataflow
        :return: A dict containing Miro problem info
        """
        problem_info_dict = {
            "dataset_num_categorical": 0,
            "dataset_classes": len(np.unique(y)),
            "dataset_features": X.shape[1],
            "dataset_samples": X.shape[0],
            "is_sparse": scipy.sparse.issparse(X)
        }

        return problem_info_dict

    def generate_ensemble_pipeline_spec(self,
                                        pipeline_id: str,
                                        run_context: AutoMLAbstractRunContext) -> AutoMLPipeline:
        module = None
        class_name = None
        if pipeline_id == constants.EnsembleConstants.VOTING_ENSEMBLE_PIPELINE_ID:
            module = "automl.client.core.nativeclient.ensemble"
            class_name = "Ensemble"
        elif pipeline_id == constants.EnsembleConstants.STACK_ENSEMBLE_PIPELINE_ID:
            module = "automl.client.core.nativeclient.stack_ensemble"
            class_name = "StackEnsemble"
        else:
            raise ValueError("Unsupported pipeline_id ({}) for Ensemble iteration. Supported ones: {}".format(
                pipeline_id, constants.EnsembleConstants.ENSEMBLE_PIPELINE_IDS))

        ensemble_spec = {
            "pipeline_id": pipeline_id,
            "objects": [{
                "module": module,
                "class_name": class_name,
                "spec_class": pipeline_spec.SDK_ENSEMBLE_NAME,
                "param_args": [],
                "param_kwargs": {
                    "automl_settings": self.automl_settings.__dict__,
                    "ensemble_run_id": run_context.run_id
                },
            }],
        }

        return AutoMLPipeline(run_context=run_context,
                              pipeline_script=json.dumps(ensemble_spec),
                              pipeline_id=pipeline_id)

    def get_current_run_id(self) -> str:
        return '{}_{}'.format(self.parent_run_id, self.current_iter)

    def is_early_stopping_reached(self):
        invalid_score = float('nan')
        if self.automl_settings.enable_early_stopping is True and self.current_iter > \
                (self.automl_settings.early_stopping_n_iters + constants.EARLY_STOPPING_NUM_LANDMARKS):

            lookback = -1 * self.automl_settings.early_stopping_n_iters
            lookback_pipelines = self.fit_outputs[lookback:]
            best_score = self._get_best_pipeline_score()

            required_ensemble_ids = self._get_required_ensemble_pipelines()

            for pipeline in lookback_pipelines:
                if pipeline.pipeline_id in required_ensemble_ids:
                    continue
                elif pipeline.score == invalid_score:
                    continue
                elif pipeline.score == best_score:
                    return False
            return True
        return False

    @property
    def _validation_scores(self):
        """Shim to avoid breaking PowerBI. This should be removed when possible."""
        return [output.get_output_dict() for output in self.fit_outputs]

    def _get_ensemble_pipeline_on_early_exit(self):
        required_ensemble_pipelines = self._get_required_ensemble_pipelines()
        valid_scores = [p.score for p in self.fit_outputs if not np.isnan(p.score)]
        if len(valid_scores) < 2:
            # if we don't have at least 2 successful iteration, no need to schedule ensemble iterations
            return None

        # we need to figure out which ensemble pipelines we might have already ran
        already_ran_pipeline_ids = [r.get_properties().get('pipeline_id')
                                    for _, r in self.child_metrics_mocks.items()]
        ensemble_pipelines_still_needed = list(
            [p for p in required_ensemble_pipelines if p not in already_ran_pipeline_ids])
        if len(ensemble_pipelines_still_needed) == 0:
            return None
        return ensemble_pipelines_still_needed[0]

    def _get_ensemble_pipeline_id_to_schedule(self):
        required_ensemble_pipelines = self._get_required_ensemble_pipelines()
        total_ensemble_runs = len(required_ensemble_pipelines)
        if total_ensemble_runs == 0:
            # get out early. no Ensemble iterations are needed
            return None
        valid_scores = [p.score for p in self.fit_outputs if not np.isnan(p.score)]
        if len(valid_scores) < 2:
            # if we don't have at least 2 successful iteration, no need to schedule ensemble iterations
            return None
        result = None
        if total_ensemble_runs == 1:
            if self.automl_settings.iterations == self.current_iter + 1:
                # the last iteration needs to be an Ensemble one
                result = required_ensemble_pipelines[0]
        else:
            # we need to be running 2 Ensemble iterations
            if self.automl_settings.iterations == self.current_iter + 2:
                result = required_ensemble_pipelines[0]
            elif self.automl_settings.iterations == self.current_iter + 1:
                result = required_ensemble_pipelines[1]

        return result

    def _get_required_ensemble_pipelines(self):
        # based on the current automl settings, figure out which ensemble pipelines we're supposed to schedule.
        ensemble_pipeline_ids = []
        if self.automl_settings.enable_ensembling:
            ensemble_pipeline_ids.append(constants.EnsembleConstants.VOTING_ENSEMBLE_PIPELINE_ID)
        if self.automl_settings.enable_stack_ensembling:
            ensemble_pipeline_ids.append(constants.EnsembleConstants.STACK_ENSEMBLE_PIPELINE_ID)

        return ensemble_pipeline_ids

    def _get_cache_store(self, automl_settings: AutoMLBaseSettings) -> CacheStore:
        logger.info('Using local disk as cache store.')
        temp_dir = self.parent_run_id if self.parent_run_id else str(uuid.uuid4())
        return LazyFileCacheStore(os.path.join(automl_settings.path, temp_dir))

    def _get_onnx_model_from_fit_output(self, fit_output: FitOutput,
                                        return_split_onnx_model: Optional[SplitOnnxModelName]
                                        ) -> Any:
        onnx_model = None
        if return_split_onnx_model is None:
            onnx_model = fit_output.onnx_model
        elif return_split_onnx_model == SplitOnnxModelName.FeaturizerOnnxModel:
            onnx_model = fit_output.onnx_featurizer_model
        elif return_split_onnx_model == SplitOnnxModelName.EstimatorOnnxModel:
            onnx_model = fit_output.onnx_estimator_model
        return onnx_model

    def _gc_transfromed_data_context(self, transformed_data_context):
        if transformed_data_context:
            transformed_data_context._clear_cache()
            del transformed_data_context
            gc.collect()

    def _terminate_child_run(self, child_run: NativeAutoMLRun, fit_output: FitOutput) -> None:
        """
        Sets the child run status to either 'Completed' or 'Failed'.
        If there were any critical errors while fitting, the run is transitioned to a 'Failed' state.
        """
        for fit_exception in fit_output.errors.values():
            if fit_exception.get("is_critical"):
                exception = cast(BaseException, fit_exception.get("exception"))
                interpreted_exception = utilities.interpret_exception(exception, is_aml_compute=False)
                child_run.fail(interpreted_exception)
                return

        child_run.complete()
