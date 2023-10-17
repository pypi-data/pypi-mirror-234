import json
from automl.client.core.nativeclient import AutoMLNativeClient
from automl.client.core.nativeclient._miroproxyclientv2 import MiroProxyClientV2

automl_settings = {
    "name": "AutoML_NativeClient_TestExperiment",
    "max_time_sec": 12000,
    "acquisition_function": "EI",
    "acquisition_param": 0.0,
    "iterations": 3,
    "featurization": 'off',
    "extra_parm": "value",
    "num_cross_folds": 5,
    "primary_metric": 'AUC_weighted',
    'task_type': 'classification',
    'n_cross_validations': 2,
    'debug_flag': {'service_url': 'url'},
    'debug_log': 'automl_tests.log',
}

automl_settings_onnx = {
    "name": "AutoML_NativeClient_TestExperiment",
    "max_time_sec": 12000,
    "acquisition_function": "EI",
    "acquisition_param": 0.0,
    "iterations": 3,
    "featurization": 'off',
    "extra_parm": "value",
    "num_cross_folds": 5,
    "primary_metric": 'AUC_weighted',
    'task_type': 'classification',
    'n_cross_validations': 2,
    'enable_tf': False,
    'debug_flag': {'service_url': 'url'},
    'debug_log': 'automl_tests.log',
    'enable_onnx_compatible_models': True
}


class DummyAuth:
    @staticmethod
    def get_authentication_header():
        auth_header = {"Authorization": "Bearer dummy"}
        return auth_header


class DummyServiceContext:
    @staticmethod
    def get_auth():
        return DummyAuth()

    @staticmethod
    def _get_jasmine_url():
        return 'http://localhost'


class DummyWorkspace:
    def __init__(self):
        self.service_context = DummyServiceContext()
        self.subscription_id = 'dummy'
        self.resource_group = 'dummy'
        self.name = 'dummy'


def native_client_get_automl(settings=automl_settings):
    automl = AutoMLNativeClient(workspace=DummyWorkspace())
    automl.initialize_client(**settings)
    native_client_patch_pipeline_provider(automl)
    automl.automl_settings.compute_target = 'local'
    return automl


def native_client_get_automl_onnx(settings=automl_settings_onnx):
    automl = AutoMLNativeClient(workspace=DummyWorkspace())
    automl.initialize_client(**settings)
    native_client_patch_pipeline_provider(automl)
    automl.automl_settings.compute_target = 'local'
    return automl


def native_client_patch_pipeline_provider(client):
    pipeline_spec = {
        "objects":
        [
            {
                "class_name": "RobustScaler",
                "module": "sklearn.preprocessing",
                "param_args": [],
                "param_kwargs":{
                    "quantile_range": [25, 75],
                    "with_centering": True,
                    "with_scaling": True
                },
                "prepared_kwargs": {},
                "spec_class": "preproc"
            },
            {
                "class_name": "LogisticRegression",
                "module": "sklearn.linear_model",
                "param_args": [],
                "param_kwargs": {
                    "C": 2222.996482526191,
                    "class_weight": None,
                    "multi_class": "ovr",
                    "penalty": "l2",
                    "solver": "lbfgs"
                },
                "prepared_kwargs": {},
                "spec_class": "sklearn"
            }
        ],
        "pipeline_id": "32081822105cbea9293fb4ed53b246b572236e7f"
    }

    result = {
        "pipeline_id": pipeline_spec["pipeline_id"],
        "pipeline_spec": json.dumps(pipeline_spec),
        "training_percent": "100",
    }
    client._provider = MiroProxyClientMock(return_value=result)


def native_client_patch_forecast_provider(client):
    pipeline_spec = {
        "objects":
        [
            {
                "class_name": "StandardScaler",
                "module": "sklearn.preprocessing",
                "param_args": [],
                "param_kwargs":{
                    "with_mean": True,
                    "with_std": True
                },
                "prepared_kwargs": {},
                "spec_class": "preproc"
            },
            {
                "class_name": "ElasticNet",
                "module": "sklearn.linear_model",
                "param_args": [],
                "param_kwargs": {
                    'alpha': 0.5267894736842105,
                    'copy_X': True,
                    'fit_intercept': True,
                    'l1_ratio': 0.791578947368421,
                    'max_iter': 1000,
                    'normalize': False,
                    'positive': False,
                    'precompute': False,
                    'random_state': 42,
                    'selection': 'cyclic',
                    'tol': 0.0001,
                    'warm_start': False
                },
                "prepared_kwargs": {},
                "spec_class": "sklearn"
            }
        ],
        "pipeline_id": "32081822105cbea9293fb4ed53b246b572236e7f"
    }

    result = {
        "pipeline_id": pipeline_spec["pipeline_id"],
        "pipeline_spec": json.dumps(pipeline_spec),
        "training_percent": "100",
    }
    client._provider = MiroProxyClientMock(return_value=result)


class MiroProxyClientMock(MiroProxyClientV2):
    def __init__(self, return_value):
        self.return_value = return_value
        super().__init__(DummyWorkspace())

    def _make_request(self, *args):
        return self.return_value
