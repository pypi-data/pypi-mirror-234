import os
import shutil
import tempfile
import unittest

import numpy as np
import sklearn

from azureml.automl.core.shared import constants
from azureml.automl.core.shared.exceptions import ConfigException
from azureml.automl.runtime._run_history.offline_automl_run import OfflineAutoMLRunContext
from azureml.automl.runtime.shared import model_wrappers
from azureml.automl.runtime.fit_output import FitOutput
from azureml.automl.runtime.automl_pipeline import AutoMLPipeline
from azureml.automl.runtime.pipeline_run_helper import PipelineRunOutput
from automl.client.core.nativeclient.run import NativeAutoMLRun
from nativeclient_mocks import native_client_get_automl, native_client_get_automl_onnx, automl_settings,\
    automl_settings_onnx


class GetData(object):
    def __init__(self, data_dict):
        self.data_dict = data_dict

    def get_data(self):
        return self.data_dict


class NativeClientFitTests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(NativeClientFitTests, self).__init__(*args, **kwargs)

        from sklearn import datasets
        digits = datasets.load_digits()
        self.X_digits = digits.data[10:, :]
        self.y_digits = digits.target[10:]
        self.images = digits.images[:10]
        self.working_folder = None
        self.automl_onnx_settings = None
        self.automl_settings = None

    def setUp(self):
        self.working_folder = tempfile.mkdtemp(dir=os.getcwd(), prefix="nativeclienttest_")
        settings = automl_settings.copy()
        settings['path'] = self.working_folder
        self.automl_settings = settings

        onnx_settings = automl_settings_onnx.copy()
        onnx_settings['path'] = self.working_folder
        self.automl_onnx_settings = onnx_settings

    def tearDown(self):
        if self.working_folder is not None:
            shutil.rmtree(self.working_folder)

    def test_fit(self):
        automl = native_client_get_automl(self.automl_settings)
        local_run = automl.fit(X=self.X_digits, y=self.y_digits, compute_target='local', show_output=True)
        scores, fitted_model = local_run.get_output()
        for index in range(min(len(self.y_digits), 10)):
            fitted_model.predict(self.X_digits[index:index + 1])[0]

    def test_fit_ensemble(self):
        self.automl_settings['iterations'] = 4
        automl = native_client_get_automl(self.automl_settings)
        local_run = automl.fit(X=self.X_digits, y=self.y_digits, compute_target='local', show_output=True)
        total_pipelines = len(automl.fit_outputs)
        # Ensemble is only enabled when we're running at least 3 iterations
        voting_iteration_index = total_pipelines - 2
        voting_pipeline = automl.fit_outputs[voting_iteration_index]
        self.assertEqual(constants.EnsembleConstants.VOTING_ENSEMBLE_PIPELINE_ID, voting_pipeline.pipeline_id)
        _, fitted_pipeline = local_run.get_output(iteration=voting_iteration_index)
        self.assertIsInstance(fitted_pipeline, sklearn.pipeline.Pipeline)
        self.assertIsInstance(fitted_pipeline._final_estimator, model_wrappers.PreFittedSoftVotingClassifier)

        stack_iteration_index = total_pipelines - 1
        stack_pipeline = automl.fit_outputs[stack_iteration_index]
        self.assertEqual(constants.EnsembleConstants.STACK_ENSEMBLE_PIPELINE_ID, stack_pipeline.pipeline_id)
        _, fitted_pipeline = local_run.get_output(iteration=stack_iteration_index)
        self.assertIsInstance(fitted_pipeline, sklearn.pipeline.Pipeline)
        self.assertIsInstance(fitted_pipeline._final_estimator, model_wrappers.StackEnsembleClassifier)

    def test_ensemble_disabled_when_no_successful_iterations(self):
        self.automl_settings['iterations'] = 5
        automl = native_client_get_automl(self.automl_settings)
        automl.parent_run_id = "automl_parent_run"
        child_metrics = NativeAutoMLRun(
            run_id=automl.parent_run_id, run_folder=os.getcwd(), settings=automl.automl_settings)
        automl_run_context = OfflineAutoMLRunContext(child_metrics)

        # fake the previous iteration results to be all NaN
        automl.fit_outputs = []
        pipelineResult = AutoMLPipeline(automl_run_context, pipeline_script="", pipeline_id="pipeline_id")

        primary_metric = automl.automl_settings.primary_metric
        metric_operation = automl.automl_settings.metric_operation
        num_classes = automl.automl_settings.num_classes

        automl.fit_outputs.append(FitOutput(primary_metric, metric_operation, num_classes, pipelineResult))
        automl.fit_outputs.append(FitOutput(primary_metric, metric_operation, num_classes, pipelineResult))
        automl.fit_outputs.append(FitOutput(primary_metric, metric_operation, num_classes, pipelineResult))
        automl.fit_outputs.append(FitOutput(primary_metric, metric_operation, num_classes, pipelineResult))
        automl.current_iter = 4
        pipeline = automl._get_pipeline(automl_run_context, None)
        self.assertNotIn(pipeline.pipeline_id, constants.EnsembleConstants.ENSEMBLE_PIPELINE_IDS)
        pipeline = automl._get_ensemble_pipeline_on_early_exit()
        self.assertIsNone(pipeline)

        # now we change the last iteration to be successful, there should still be no ensemble scheduled
        fitted_pipeline = sklearn.pipeline.Pipeline(steps=[("bla", sklearn.linear_model.LogisticRegression())])
        result = PipelineRunOutput(
            automl.automl_settings.task_type,
            automl.automl_settings.enable_streaming,
            pipeline_obj=fitted_pipeline,
            training_type=None)
        result.record_pipeline_output(
            scores={"AUC_weighted": 0.5},
            fit_time=10,
            fitted_pipeline=fitted_pipeline,
            fitted_pipelines_train=None,
            training_percent=100)
        automl.fit_outputs[3].record_pipeline_results(result)
        automl.current_iter = 4
        pipeline = automl._get_pipeline(automl_run_context, None)
        self.assertNotIn(pipeline.pipeline_id, constants.EnsembleConstants.ENSEMBLE_PIPELINE_IDS)
        pipeline = automl._get_ensemble_pipeline_on_early_exit()
        self.assertIsNone(pipeline)

        # now add one more successful iteration and assert that we get an Ensemble upon a call to get_pipeline
        automl.fit_outputs[2].record_pipeline_results(result)
        automl.current_iter = 4
        pipeline = automl._get_pipeline(automl_run_context, None)
        self.assertIn(pipeline.pipeline_id, constants.EnsembleConstants.ENSEMBLE_PIPELINE_IDS)
        pipeline = automl._get_ensemble_pipeline_on_early_exit()
        self.assertIn(pipeline, constants.EnsembleConstants.ENSEMBLE_PIPELINE_IDS)

    def test_fit_onnx(self):
        automl = native_client_get_automl(self.automl_onnx_settings)
        local_run = automl.fit(X=self.X_digits, y=self.y_digits, compute_target='local', show_output=True)
        scores, onnx_model = local_run.get_output(return_onnx_model=True)
        self.assertIsNotNone(onnx_model)

    def test_fit_return_best_pipeline_with_nan(self):
        automl = native_client_get_automl(self.automl_settings)

        primary_metric = automl.automl_settings.primary_metric
        metric_operation = automl.automl_settings.metric_operation
        num_classes = automl.automl_settings.num_classes

        local_run = automl.fit(X=self.X_digits, y=self.y_digits, compute_target='local', show_output=True)
        automl.fit_outputs.append(FitOutput(primary_metric, metric_operation, num_classes, None))
        scores, fitted_model = local_run.get_output()
        for index in range(min(len(self.y_digits), 10)):
            fitted_model.predict(self.X_digits[index:index + 1])[0]


class NativeClientModelExplanationTests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(NativeClientModelExplanationTests, self).__init__(*args,
                                                                **kwargs)

        from sklearn import datasets
        digits = datasets.load_digits()
        self.X_digits = digits.data[10:, :]
        self.y_digits = digits.target[10:]
        self.X_valid = digits.data[0:2]
        self.images = digits.images[:10]

    def setUp(self):
        self.working_folder = tempfile.mkdtemp(dir=os.getcwd(), prefix="nativeclient_explain_")
        settings = automl_settings.copy()
        settings['path'] = self.working_folder
        self.automl = native_client_get_automl(settings)

    def tearDown(self):
        if self.working_folder is not None:
            shutil.rmtree(self.working_folder, ignore_errors=True)


if __name__ == "__main__":
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
