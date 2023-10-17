# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import sys
from azureml.automl.core.shared import logging_utilities
from azureml.automl.core._logging import log_server
from .automlclassifier import AutoMLClassifier
from .automlregressor import AutoMLRegressor
from .automlforecaster import AutoMLForecaster
from .automlnativeclient import AutoMLNativeClient

__all__ = [
    'AutoMLNativeClient',
    'AutoMLClassifier',
    'AutoMLRegressor',
    'AutoMLForecaster'
]

try:
    from ._version import ver as VERSION
    __version__ = VERSION
except ImportError:
    VERSION = '0.0.0+dev'
    __version__ = VERSION

# Mark this package as being allowed to log certain built-in types
module = sys.modules[__name__]
logging_utilities.mark_package_exceptions_as_loggable(module)

log_server.install_handler('automl.client.core.nativeclient')
