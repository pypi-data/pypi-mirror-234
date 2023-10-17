import logging
import os
import sys
import unittest.mock

import pytest

from azureml.automl.core.automl_base_settings import AutoMLBaseSettings
from azureml.automl.core._logging import log_server


@pytest.fixture(scope="session")
def worker_id(request):
    if hasattr(request.config, "workerinput"):
        return request.config.workerinput["workerid"]
    else:
        return "master"


@pytest.fixture(scope="session", autouse=True)
def set_data_home(worker_id):
    os.environ["SCIKIT_LEARN_DATA"] = os.path.join(os.path.expanduser("~"), "scikit_learn_data", worker_id)


@pytest.fixture(scope="session", autouse=True)
def per_session_init():
    from azureml._logging import debug_mode as aml_debug_mode

    aml_debug_mode.debug_sdk()


@pytest.fixture(autouse=True)
def per_test_init(request, monkeypatch, tmp_path):
    # Make sure sys.path contains the test module
    test_dir = os.path.abspath(os.path.dirname(request.fspath.strpath))
    if test_dir not in sys.path:
        sys.path.append(test_dir)

    # Create temp folder for each test to prevent collisions
    old_path = os.getcwd()
    os.chdir(str(tmp_path))

    # Disable logging to file and propagate logs to root logger for pytest capture
    monkeypatch.setattr(AutoMLBaseSettings, "_init_logging", lambda *args: None)
    log_server.DEBUG_MODE = True
    log_server.install_handler("azureml")
    verbosity = os.environ.get("test_log_verbosity", logging.INFO)
    log_server.set_verbosity(verbosity)
    logging.getLogger().setLevel(verbosity)

    # Make sure tests clean up logging handlers to prevent ValueErrors
    old_handle_error = logging.Handler.handleError

    def handleError(record):
        t, v, tb = sys.exc_info()
        if str(v) == "I/O operation on closed file":
            pytest.fail("Clean up test log handlers using log_server.remove_handler()")
        old_handle_error(record)
        pytest.fail("Error in logging system, see stderr for details")
    monkeypatch.setattr(logging.Handler, "handleError", handleError)

    yield

    # Reset the working directory after the test to prevent weird issues
    os.chdir(old_path)


def to_alphanum(s):
    return "".join([x if x.isalnum() else "_" for x in s])


def append_path(original, new_path):
    if not original:
        return new_path
    return "{}:{}".format(original, new_path)
