# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from typing import Any, BinaryIO, cast, Dict, List, Optional, TextIO, Tuple, Union
from functools import lru_cache
from io import IOBase
from shutil import copyfile
import json
import os
import pickle
import re
import sys

import numpy as np
from azureml._common._error_definition import AzureMLError

from azureml.automl.core.shared import constants, utilities
from azureml.automl.core.shared._diagnostics.automl_error_definitions import ConflictingValueForArguments, \
    InvalidArgumentWithSupportedValues, ModelMissing
from azureml.automl.core.shared._diagnostics.contract import Contract
from azureml.automl.core.shared.exceptions import AutoMLException, ConfigException, OnnxConvertException
from azureml.automl.core.console_interface import ConsoleInterface
from azureml.automl.core.console_writer import ConsoleWriter
from azureml.automl.core.onnx_convert.onnx_convert_constants import SplitOnnxModelName, OnnxConvertConstants
from azureml.automl.runtime._run_history.offline_automl_run import OfflineAutoMLRunBase
from azureml.automl.runtime.onnx_convert import OnnxConverter
from .nativeclient_settings import AutoMLNativeClientSettings


class NativeAutoMLRun(OfflineAutoMLRunBase):
    FIT_OUTPUT_FILE_NAME = "fit_output.pkl"
    CHILD_RUN_FOLDER_PREFIX = "_child_"

    def __init__(self, run_id: str, run_folder: str, settings: Optional[AutoMLNativeClientSettings] = None) -> None:
        super().__init__(run_id, run_folder)
        if settings:
            self.add_properties({
                'AMLSettingsJsonString': json.dumps(settings.as_serializable_dict())
            })
        self._cached_fit_output_dict = None

    def __getitem__(self, key: str) -> Any:
        """
        Get item from the fit output for this run via the bracket operator. Provides backwards compatibility for
        the dictionary formerly returned by AutoMLLocalRun.

        :param key: The key whose value needs to be obtained from the run object.
        :return:
        """
        if key == 'fitted_pipeline':
            path = os.path.join(self.run_folder, constants.MODEL_PATH)
            with open(path, 'rb') as f:
                return pickle.load(f)
        if self._cached_fit_output_dict is None:
            path = os.path.join(self.run_folder, NativeAutoMLRun.FIT_OUTPUT_FILE_NAME)
            with open(path, 'rb') as f:
                self._cached_fit_output_dict = pickle.load(f)
        assert self._cached_fit_output_dict is not None
        return self._cached_fit_output_dict[key]

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        """
        Get item from the fit output for this run. Provides backwards compatibility for the dictionary formerly
        returned by AutoMLLocalRun.

        :param key:
        :param default:
        :return:
        """
        try:
            return self[key]
        except KeyError:
            return default

    def __setitem__(self, key: str, item: Any) -> None:
        """
        Set item to the in-memory copy of fit output for this run via the bracket operator. Changes are not persisted
        to disk. Provides backwards compatibilty for the dictionary formerly returned by AutoMLLocalRun.

        :param key:
        :param item:
        :return:
        """
        if self._cached_fit_output_dict is None:
            path = os.path.join(self.run_folder, NativeAutoMLRun.FIT_OUTPUT_FILE_NAME)
            with open(path, 'rb') as f:
                self._cached_fit_output_dict = pickle.load(f)
        assert self._cached_fit_output_dict is not None
        self._cached_fit_output_dict[key] = item

    @staticmethod
    def get_child_run_folder(path: str, iteration: Any) -> str:
        return os.path.join(path, '{}{}'.format(NativeAutoMLRun.CHILD_RUN_FOLDER_PREFIX, iteration))

    def add_properties(self, properties: Dict[str, Any]) -> None:
        super().add_properties(properties)
        self.get_properties.cache_clear()

    @lru_cache(None)
    def get_properties(self) -> Dict[str, Any]:
        return super().get_properties()

    def set_tags(self, tags: Dict[str, Any]) -> None:
        super().set_tags(tags)
        self.get_tags.cache_clear()

    @lru_cache(None)
    def get_tags(self) -> Dict[str, Any]:
        return super().get_tags()

    @lru_cache(None)
    def get_metrics(self, name: Optional[str] = None, recursive: bool = False, run_type: Optional[Any] = None,
                    populate: bool = False) -> Dict[str, Any]:
        return super().get_metrics(name, recursive, run_type, populate)

    def get_output(self,
                   iteration: Optional[int] = None,
                   metric: Optional[str] = None,
                   return_onnx_model: bool = False,
                   return_split_onnx_model: Optional[SplitOnnxModelName] = None
                   ) -> Tuple['NativeAutoMLRun', Any]:
        """
        Return the best pipeline that has already been tested.

        If no input is provided get_output
        will return the best pipeline according to the primary metric.

        :param iteration: The iteration number of the correspond pipeline spec and fitted model to return.
        :param metric: The metric to use to return the best pipeline spec and fitted model to return.
        :param return_onnx_model: This method will return the converted ONNX model, if user indicated
            the enable_onnx_compatible_models config.
        :return: The best pipeline spec, the corresponding fitted model.
        """
        if iteration is not None and metric is not None:
            raise ConfigException._with_error(
                AzureMLError.create(
                    ConflictingValueForArguments, target="iteration", arguments=', '.join(['metric', 'iteration'])
                )
            )

        if return_onnx_model:
            # Note: if conversion of split models fails, the entire onnx conversion of an iteration will fail.
            # This means that if the conversion of an iteration succeeds, and user set split convert config to true,
            # all the 3 models will be successfully converted.
            if return_split_onnx_model is None:
                model_name = constants.MODEL_PATH_ONNX
            elif return_split_onnx_model == SplitOnnxModelName.FeaturizerOnnxModel:
                model_name = OnnxConvertConstants.FeaturizerOnnxModelPath
            elif return_split_onnx_model == SplitOnnxModelName.EstimatorOnnxModel:
                model_name = OnnxConvertConstants.EstimatorOnnxModelPath
        else:
            model_name = constants.MODEL_PATH

        properties = self.get_properties()
        automl_settings = AutoMLNativeClientSettings(**json.loads(properties['AMLSettingsJsonString']))

        if return_onnx_model and not automl_settings.enable_onnx_compatible_models:
            raise OnnxConvertException("Invalid parameter 'return_onnx_model' passed in.")
        if return_split_onnx_model is not None \
                and not automl_settings.enable_split_onnx_featurizer_estimator_models:
            raise OnnxConvertException("Invalid parameter 'return_split_onnx_model' passed in.")

        if metric is None:
            metric = automl_settings.primary_metric

        if metric in constants.Metric.CLASSIFICATION_SET:
            objective = constants.MetricObjective.Classification[metric]
        elif metric in constants.Metric.REGRESSION_SET:
            objective = constants.MetricObjective.Regression[metric]
        else:
            raise ConfigException._with_error(
                AzureMLError.create(
                    InvalidArgumentWithSupportedValues, target="metric",
                    arguments="metric ({})".format(metric), supported_values=", ".join(constants.Metric.FULL_SET)
                )
            )

        curr_run = None

        child_runs_sorted_with_scores = []
        if iteration is not None:
            curr_run = NativeAutoMLRun(run_id=self.id + '_' + str(iteration),
                                       run_folder=NativeAutoMLRun.get_child_run_folder(self.run_folder, iteration))
        else:
            children = self.get_children(_rehydrate_runs=False)
            best_score = None
            comp = utilities._get_max_min_comparator(objective)
            for child in children:
                candidate_score = child.get_metrics().get(metric, float('nan'))
                if not np.isnan(candidate_score):
                    child_runs_sorted_with_scores.append((child, candidate_score))
                    if best_score is None:
                        best_score = candidate_score
                        curr_run = child
                    else:
                        new_score = comp(best_score, candidate_score)
                        if new_score != best_score:
                            best_score = new_score
                            curr_run = child

            if curr_run is None:
                raise AutoMLException._with_error(
                    AzureMLError.create(ModelMissing, target="metric", metric=metric)
                )

        if return_onnx_model and iteration is None:
            # If returning the ONNX best model,
            # we try to download the best score model, if it's not converted successfully,
            # use the 2nd best score model, and so on.
            is_succeeded = False
            if objective == constants.OptimizerObjectives.MAXIMIZE:
                is_desc = True
            else:
                Contract.assert_true(
                    objective == constants.OptimizerObjectives.MINIMIZE,
                    "Maximization or Minimization could not be determined based on current metric",
                    log_safe=True
                )
                is_desc = False
            # Sort the child run to score tuple list.
            child_runs_sorted_with_scores.sort(key=lambda obj: obj[1], reverse=is_desc)  # type: ignore
            for child_run, _ in child_runs_sorted_with_scores:
                try:
                    onnx_fl = os.path.join(child_run.run_folder, model_name)
                    if os.path.isfile(onnx_fl):
                        # We got the successfully converted ONNX model.
                        curr_run = child_run
                        is_succeeded = True
                        break
                except Exception:
                    continue

            if not is_succeeded:
                # Raise the exception if none of the child runs have converted ONNX model.
                raise OnnxConvertException("All the models in child runs were not able "
                                           "to be converted to the ONNX model.")

        filename = os.path.join(curr_run.run_folder, model_name)

        if return_onnx_model:
            fitted_model = OnnxConverter.load_onnx_model(filename)
        else:
            with open(filename, "rb") as model_file:
                fitted_model = pickle.load(model_file)
        return curr_run, fitted_model

    def get_children(self,
                     recursive: bool = False,
                     tags: Optional[Dict[str, Any]] = None,
                     properties: Optional[Dict[str, Any]] = None,
                     type: Optional[Any] = None,
                     status: Optional[str] = None,
                     _rehydrate_runs: bool = True) -> List['NativeAutoMLRun']:
        os_children = os.listdir(self.run_folder)
        child_run_tuples = [(child[len(NativeAutoMLRun.CHILD_RUN_FOLDER_PREFIX):],
                             os.path.join(self.run_folder, child)) for child in os_children
                            if child.startswith(NativeAutoMLRun.CHILD_RUN_FOLDER_PREFIX)]
        child_runs = [NativeAutoMLRun("{}_{}".format(self.id, iteration), folder)
                      for (iteration, folder) in child_run_tuples]

        return child_runs

    def get_parent_run(self) -> 'NativeAutoMLRun':
        if not self.run_folder.startswith(self.CHILD_RUN_FOLDER_PREFIX):
            raise ValueError('Cannot get parent run of a parent run.')
        match = re.fullmatch(r'(.*)_\d+', self.id)
        if match is None:
            raise ValueError('Unknown run ID format: {}'.format(self.id))
        parent_id = match.group(1)
        return NativeAutoMLRun(parent_id, os.path.dirname(self.run_folder))

    def get_guardrails(self, to_console: bool = True) -> Dict[str, Any]:
        """Print and returns detailed results from running Guardrail verification."""
        writer = ConsoleWriter(sys.stdout)
        ci = ConsoleInterface('verifier_results', writer)
        verifier_results = {}           # type: Dict[str, Any]
        try:
            local_file_path = os.path.join(os.path.curdir, 'verifier_results.json')
            self.download_file(constants.VERIFIER_RESULTS_PATH, local_file_path)
            with open(local_file_path) as a:
                verifier_results = json.load(a)
            if len(verifier_results['faults']) == 0:
                writer.println("Guardrail verification completed without any detected problems.")
            elif to_console:
                ci.print_guardrails(verifier_results['faults'], True)
        except FileNotFoundError:
            writer.println("Current Run does not have Guardrail data.")
        finally:
            os.remove(local_file_path)
            return verifier_results

    def get_run_sdk_dependencies(self, iteration: Optional[int] = None, check_versions: bool = True,
                                 **kwargs: Any) -> Dict[str, str]:
        """
        No-op (this is here mainly for testing purposes).

        :param iteration:
        :param check_versions:
        :param kwargs:
        :return:
        """
        return {}

    def wait_for_completion(self, show_output: bool = False, wait_post_processing: bool = False,
                            raise_on_error: bool = True) -> Dict[str, Any]:
        """
        No-op (this is here mainly for testing purposes).

        :param show_output:
        :param wait_post_processing:
        :param raise_on_error:
        :return:
        """
        return {}
