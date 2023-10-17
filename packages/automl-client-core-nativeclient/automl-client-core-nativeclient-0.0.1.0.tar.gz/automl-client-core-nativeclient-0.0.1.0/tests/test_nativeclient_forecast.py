import os
import math
import unittest

import numpy as np
import pandas as pd
import pytest

from pandas.testing import assert_frame_equal
from pandas.tseries.offsets import DateOffset
from pandas.tseries.frequencies import to_offset
from numpy.ma.testutils import assert_array_equal
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split

from automl.client.core.nativeclient import AutoMLNativeClient
from azureml.automl.core.constants import FeatureType
from azureml.automl.core.featurization.featurizationconfig import FeaturizationConfig
from azureml.automl.core.shared import constants
from azureml.automl.core.shared.constants import TimeSeries, TimeSeriesInternal,\
    ShortSeriesHandlingValues, AggregationFunctions
from azureml.automl.core.shared.exceptions import ConfigException, DataException
from azureml.automl.core.shared.forecasting_exception import ForecastingDataException
from azureml.automl.core.shared.reference_codes import ReferenceCodes

from nativeclient_mocks import DummyWorkspace, native_client_patch_forecast_provider
from pandas.util.testing import assert_series_equal, assert_index_equal

tsind_map = TimeSeriesInternal.TIME_INDEX_FEATURE_NAME_MAP

import logging
rt_logger = logging.getLogger()
rt_logger.setLevel(logging.ERROR)


def quantile(a, q, *args, **kwargs):
    """
    This function is used to provide compatibility between versions of pandas having and
    not having interpolation parameter for the rolling window.
    The issue: pandas < 0.21.rc1 is using lower interpolation in pandas.DataFrame.rolling.quantile
    and this parameter is not tunable. pandas versions between 0.21.rc1 and  0.23.rc2 are
    using linear interpolation in pandas.DataFrame.rolling.quantile and this parameter is not tunable.
    pandas versions >= 0.23.rc2 allow to tune this parameter, but it is linear by default.
    To allow unit tests to go through in the lower versions of pandas we create our own quantile function which behaves
    in the way pandas.DataFrame.rolling.quantile used to work before 0.21.rc1.
    """
    return pd.Series(a).quantile(q, *args, **kwargs)


@pytest.fixture
def automl_settings():
    return {
        "iterations": 3,
        "primary_metric": 'normalized_root_mean_squared_error',
        'task_type': constants.Tasks.REGRESSION,
        'n_cross_validations': None,
        'debug_flag': {'service_url': 'url'},
        'debug_log': 'automl_tests.log',
        'is_timeseries': True,
        'iteration_timeout_minutes': None,
        TimeSeries.TARGET_LAGS: 1,
        TimeSeries.TARGET_ROLLING_WINDOW_SIZE: 5,
        TimeSeries.TIME_COLUMN_NAME: 'date',
        TimeSeries.USE_STL: None,
        TimeSeries.SHORT_SERIES_HANDLING: False,
        TimeSeries.SHORT_SERIES_HANDLING_CONFIG: None
    }


class TestNativeClientForecasting:

    def test_fits_no_grains(self, automl_settings):
        dates_train = list(pd.date_range(start='1991-01-01', end='2000-12-31', freq='QS'))
        is_raining = 20 * [1, 0]
        automl_settings[TimeSeries.GRAIN_COLUMN_NAMES] = None
        automl_settings[TimeSeries.TARGET_ROLLING_WINDOW_SIZE] = None
        automl_settings[TimeSeries.TARGET_LAGS] = None
        automl_settings[TimeSeries.DROP_COLUMN_NAMES] = ['rain']
        dict_train = {'date': dates_train,
                      'rain': is_raining
                      }
        automl = self._create_native_client(automl_settings)
        df_train = pd.DataFrame(data=dict_train)
        X_train = df_train[0:30]
        y_train = np.arange(0, 30)
        X_valid = df_train[30:]
        y_valid = np.arange(0, 10)
        local_run = automl.fit(X=X_train, y=y_train,
                               X_valid=X_valid, y_valid=y_valid,
                               compute_target='local', show_output=False)
        scores, fitted_model = local_run.get_output()
        preds = fitted_model.forecast(X_valid)
        assert len(preds[0]) == X_valid.shape[0], "The array has wrong size."
        assert all([pred is not None for pred in preds[0]]), "Some predictions are NaN"

    def test_fits_with_grains(self, automl_settings):
        """Test if AutoML efficiently fits data with grains."""
        dates_train = 2 * list(pd.date_range(start='1991-01-01', end='2000-12-31', freq='QS'))
        is_raining = 40 * [1, 0]
        automl_settings[TimeSeries.GRAIN_COLUMN_NAMES] = ['store']
        automl_settings[TimeSeries.DROP_COLUMN_NAMES] = ['rain']
        automl_settings[TimeSeries.TARGET_ROLLING_WINDOW_SIZE] = None
        automl_settings[TimeSeries.TARGET_LAGS] = None
        automl = self._create_native_client(automl_settings)
        len_dates = len(dates_train) / 2
        dict_train = {'date': dates_train,
                      'store': list(np.repeat('a', len_dates)) + list(np.repeat('b', len_dates)),
                      'rain': is_raining
                      }
        df_train = pd.DataFrame(data=dict_train)
        X_train = pd.concat([df_train[0:30], df_train[40:70]])
        y_train = np.concatenate([np.arange(0, 30), np.arange(0, 30)])
        X_valid = pd.concat([df_train[30:40], df_train[70:]])
        y_valid = np.concatenate([np.arange(0, 10), np.arange(0, 10)])
        local_run = automl.fit(X=X_train, y=y_train,
                               X_valid=X_valid, y_valid=y_valid,
                               compute_target='local', show_output=False)
        scores, fitted_model = local_run.get_output()
        preds = fitted_model.forecast(X_valid)
        assert len(preds[0]) == X_valid.shape[0], "The array has wrong size."
        assert all([pred is not None for pred in preds]), "Some predictions are NaN"

    def test_leads_are_not_allowed(self, automl_settings):
        """Test if the attempt to create lead will result in error."""
        automl_settings[TimeSeries.GRAIN_COLUMN_NAMES] = None
        automl_settings[TimeSeries.DROP_COLUMN_NAMES] = ['is_raining']
        automl_settings[TimeSeries.TARGET_LAGS] = -2
        with pytest.raises(ConfigException):
            self._create_native_client(automl_settings)
        automl_settings[TimeSeries.TARGET_LAGS] = 0
        with pytest.raises(ConfigException):
            self._create_native_client(automl_settings)

    def test_lag_lead(self, automl_settings):
        """Test if lag-lead operator is plugged in."""
        automl_settings[TimeSeries.GRAIN_COLUMN_NAMES] = None
        automl_settings[TimeSeries.DROP_COLUMN_NAMES] = ['is_raining']
        automl_settings[TimeSeries.TARGET_LAGS] = 2
        automl_settings[TimeSeries.MAX_HORIZON] = 2
        automl_settings[TimeSeries.TARGET_ROLLING_WINDOW_SIZE] = None
        automl = self._create_native_client(automl_settings)
        X_train, y_train, X_valid, y_valid, X_test, y_test = self.get_mock_data(
            automl_settings,
            automl_settings[TimeSeries.MAX_HORIZON])
        # Put some existing column to show it was removed.
        X_train.assign(**{'_lag2': np.repeat(np.NaN, 8)})
        local_run = automl.fit(X=X_train, y=y_train,
                               X_valid=X_valid, y_valid=y_valid,
                               compute_target='local', show_output=False)
        scores, fitted_model = local_run.get_output()
        preds = fitted_model.forecast(X_valid)
        assert len(preds[0]) == 5, "The array has wrong size."
        assert all([p is not None for p in preds[0]]), "Some predictions are NaN"
        # The first step of fitted_model is TimeSeriesTransformer.
        result = fitted_model.steps[0][1].transform(X_valid)
        y = np.zeros(result.shape[0])
        result, y = fitted_model.steps[0][1]._remove_nans_from_look_back_features(result, y)
        # Remove time index featurizer columns.
        lagleaddict = {'date': ['2011-01-09', '2011-01-09', '2011-01-10', '2011-01-10', '2011-01-11'],
                       TimeSeriesInternal.DUMMY_GRAIN_COLUMN: np.repeat('_automl_dummy_grain_col', 5),
                       'origin': ["2011-01-07", "2011-01-08",
                                  "2011-01-08", "2011-01-09",
                                  "2011-01-09"],
                       'temperature_WASNULL': np.repeat(0, 5),
                       tsind_map[TimeSeriesInternal.TIME_INDEX_FEATURE_ID_DAY]: [9, 9, 10, 10, 11],
                       tsind_map[TimeSeriesInternal.TIME_INDEX_FEATURE_ID_WDAY]: [6, 6, 0, 0, 1],
                       tsind_map[TimeSeriesInternal.TIME_INDEX_FEATURE_ID_YEAR_ISO]: [2011, 2011, 2011, 2011, 2011],
                       'temperature': [30, 30, 20, 20, 10],
                       TimeSeriesInternal.DUMMY_TARGET_COLUMN + "_lag2D": [4, 3, 3, 14, 14],
                       TimeSeriesInternal.DUMMY_TARGET_COLUMN + "_WASNULL": 0,
                       TimeSeriesInternal.HORIZON_NAME: [2, 1, 2, 1, 2]
                       }
        df_expected = pd.DataFrame(lagleaddict)
        df_expected['date'] = pd.to_datetime(df_expected['date'])
        df_expected['origin'] = pd.to_datetime(df_expected['origin'])
        df_expected.set_index(['date', '_automl_dummy_grain_col', 'origin'], inplace=True)
        assert_frame_equal(df_expected, result, check_like=True, check_dtype=False)

    def test_lag_lead_with_grains(self, automl_settings):
        """Test lag-lead operator with grain columns."""
        automl_settings[TimeSeries.GRAIN_COLUMN_NAMES] = 'mygrains'
        automl_settings[TimeSeries.DROP_COLUMN_NAMES] = ['is_raining']
        automl_settings[TimeSeries.TARGET_LAGS] = 2
        automl_settings[TimeSeries.TARGET_ROLLING_WINDOW_SIZE] = None
        automl = self._create_native_client(automl_settings)
        X_train, y_train, X_valid, y_valid, X_test, y_test = self.get_mock_grain_data(automl_settings)
        local_run = automl.fit(X=X_train, y=y_train,
                               X_valid=X_valid, y_valid=y_valid,
                               compute_target='local', show_output=False)
        scores, fitted_model = local_run.get_output()
        preds = fitted_model.forecast(X_valid)
        assert len(preds[0]) == X_valid.shape[0], "The array has wrong size."
        assert all([p is not None for p in preds[0]]), "Some predictions are NaN"
        # The first step of fitted_model is TimeSeriesTransformer.
        # This time we will transform X_train, but then we need to add target column to it.
        X_train[TimeSeriesInternal.DUMMY_TARGET_COLUMN] = y_train
        result = fitted_model.steps[0][1].transform(X_train).sort_index()
        y = result.pop(TimeSeriesInternal.DUMMY_TARGET_COLUMN).values
        result, y = fitted_model.steps[0][1]._remove_nans_from_look_back_features(result, y)
        result[TimeSeriesInternal.DUMMY_TARGET_COLUMN] = y
        exp_grains = ['grain1', 'grain2'] * 6
        lagleaddict = {'date': np.repeat(['2011-01-03', '2011-01-04',
                                          '2011-01-05', '2011-01-06',
                                          '2011-01-07', '2011-01-08'], 2),
                       automl_settings[TimeSeries.GRAIN_COLUMN_NAMES]: exp_grains,
                       'origin': np.repeat(['2011-01-02', '2011-01-03',
                                            '2011-01-04', '2011-01-05',
                                            '2011-01-06', '2011-01-07'], 2),
                       'temperature_WASNULL': np.repeat(0, 12),
                       tsind_map[TimeSeriesInternal.TIME_INDEX_FEATURE_ID_DAY]: np.repeat([3, 4, 5, 6, 7, 8], 2),
                       tsind_map[TimeSeriesInternal.TIME_INDEX_FEATURE_ID_WDAY]: np.repeat([0, 1, 2, 3, 4, 5], 2),
                       tsind_map[TimeSeriesInternal.TIME_INDEX_FEATURE_ID_YEAR_ISO]: np.repeat(2011, 12),
                       'temperature': np.repeat([30, 40, 10, 20, 30, 40], 2),
                       TimeSeriesInternal.DUMMY_TARGET_COLUMN: np.repeat([11, 14, 10,
                                                                          4, 3, 14], 2),
                       TimeSeriesInternal.DUMMY_TARGET_COLUMN + "_lag2D": np.repeat([15., 1., 11.,
                                                                                     14., 10., 4.], 2),
                       TimeSeriesInternal.DUMMY_TARGET_COLUMN + "_WASNULL": 0,
                       'grain_mygrains': [0, 1] * 6,
                       TimeSeriesInternal.HORIZON_NAME: np.repeat(1, 12)
                       }
        df_expected = pd.DataFrame(lagleaddict)
        df_expected['date'] = pd.to_datetime(df_expected['date'])
        df_expected['origin'] = pd.to_datetime(df_expected['origin'])
        df_expected.set_index(['date', automl_settings[TimeSeries.GRAIN_COLUMN_NAMES], 'origin'], inplace=True)
        df_expected.sort_index(inplace=True)
        assert_frame_equal(df_expected, result, check_like=True, check_dtype=False)

    def test_rolling_window(self, automl_settings):
        """Test rolling window with additional parameters"""
        automl_settings[TimeSeries.GRAIN_COLUMN_NAMES] = None
        automl_settings[TimeSeries.DROP_COLUMN_NAMES] = ['is_raining']
        automl_settings[TimeSeries.TARGET_ROLLING_WINDOW_SIZE] = 4
        automl_settings[TimeSeries.TARGET_LAGS] = None
        automl_settings[TimeSeries.MAX_HORIZON] = 2
        automl = self._create_native_client(automl_settings)
        X_train, y_train, X_valid, y_valid, X_test, y_test = self.get_mock_data(
            automl_settings,
            automl_settings[TimeSeries.MAX_HORIZON])
        # Put some existing column to show it was removed.
        colname = TimeSeriesInternal.DUMMY_TARGET_COLUMN + '_mean_window4'
        X_train.assign(**{colname: np.repeat(np.NaN, 8)})
        X_valid.assign(**{colname: np.repeat(np.NaN, 5)})
        X_test.assign(**{colname: np.repeat(np.NaN, 5)})
        local_run = automl.fit(X=X_train, y=y_train,
                               X_valid=X_valid, y_valid=y_valid,
                               compute_target='local', show_output=False)
        scores, fitted_model = local_run.get_output()
        preds = fitted_model.forecast(X_valid)
        assert len(preds[0]) == X_valid.shape[0], "The array has wrong size."
        assert all([p is not None for p in preds[0]]), "Some predictions are NaN"
        result = fitted_model.steps[0][1].transform(X_valid).sort_index()
        y = np.zeros(result.shape[0])
        result, y = fitted_model.steps[0][1]._remove_nans_from_look_back_features(result, y)
        window_dict = {'date': ['2011-01-09', '2011-01-09', '2011-01-10'],
                       '_automl_dummy_grain_col': np.repeat('_automl_dummy_grain_col', 3),
                       'also_origin': ["2011-01-07", "2011-01-08", "2011-01-08"],
                       'temperature_WASNULL': np.repeat(0, 3),
                       tsind_map[TimeSeriesInternal.TIME_INDEX_FEATURE_ID_DAY]: [9, 9, 10],
                       tsind_map[TimeSeriesInternal.TIME_INDEX_FEATURE_ID_WDAY]: [6, 6, 0],
                       tsind_map[TimeSeriesInternal.TIME_INDEX_FEATURE_ID_YEAR_ISO]: [2011, 2011, 2011],
                       'temperature': [30, 30, 20],
                       TimeSeriesInternal.DUMMY_TARGET_COLUMN + '_mean_window4D': [7.75, 7.75, 7.75],
                       TimeSeriesInternal.DUMMY_TARGET_COLUMN + '_min_window4D': [3., 3., 3.],
                       TimeSeriesInternal.DUMMY_TARGET_COLUMN + '_max_window4D': [14., 14., 14.],
                       TimeSeriesInternal.DUMMY_TARGET_COLUMN + "_WASNULL": 0,
                       TimeSeriesInternal.HORIZON_NAME: [2, 1, 2]
                       }
        df_expected = pd.DataFrame(window_dict)
        df_expected['date'] = pd.to_datetime(df_expected['date'])
        df_expected['also_origin'] = pd.to_datetime(df_expected['also_origin'])
        df_expected.set_index(['date', '_automl_dummy_grain_col', 'also_origin'], inplace=True)
        assert_frame_equal(df_expected, result, check_like=True, check_dtype=False)

    def test_rolling_window_grains(self, automl_settings):
        """Testing rolling window it there are grains in the data set."""
        automl_settings[TimeSeries.GRAIN_COLUMN_NAMES] = 'mygrain'
        automl_settings[TimeSeries.DROP_COLUMN_NAMES] = ['is_raining']
        automl_settings[TimeSeries.TARGET_ROLLING_WINDOW_SIZE] = 4
        automl_settings[TimeSeries.MAX_HORIZON] = 2
        automl_settings[TimeSeries.TARGET_LAGS] = None
        automl = self._create_native_client(automl_settings)
        X_train, y_train, X_valid, y_valid, X_test, y_test = self.get_mock_grain_data(automl_settings)
        local_run = automl.fit(X=X_train, y=y_train,
                               X_valid=X_valid, y_valid=y_valid,
                               compute_target='local', show_output=False)
        scores, fitted_model = local_run.get_output()
        preds = fitted_model.forecast(X_valid)
        result = fitted_model.steps[0][1].transform(X_valid).sort_index()
        y = np.zeros(result.shape[0])
        result, y = fitted_model.steps[0][1]._remove_nans_from_look_back_features(result, y)
        assert len(preds[0]) == X_valid.shape[0], "The array has wrong size."
        assert all([p is not None for p in preds[0]]), "Some predictions are NaN"
        exp_grains = list(np.repeat('grain1', 3)) + list(np.repeat('grain2', 3))
        window_dict = {'date': ['2011-01-09', '2011-01-09', '2011-01-10'] * 2,
                       automl_settings[TimeSeries.GRAIN_COLUMN_NAMES]: exp_grains,
                       'origin': ["2011-01-07", "2011-01-08", "2011-01-08"] * 2,
                       'temperature_WASNULL': np.repeat(0, 6),
                       tsind_map[TimeSeriesInternal.TIME_INDEX_FEATURE_ID_DAY]: [9, 9, 10] * 2,
                       tsind_map[TimeSeriesInternal.TIME_INDEX_FEATURE_ID_WDAY]: [6, 6, 0] * 2,
                       tsind_map[TimeSeriesInternal.TIME_INDEX_FEATURE_ID_YEAR_ISO]: [2011] * 6,
                       'temperature': [30, 30, 20] * 2,
                       TimeSeriesInternal.DUMMY_TARGET_COLUMN + '_mean_window4D': [7.75, 7.75, 7.75] * 2,
                       TimeSeriesInternal.DUMMY_TARGET_COLUMN + '_min_window4D': [3., 3., 3.] * 2,
                       TimeSeriesInternal.DUMMY_TARGET_COLUMN + '_max_window4D': [14., 14., 14.] * 2,
                       TimeSeriesInternal.DUMMY_TARGET_COLUMN + "_WASNULL": 0,
                       'grain_mygrain': [0, 0, 0, 1, 1, 1],
                       TimeSeriesInternal.HORIZON_NAME: [2, 1, 2] * 2
                       }
        df_expected = pd.DataFrame(window_dict)
        df_expected['date'] = pd.to_datetime(df_expected['date'])
        df_expected['origin'] = pd.to_datetime(df_expected['origin'])
        df_expected.set_index(['date', automl_settings[TimeSeries.GRAIN_COLUMN_NAMES], 'origin'], inplace=True)
        df_expected.sort_index(inplace=True)
        assert_frame_equal(df_expected, result, check_like=True, check_dtype=False)

    def test_lags_with_rolling_window(self, automl_settings):
        """
        window_size=5, lags={TimeSeriesInternal.DUMMY_TARGET_COLUMN: 1}, max_horyzon = 1
        """
        automl_settings[TimeSeries.GRAIN_COLUMN_NAMES] = None
        automl_settings[TimeSeries.DROP_COLUMN_NAMES] = ['is_raining']
        automl = self._create_native_client(automl_settings)
        X_train, y_train, X_valid, y_valid, X_test, y_test = self.get_mock_data(
            automl_settings,
            TimeSeriesInternal.MAX_HORIZON_DEFAULT)
        local_run = automl.fit(X=X_train, y=y_train,
                               X_valid=X_valid, y_valid=y_valid,
                               compute_target='local', show_output=False)
        scores, fitted_model = local_run.get_output()
        preds = fitted_model.forecast(X_valid)
        assert len(preds[0]) == X_valid.shape[0], "The array has wrong size."
        assert all([p is not None for p in preds[0]]), "Some predictions are NaN"
        result = fitted_model.steps[0][1].transform(X_valid).sort_index()
        y = np.zeros(result.shape[0])
        result, y = fitted_model.steps[0][1]._remove_nans_from_look_back_features(result, y)
        window_dict = {'date': ['2011-01-09'],
                       TimeSeriesInternal.DUMMY_GRAIN_COLUMN: TimeSeriesInternal.DUMMY_GRAIN_COLUMN,
                       'origin': ["2011-01-08"],
                       'temperature_WASNULL': [0],
                       tsind_map[TimeSeriesInternal.TIME_INDEX_FEATURE_ID_DAY]: [9],
                       'temperature': [30],
                       tsind_map[TimeSeriesInternal.TIME_INDEX_FEATURE_ID_WDAY]: [6],
                       tsind_map[TimeSeriesInternal.TIME_INDEX_FEATURE_ID_YEAR_ISO]: [2011],
                       TimeSeriesInternal.DUMMY_TARGET_COLUMN + '_lag1D': [14.],
                       TimeSeriesInternal.DUMMY_TARGET_COLUMN + '_mean_window5D': [9.],
                       TimeSeriesInternal.DUMMY_TARGET_COLUMN + '_min_window5D': [3.],
                       TimeSeriesInternal.DUMMY_TARGET_COLUMN + '_max_window5D': [14.],
                       TimeSeriesInternal.DUMMY_TARGET_COLUMN + "_WASNULL": 0,
                       TimeSeriesInternal.HORIZON_NAME: [1]
                       }
        df_expected = pd.DataFrame(window_dict)
        df_expected['date'] = pd.to_datetime(df_expected['date'])
        df_expected['origin'] = pd.to_datetime(df_expected['origin'])
        df_expected.set_index(['date', TimeSeriesInternal.DUMMY_GRAIN_COLUMN, 'origin'], inplace=True)
        assert_frame_equal(df_expected, result, check_like=True, check_dtype=False)
        # Validate transformation on the train set.
        X_train[TimeSeriesInternal.DUMMY_TARGET_COLUMN] = y_train
        result = fitted_model.steps[0][1].transform(X_train).sort_index()
        y = result.pop(TimeSeriesInternal.DUMMY_TARGET_COLUMN).values
        result, y = fitted_model.steps[0][1]._remove_nans_from_look_back_features(result, y)
        result[TimeSeriesInternal.DUMMY_TARGET_COLUMN] = y
        window_dict = {'date': ['2011-01-06', '2011-01-07', '2011-01-08'],
                       TimeSeriesInternal.DUMMY_GRAIN_COLUMN: np.repeat(TimeSeriesInternal.DUMMY_GRAIN_COLUMN, 3),
                       'origin': ["2011-01-05", "2011-01-06", "2011-01-07"],
                       'temperature_WASNULL': [0, 0, 0],
                       tsind_map[TimeSeriesInternal.TIME_INDEX_FEATURE_ID_DAY]: [6, 7, 8],
                       'temperature': [20, 30, 40],
                       tsind_map[TimeSeriesInternal.TIME_INDEX_FEATURE_ID_WDAY]: [3, 4, 5],
                       tsind_map[TimeSeriesInternal.TIME_INDEX_FEATURE_ID_YEAR_ISO]: [2011] * 3,
                       TimeSeriesInternal.DUMMY_TARGET_COLUMN: [4, 3, 14],
                       TimeSeriesInternal.DUMMY_TARGET_COLUMN + '_lag1D': [10., 4., 3.],
                       TimeSeriesInternal.DUMMY_TARGET_COLUMN + '_mean_window5D': [10.20, 8., 8.40],
                       TimeSeriesInternal.DUMMY_TARGET_COLUMN + '_min_window5D': [1., 1., 3.],
                       TimeSeriesInternal.DUMMY_TARGET_COLUMN + '_max_window5D': [15., 14., 14.],
                       TimeSeriesInternal.DUMMY_TARGET_COLUMN + "_WASNULL": 0,
                       TimeSeriesInternal.HORIZON_NAME: [1, 1, 1]
                       }
        df_expected = pd.DataFrame(window_dict)
        df_expected['date'] = pd.to_datetime(df_expected['date'])
        df_expected['origin'] = pd.to_datetime(df_expected['origin'])
        df_expected.set_index(['date', TimeSeriesInternal.DUMMY_GRAIN_COLUMN, 'origin'], inplace=True)
        assert_frame_equal(df_expected, result, check_like=True, check_dtype=False)

    def test_lag_rolling_windows_on_grained_set(self, automl_settings):
        """Test the lag and rolling windows on data set with grains."""
        automl_settings[TimeSeries.GRAIN_COLUMN_NAMES] = 'mygrain'
        automl_settings[TimeSeries.DROP_COLUMN_NAMES] = ['is_raining']
        automl = self._create_native_client(automl_settings)
        X_train, y_train, X_valid, y_valid, X_test, y_test = self.get_mock_grain_data(automl_settings)
        local_run = automl.fit(X=X_train, y=y_train,
                               X_valid=X_valid, y_valid=y_valid,
                               compute_target='local', show_output=False)
        scores, fitted_model = local_run.get_output()
        preds = fitted_model.forecast(X_valid)
        result = fitted_model.steps[0][1].transform(X_valid).sort_index()
        y = np.zeros(result.shape[0])
        result, y = fitted_model.steps[0][1]._remove_nans_from_look_back_features(result, y)
        assert len(preds) == 2, "The array has wrong size."
        assert all([p is not None for p in preds[0]]), "Some predictions are NaN"
        exp_grains = ['grain1', 'grain2']
        window_dict = {'date': ['2011-01-09'] * 2,
                       automl_settings[TimeSeries.GRAIN_COLUMN_NAMES]: exp_grains,
                       'origin': ['2011-01-08'] * 2,
                       'temperature_WASNULL': np.repeat(0, 2),
                       tsind_map[TimeSeriesInternal.TIME_INDEX_FEATURE_ID_DAY]: [9, 9],
                       'temperature': [30, 30],
                       tsind_map[TimeSeriesInternal.TIME_INDEX_FEATURE_ID_WDAY]: [6, 6],
                       tsind_map[TimeSeriesInternal.TIME_INDEX_FEATURE_ID_YEAR_ISO]: [2011, 2011],
                       TimeSeriesInternal.DUMMY_TARGET_COLUMN + '_lag1D': [14., 14.],
                       TimeSeriesInternal.DUMMY_TARGET_COLUMN + '_mean_window5D': [9., 9.],
                       TimeSeriesInternal.DUMMY_TARGET_COLUMN + '_min_window5D': [3., 3.],
                       TimeSeriesInternal.DUMMY_TARGET_COLUMN + '_max_window5D': [14., 14.],
                       TimeSeriesInternal.DUMMY_TARGET_COLUMN + "_WASNULL": 0,
                       'grain_mygrain': [0, 1],
                       TimeSeriesInternal.HORIZON_NAME: [1, 1]
                       }
        df_expected = pd.DataFrame(window_dict)
        df_expected['date'] = pd.to_datetime(df_expected['date'])
        df_expected['origin'] = pd.to_datetime(df_expected['origin'])
        df_expected.set_index(['date', automl_settings[TimeSeries.GRAIN_COLUMN_NAMES], 'origin'], inplace=True)
        assert_frame_equal(df_expected, result, check_like=True, check_dtype=False)

    def test_non_defaults(self, automl_settings):
        """Test transform if neither of parameters is default"""
        automl_settings[TimeSeries.GRAIN_COLUMN_NAMES] = 'mygrain'
        automl_settings[TimeSeries.DROP_COLUMN_NAMES] = ['is_raining']
        automl_settings[TimeSeries.TARGET_ROLLING_WINDOW_SIZE] = 4
        automl_settings[TimeSeries.MAX_HORIZON] = 3
        automl_settings[TimeSeries.TARGET_LAGS] = 2
        automl = self._create_native_client(automl_settings)
        X_train, y_train, X_valid, y_valid, X_test, y_test = self.get_mock_grain_data(automl_settings)
        local_run = automl.fit(X=X_train, y=y_train,
                               X_valid=X_valid, y_valid=y_valid,
                               compute_target='local', show_output=False)
        scores, fitted_model = local_run.get_output()
        preds = fitted_model.forecast(X_valid)
        result = fitted_model.steps[0][1].transform(X_valid).sort_index()
        y = np.zeros(result.shape[0])
        result, y = fitted_model.steps[0][1]._remove_nans_from_look_back_features(result, y)
        assert len(preds[0]) == X_valid.shape[0], "The array has wrong size."
        assert all([p is not None for p in preds[0]]), "Some predictions are NaN"
        exp_grains = list(np.repeat(['grain1', 'grain2'], 3)) + \
            list(np.repeat(['grain1', 'grain2'], 2)) + ['grain1', 'grain2']
        window_dict = {'date': ['2011-01-09'] *
                       6 +
                       ['2011-01-10'] *
                       4 +
                       ['2011-01-11'] *
                       2,
                       automl_settings[TimeSeries.GRAIN_COLUMN_NAMES]: exp_grains,
                       'origin': ['2011-01-06', '2011-01-07', '2011-01-08'] *
                       2 +
                       ['2011-01-07', '2011-01-08'] *
                       2 +
                       ['2011-01-08'] *
                       2, 'temperature_WASNULL': np.repeat(0, 12),
                       tsind_map[TimeSeriesInternal.TIME_INDEX_FEATURE_ID_DAY]: [9] *
                       6 +
                       [10] *
                       4 +
                       [11] *
                       2, 'temperature': [30] *
                       6 +
                       [20] *
                       4 +
                       [10] *
                       2, tsind_map[TimeSeriesInternal.TIME_INDEX_FEATURE_ID_WDAY]: [6] * 6 + [0] * 4 + [1] * 2,
                       tsind_map[TimeSeriesInternal.TIME_INDEX_FEATURE_ID_YEAR_ISO]: [2011] * 12,
                       TimeSeriesInternal.DUMMY_TARGET_COLUMN +
                       '_lag2D': [10., 4., 3.] *
                       2 +
                       [4., 3.] *
                       2 +
                       [3.] *
                       2, TimeSeriesInternal.DUMMY_TARGET_COLUMN +
                       '_mean_window4D': [9.75, 7.75, 7.75] *
                       2 +
                       [7.75, 7.75] *
                       2 +
                       [7.75] *
                       2, TimeSeriesInternal.DUMMY_TARGET_COLUMN +
                       '_min_window4D': [4., 3., 3.] *
                       2 +
                       [3., 3.] *
                       2 +
                       [3.] *
                       2, TimeSeriesInternal.DUMMY_TARGET_COLUMN +
                       '_max_window4D': [14., 14., 14.] *
                       2 +
                       [14., 14.] *
                       2 +
                       [14.] *
                       2,
                       TimeSeriesInternal.DUMMY_TARGET_COLUMN + "_WASNULL": 0,
                       'grain_mygrain': [0] * 3 + [1] * 3 + [0, 0, 1, 1, 0, 1],
                       TimeSeriesInternal.HORIZON_NAME: [3, 2, 1] *
                       2 +
                       [3, 2] *
                       2 +
                       [3, 3]}
        df_expected = pd.DataFrame(window_dict)
        df_expected['date'] = pd.to_datetime(df_expected['date'])
        df_expected['origin'] = pd.to_datetime(df_expected['origin'])
        df_expected.set_index(['date', automl_settings[TimeSeries.GRAIN_COLUMN_NAMES], 'origin'], inplace=True)
        df_expected.sort_index(inplace=True)
        assert_frame_equal(df_expected, result, check_like=True, check_dtype=False)

    def test_lags_rolling_window_and_stl(self, automl_settings):
        """Test the lag and rolling windows on data set with grains featurization='off'."""
        self._do_test_lags_rolling_window_and_stl(automl_settings, 'off')

    def test_lags_rolling_window_and_stl_featurization(self, automl_settings):
        """Test the lag and rolling windows on data set with grains featurization='auto'."""
        self._do_test_lags_rolling_window_and_stl(automl_settings, 'auto')

    def _do_test_lags_rolling_window_and_stl(self, automl_settings, featurization):
        """Test the lag and rolling windows on data set with grains."""
        automl_settings[TimeSeries.GRAIN_COLUMN_NAMES] = 'mygrain'
        automl_settings[TimeSeries.DROP_COLUMN_NAMES] = ['is_raining']
        automl_settings[TimeSeries.USE_STL] = TimeSeries.STL_OPTION_SEASON_TREND
        automl_settings[TimeSeries.SEASONALITY] = 7
        automl_settings['featurization'] = featurization
        automl = self._create_native_client(automl_settings)
        X_train, y_train, X_valid, y_valid, X_test, y_test = self.get_mock_grain_data(automl_settings)
        local_run = automl.fit(X=X_train, y=y_train,
                               X_valid=X_valid, y_valid=y_valid,
                               compute_target='local', show_output=False)
        scores, fitted_model = local_run.get_output()
        preds = fitted_model.forecast(X_valid)
        result = fitted_model.steps[0][1].transform(X_valid).sort_index()
        y = np.zeros(result.shape[0])
        result, y = fitted_model.steps[0][1]._remove_nans_from_look_back_features(result, y)
        assert len(preds[0]) == X_valid.shape[0], "The array has wrong size."
        assert all([p is not None for p in preds[0]]), "Some predictions are NaN"
        assert fitted_model.steps[0][1].seasonality == 7, "Seasonality was not set to expected value"
        expected_list = sorted(['date',
                                automl_settings[TimeSeries.GRAIN_COLUMN_NAMES],
                                'origin', 'temperature_WASNULL',
                                tsind_map[TimeSeriesInternal.TIME_INDEX_FEATURE_ID_DAY], 'temperature',
                                tsind_map[TimeSeriesInternal.TIME_INDEX_FEATURE_ID_WDAY],
                                tsind_map[TimeSeriesInternal.TIME_INDEX_FEATURE_ID_YEAR_ISO],
                                TimeSeriesInternal.DUMMY_TARGET_COLUMN + '_lag1D',
                                TimeSeriesInternal.DUMMY_TARGET_COLUMN + '_mean_window5D',
                                TimeSeriesInternal.DUMMY_TARGET_COLUMN + '_min_window5D',
                                TimeSeriesInternal.DUMMY_TARGET_COLUMN + '_max_window5D',
                                TimeSeriesInternal.DUMMY_TARGET_COLUMN + '_WASNULL',
                                'grain_{}'.format(automl_settings[TimeSeries.GRAIN_COLUMN_NAMES]),
                                TimeSeriesInternal.HORIZON_NAME,
                                TimeSeriesInternal.DUMMY_TARGET_COLUMN + TimeSeriesInternal.STL_SEASON_SUFFIX,
                                TimeSeriesInternal.DUMMY_TARGET_COLUMN + TimeSeriesInternal.STL_TREND_SUFFIX
                                ])
        result.reset_index(inplace=True, drop=False)
        assert(set(expected_list) == set(result.columns))

    def test_diabetes_data(self, automl_settings):
        """Test standard transformer on diabetes data."""
        x, y = load_diabetes(return_X_y=True)
        diffed_col = np.diff(y)
        # Padding values after processing diff with 0.
        y = np.insert(diffed_col, 0, 0)
        X_train, X_valid, y_train, y_valid = train_test_split(x,
                                                              y,
                                                              test_size=0.2,
                                                              random_state=0)
        date_column_name = "date"
        nrows_train, ncols_train = X_train.shape
        nrows_test, ncols_test = X_valid.shape
        column_names = [str(i) for i in range(ncols_train)]
        X_train = pd.DataFrame(X_train, columns=column_names)
        X_valid = pd.DataFrame(X_valid, columns=column_names)
        time_axis = pd.date_range('1980-01-01', periods=(nrows_train + nrows_test), freq='D')
        X_train[date_column_name] = time_axis[:nrows_train]
        X_valid[date_column_name] = time_axis[nrows_train:]

        automl = self._create_native_client(automl_settings)
        local_run = automl.fit(X=X_train, y=y_train,
                               X_valid=X_valid, y_valid=y_valid,
                               compute_target='local', show_output=False)
        scores, fitted_model = local_run.get_output()
        preds = fitted_model.forecast(X_valid)
        assert len(preds[0]) == X_valid.shape[0], "Wrong number of predictions."
        ##
        X_valid_before = X_valid.copy()
        ##
        result = fitted_model.steps[0][1].transform(X_valid).sort_index()
        y = np.zeros(result.shape[0])
        result, y = fitted_model.steps[0][1]._remove_nans_from_look_back_features(result, y)
        diabetes_out = {date_column_name: '1980-12-19',
                        TimeSeriesInternal.DUMMY_GRAIN_COLUMN: TimeSeriesInternal.DUMMY_GRAIN_COLUMN,
                        'origin': '1980-12-18',
                        '0': X_valid_before.iloc[0]['0'],
                        '1': X_valid_before.iloc[0]['1'],
                        '2': X_valid_before.iloc[0]['2'],
                        '3': X_valid_before.iloc[0]['3'],
                        '4': X_valid_before.iloc[0]['4'],
                        '5': X_valid_before.iloc[0]['5'],
                        '6': X_valid_before.iloc[0]['6'],
                        '7': X_valid_before.iloc[0]['7'],
                        '8': X_valid_before.iloc[0]['8'],
                        '9': X_valid_before.iloc[0]['9'],
                        '8_WASNULL': 0,
                        '9_WASNULL': 0,
                        '0_WASNULL': 0,
                        '1_WASNULL': 0,
                        '2_WASNULL': 0,
                        '3_WASNULL': 0,
                        '4_WASNULL': 0,
                        '5_WASNULL': 0,
                        '6_WASNULL': 0,
                        '7_WASNULL': 0,
                        '8_WASNULL': 0,
                        '9_WASNULL': 0,
                        tsind_map[TimeSeriesInternal.TIME_INDEX_FEATURE_ID_MONTH]: 12,
                        tsind_map[TimeSeriesInternal.TIME_INDEX_FEATURE_ID_DAY]: 19,
                        tsind_map[TimeSeriesInternal.TIME_INDEX_FEATURE_ID_QDAY]: 80,
                        tsind_map[TimeSeriesInternal.TIME_INDEX_FEATURE_ID_QUARTER]: 4,
                        tsind_map[TimeSeriesInternal.TIME_INDEX_FEATURE_ID_HALF]: 2,
                        tsind_map[TimeSeriesInternal.TIME_INDEX_FEATURE_ID_WDAY]: 4,
                        TimeSeriesInternal.DUMMY_TARGET_COLUMN + '_lag1D': [221.],
                        TimeSeriesInternal.DUMMY_TARGET_COLUMN + '_mean_window5D': [19.60],
                        TimeSeriesInternal.DUMMY_TARGET_COLUMN + '_min_window5D': [-87.],
                        TimeSeriesInternal.DUMMY_TARGET_COLUMN + '_max_window5D': [221.],
                        TimeSeriesInternal.DUMMY_TARGET_COLUMN + '_WASNULL': 0,
                        TimeSeriesInternal.HORIZON_NAME: [1]
                        }
        df_expected = pd.DataFrame(diabetes_out)
        df_expected[date_column_name] = pd.to_datetime(df_expected[date_column_name])
        df_expected['origin'] = pd.to_datetime(df_expected['origin'])
        df_expected.set_index([date_column_name, TimeSeriesInternal.DUMMY_GRAIN_COLUMN, 'origin'], inplace=True)
        assert_frame_equal(df_expected, result, check_like=True, check_dtype=False)

    def test_column_order_after_transform(self, automl_settings):
        """Test if columns have the same order in train and test."""

        automl_settings[TimeSeries.TARGET_ROLLING_WINDOW_SIZE] = None
        automl_settings[TimeSeries.TARGET_LAGS] = None
        self._do_test_column_order(automl_settings)

    def test_column_order_after_transform_lag_lead(self, automl_settings):
        """Test if columns have the same order in train and test if LagLeadOperator was applied."""

        automl_settings[TimeSeries.TARGET_ROLLING_WINDOW_SIZE] = None
        automl_settings[TimeSeries.TARGET_LAGS] = 1
        self._do_test_column_order(automl_settings)

    def test_column_order_after_transform_rw(self, automl_settings):
        """Test if columns have the same order in train and test if RollingWindow was applied."""

        automl_settings[TimeSeries.TARGET_ROLLING_WINDOW_SIZE] = 5
        automl_settings[TimeSeries.TARGET_LAGS] = None
        self._do_test_column_order(automl_settings)

    def test_column_order_after_transform_lags_rw(self, automl_settings):
        """Test if columns have the same order in train and test if RollingWindow and LagLeadOperator were applied."""

        automl_settings[TimeSeries.TARGET_ROLLING_WINDOW_SIZE] = 5
        automl_settings[TimeSeries.TARGET_LAGS] = 1
        self._do_test_column_order(automl_settings)

    def test_native_client_forecast_function(self, automl_settings):
        """Test forecast function obtained from the native client."""
        automl_settings[TimeSeries.GRAIN_COLUMN_NAMES] = 'mygrains'
        automl_settings[TimeSeries.DROP_COLUMN_NAMES] = ['is_raining']
        automl_settings[TimeSeries.TARGET_LAGS] = 1
        automl_settings[TimeSeries.TARGET_ROLLING_WINDOW_SIZE] = 5
        automl_settings['n_cross_validations'] = 2
        automl_settings[TimeSeries.MAX_HORIZON] = 5
        automl = self._create_native_client(automl_settings)
        X_train, y_train, X_test, y_test = self.get_simple_grain_data(automl_settings, 5)
        local_run = automl.fit(X=X_train, y=y_train,
                               compute_target='local', show_output=False)
        scores, fitted_model = local_run.get_output()
        y_query = np.repeat(np.NaN, X_test.shape[0])
        y_pred, xy_pred = fitted_model.forecast(X_test, y_query)
        assert(xy_pred.shape[0] == X_test.shape[0])
        # Test the confidence intervals.
        ci_df = fitted_model.forecast_quantiles(X_test, y_query)
        ci_df2 = fitted_model.forecast_quantiles(X_test, None)
        assert_frame_equal(ci_df, ci_df2)
        assert(ci_df.shape[0] == X_test.shape[0])
        assert(not ci_df.isnull().values.any())
        # Test ci-s only wit5h nan-s at the end.
        X_test['tst'] = y_test
        dfs = []
        for grain, df in X_test.groupby(automl_settings[TimeSeries.GRAIN_COLUMN_NAMES]):
            y = df['tst']
            y[3:] = np.NaN
            df['tst'] = y
            dfs.append(df)
        X_test = pd.concat(dfs)
        y_query = X_test.pop('tst').values
        y_pred, xy_pred = fitted_model.forecast(X_test, y_query)
        assert(xy_pred.shape[0] == X_test.shape[0])
        ci_df = fitted_model.forecast_quantiles(X_test, y_query, ignore_data_errors=False)
        assert(ci_df.shape[0] == X_test.shape[0])
        assert(not ci_df.isnull().values.any())
        # Test ci-s when all the values are on place.
        y_pred, xy_pred = fitted_model.forecast(X_test, y_test, ignore_data_errors=True)
        assert(xy_pred.shape[0] == X_test.shape[0])
        ci_df = fitted_model.forecast_quantiles(X_test, y_test, ignore_data_errors=True)
        assert(ci_df.shape[0] == X_test.shape[0])
        assert(not ci_df.isnull().values.any())

    def test_forecast_multiple_lags(self, automl_settings):
        """Test setting of multiple lags."""
        automl_settings[TimeSeries.GRAIN_COLUMN_NAMES] = 'mygrains'
        automl_settings[TimeSeries.DROP_COLUMN_NAMES] = ['is_raining']
        automl_settings[TimeSeries.TARGET_LAGS] = [1, 2, 5]
        automl_settings[TimeSeries.TARGET_ROLLING_WINDOW_SIZE] = 5
        automl_settings['n_cross_validations'] = 2
        automl_settings[TimeSeries.MAX_HORIZON] = 5
        automl = self._create_native_client(automl_settings)
        X_train, y_train, X_test, y_test = self.get_simple_grain_data(automl_settings, 5)
        local_run = automl.fit(X=X_train, y=y_train,
                               compute_target='local', show_output=False)
        scores, fitted_model = local_run.get_output()
        y_query = np.repeat(np.NaN, X_test.shape[0])
        y_pred, xy_pred = fitted_model.forecast(X_test, y_query)
        assert(xy_pred.shape[0] == X_test.shape[0])
        set_lags = set()
        set_lags.add("{}_lag{}D".format(TimeSeriesInternal.DUMMY_TARGET_COLUMN, 1))
        set_lags.add("{}_lag{}D".format(TimeSeriesInternal.DUMMY_TARGET_COLUMN, 2))
        set_lags.add("{}_lag{}D".format(TimeSeriesInternal.DUMMY_TARGET_COLUMN, 5))
        assert(set_lags.issubset(set(xy_pred.columns.values)))
        # Test the confidence intervals.
        ci_df = fitted_model.forecast_quantiles(X_test, y_query)
        assert(ci_df.shape[0] == X_test.shape[0])
        assert(not ci_df.isnull().values.any())

    def test_data_type_was_not_lost(self, automl_settings):
        """Test if the data type is not lost during fitting."""
        dates_train = list(pd.date_range(start='1991-01-01', freq='D', periods=40))
        sales = np.arange(40)
        sales_flt = sales.astype(float)
        type = 20 * ['A', 'B']
        is_raining = np.array(20 * [True, False])
        automl_settings[TimeSeries.GRAIN_COLUMN_NAMES] = None
        automl_settings[TimeSeries.TARGET_ROLLING_WINDOW_SIZE] = None
        automl_settings[TimeSeries.TARGET_LAGS] = None
        automl_settings['n_cross_validations'] = 2
        dict_train = {'date': dates_train,
                      'sales': sales,
                      'sales_flt': sales_flt,
                      'type': type,
                      'is_raining': is_raining
                      }
        automl = self._create_native_client(automl_settings)
        df_train = pd.DataFrame(data=dict_train)
        # Emulate what happens in the fit()
        df_train = pd.DataFrame(df_train.values, columns=df_train.columns.values)
        df_train = df_train.infer_objects()
        #
        X_train = df_train[0:30]
        # create a gap to initiate the inference.
        X_train.drop(12, inplace=True, axis=0)
        y_train = np.arange(0, X_train.shape[0])
        X_test = df_train[30:]
        local_run = automl.fit(X=X_train, y=y_train,
                               compute_target='local', show_output=False)
        scores, fitted_model = local_run.get_output()
        _, x_after = fitted_model.forecast(X_test, np.repeat(np.NaN, X_test.shape[0]))
        # Make sure that sales were not assumed to be categorical and were not OneHot encoded
        assert_array_equal(sales[30:], x_after['sales'].values, 'The array was corrupted.')
        assert(np.float == x_after['sales'].values.dtype)
        assert_array_equal(sales_flt[30:], x_after['sales_flt'].values, 'The array was corrupted.')
        assert(X_test['sales_flt'].dtype == x_after['sales_flt'].values.dtype)
        # We are converting boolean columns to int on in transform() method.
        assert_array_equal(is_raining[30:].astype(int), x_after['is_raining'].values, 'The array was corrupted.')
        assert('type' in x_after.columns)

    def test_drop_short_series(self, automl_settings):
        """Test if the data type is not lost during fitting."""
        LENGTH = 80
        dates_train = list(pd.date_range(start='1991-01-01', freq='D', periods=LENGTH))
        sales = np.arange(LENGTH)
        sales_flt = sales.astype(float)
        type = (LENGTH // 2) * ['A', 'B']
        is_raining = np.array((LENGTH // 2) * [True, False])
        automl_settings[TimeSeries.GRAIN_COLUMN_NAMES] = ['type']
        automl_settings[TimeSeries.TARGET_ROLLING_WINDOW_SIZE] = None
        automl_settings[TimeSeries.TARGET_LAGS] = None
        automl_settings['n_cross_validations'] = 5
        automl_settings[TimeSeries.MAX_HORIZON] = 10
        automl_settings[TimeSeries.SHORT_SERIES_HANDLING] = True
        automl_settings[TimeSeries.SHORT_SERIES_HANDLING_CONFIG] = ShortSeriesHandlingValues.SHORT_SERIES_HANDLING_DROP
        dict_train = {'date': dates_train,
                      'sales': sales,
                      'sales_flt': sales_flt,
                      'type': type,
                      'is_raining': is_raining
                      }
        automl = self._create_native_client(automl_settings)
        df_train = pd.DataFrame(data=dict_train)
        # Emulate what happens in the fit()
        df_train = pd.DataFrame(df_train.values, columns=df_train.columns.values)
        #
        spl = 30
        dfs_train = []
        dfs_test = []
        for grain, df in df_train.groupby(automl_settings[TimeSeries.GRAIN_COLUMN_NAMES]):
            df_train = df[:spl]
            df_train['y'] = np.arange(0, df_train.shape[0])
            # We want to trim the grain A to check how it will be handled by AutoML.
            if grain == 'A':
                df_train = df_train[:12]
            df_test = df[spl:]
            dfs_train.append(df_train)
            dfs_test.append(df_test)
        X_train = pd.concat(dfs_train)
        y_train = X_train.pop('y').values
        X_test = pd.concat(dfs_test)
        local_run = automl.fit(X=X_train, y=y_train,
                               compute_target='local', show_output=False)
        scores, fitted_model = local_run.get_output()
        y_pred, x_after = fitted_model.forecast(X_test, np.repeat(np.NaN, X_test.shape[0]))
        # Assert that the predictions are generated only for grain B.
        assert_array_equal(y_pred, x_after[TimeSeriesInternal.DUMMY_TARGET_COLUMN].values, "Incorrect values")
        # We have to check if grain A lacks the predictions, while the rest is on the place.
        X_test[TimeSeriesInternal.DUMMY_TARGET_COLUMN] = y_pred
        for grain, df in X_test.groupby(automl_settings[TimeSeries.GRAIN_COLUMN_NAMES]):
            if grain == 'A':
                assert(all(pd.isnull(y) for y in df[TimeSeriesInternal.DUMMY_TARGET_COLUMN]))
            else:
                assert(all(not pd.isnull(y) for y in df[TimeSeriesInternal.DUMMY_TARGET_COLUMN]))

    def test_y_df_as_input(self, automl_settings):
        """Test forecast if y is a dataframe."""
        automl_settings[TimeSeries.GRAIN_COLUMN_NAMES] = 'type'
        automl_settings[TimeSeries.TARGET_ROLLING_WINDOW_SIZE] = None
        automl_settings[TimeSeries.TARGET_LAGS] = None
        automl_settings['n_cross_validations'] = 2
        automl_settings[TimeSeries.MAX_HORIZON] = 10
        automl_settings[TimeSeries.SHORT_SERIES_HANDLING] = True
        automl_settings[TimeSeries.SHORT_SERIES_HANDLING_CONFIG] = ShortSeriesHandlingValues.SHORT_SERIES_HANDLING_DROP
        X_train, y_train, X_test, _ = self.get_simple_grain_data(automl_settings,
                                                                 ntest=10)
        automl = self._create_native_client(automl_settings)
        y_train = pd.DataFrame({'y': y_train})
        local_run = automl.fit(X=X_train, y=y_train,
                               compute_target='local', show_output=False)
        _, fitted_model = local_run.get_output()
        y_pred, _ = fitted_model.forecast(X_test, np.repeat(np.NaN, X_test.shape[0]))
        # Assert that the predictions were generated.
        assert(all(not pd.isnull(y) for y in y_pred))

    def test_y_df_as_input_valid(self, automl_settings):
        """Test forecast if y and y_valid are dataframes."""
        HORIZON = 5
        automl_settings[TimeSeries.GRAIN_COLUMN_NAMES] = None
        automl_settings[TimeSeries.TARGET_ROLLING_WINDOW_SIZE] = None
        automl_settings[TimeSeries.TARGET_LAGS] = None
        automl_settings[TimeSeries.MAX_HORIZON] = HORIZON
        automl_settings[TimeSeries.SHORT_SERIES_HANDLING] = True
        automl_settings[TimeSeries.SHORT_SERIES_HANDLING_CONFIG] = ShortSeriesHandlingValues.SHORT_SERIES_HANDLING_DROP
        X_train, y_train, X_valid, y_valid, X_test, _ = self.get_mock_data(automl_settings,
                                                                           HORIZON,
                                                                           HORIZON,
                                                                           HORIZON)
        automl = self._create_native_client(automl_settings)
        y_train = pd.DataFrame({'y': y_train})
        y_valid = pd.DataFrame({'y': y_valid})
        local_run = automl.fit(X=X_train, y=y_train,
                               X_valid=X_valid, y_valid=y_valid,
                               compute_target='local', show_output=False)
        _, fitted_model = local_run.get_output()
        y_pred, _ = fitted_model.forecast(X_test, np.repeat(np.NaN, X_test.shape[0]))
        # Assert that the predictions were generated.
        assert(all(not pd.isnull(y) for y in y_pred))

    def test_y_series_as_input_valid(self, automl_settings):
        """Test forecast if y and y_valid are dataframes."""
        HORIZON = 5
        automl_settings[TimeSeries.GRAIN_COLUMN_NAMES] = None
        automl_settings[TimeSeries.TARGET_ROLLING_WINDOW_SIZE] = None
        automl_settings[TimeSeries.TARGET_LAGS] = None
        automl_settings[TimeSeries.MAX_HORIZON] = HORIZON
        automl_settings[TimeSeries.SHORT_SERIES_HANDLING] = True
        automl_settings[TimeSeries.SHORT_SERIES_HANDLING_CONFIG] = ShortSeriesHandlingValues.SHORT_SERIES_HANDLING_DROP
        X_train, y_train, X_valid, y_valid, X_test, _ = self.get_mock_data(automl_settings,
                                                                           HORIZON,
                                                                           HORIZON,
                                                                           HORIZON)
        automl = self._create_native_client(automl_settings)
        y_train = pd.Series(data=y_train)
        y_valid = pd.Series(data=y_valid)
        local_run = automl.fit(X=X_train, y=y_train,
                               X_valid=X_valid, y_valid=y_valid,
                               compute_target='local', show_output=False)
        _, fitted_model = local_run.get_output()
        y_pred, _ = fitted_model.forecast(X_test, np.repeat(np.NaN, X_test.shape[0]))
        # Assert that the predictions were generated.
        assert(all(not pd.isnull(y) for y in y_pred))

    def test_auto_mode(self, automl_settings):
        """Test auto mode with cv"""
        self._do_test_auto_mode(automl_settings, True)

    def test_auto_mode_nocv(self, automl_settings):
        """Test auto mode without cv"""
        self._do_test_auto_mode(automl_settings, False)

    def _do_test_auto_mode(self, automl_settings, use_cv):
        """Test the heuristic lags, rolling windows and max_horizon."""
        automl_settings[TimeSeries.GRAIN_COLUMN_NAMES] = None
        automl_settings[TimeSeries.TARGET_ROLLING_WINDOW_SIZE] = TimeSeries.AUTO
        automl_settings[TimeSeries.TARGET_LAGS] = TimeSeries.AUTO
        automl_settings[TimeSeries.MAX_HORIZON] = TimeSeries.AUTO
        automl_settings[TimeSeries.SHORT_SERIES_HANDLING] = True
        automl_settings[TimeSeries.SHORT_SERIES_HANDLING_CONFIG] = ShortSeriesHandlingValues.SHORT_SERIES_HANDLING_DROP
        automl_settings[TimeSeries.USE_STL] = TimeSeries.STL_OPTION_SEASON_TREND
        if use_cv:
            automl_settings['n_cross_validations'] = 2
        # Note. It is difficult to accurately model the PACF behavior.
        # please use lag of 1 and rw of 5 to get the expected lag 1 and rw 2.
        # Begin with a series that has a period of 7 days for 52 weeks, so about a quarter
        target_colname = 'y'
        N = 3 * 7 * 52
        sinedata = pd.DataFrame(
            {automl_settings[TimeSeries.TIME_COLUMN_NAME]: pd.date_range('2019-01-01', periods=N, freq='D')})
        # make a sine wave
        sinedata[target_colname] = ((sinedata[automl_settings[TimeSeries.TIME_COLUMN_NAME]
                                              ].dt.dayofweek - 2) * 2 * math.pi / 7).apply(math.sin)
        # We have to set correct seed because the generated data are stochastic and are not guaranteed
        # to have the predicted lags/rolling windows.
        np.random.seed(50)
        sinedata[target_colname] = sinedata[target_colname] + np.random.randn(N) * 0.15
        l1 = sinedata[target_colname].shift(1)  # lag
        l2 = sinedata[target_colname].shift(2)  # rw
        if l1 is not None and l2 is None:
            sinedata[target_colname] = l1
        elif l1 is not None and l2 is not None:
            sinedata[target_colname] = sinedata[target_colname] * 0.1 + 0.6 * l1 + 0.3 * l2
        sinedata.dropna(inplace=True)
        X_train = sinedata[:-10].copy()
        y_train = X_train.pop(target_colname).values
        X_test = sinedata[-10:].copy()
        y_test = X_test.pop(target_colname).values
        automl = self._create_native_client(automl_settings)
        if use_cv:
            local_run = automl.fit(X=X_train, y=y_train,
                                   compute_target='local', show_output=False)
        else:
            local_run = automl.fit(X=X_train, y=y_train,
                                   X_valid=X_test,
                                   y_valid=y_test,
                                   compute_target='local', show_output=False)
        _, fitted_model = local_run.get_output()
        # Check that horizon was set correctly.
        assert(fitted_model._ts_transformer.max_horizon == 7)
        assert(fitted_model.max_horizon == 7)
        assert(fitted_model.target_lags == [1])
        assert(fitted_model.target_rolling_window_size == 2)
        y_pred, x_form = fitted_model.forecast(X_test[:5], np.repeat(np.NaN, 5))
        # Assert that the predictions were generated.
        assert(all(not pd.isnull(y) for y in y_pred))

        expected_columns = [
            "{}_lag{}D".format(TimeSeriesInternal.DUMMY_TARGET_COLUMN, 1),
            "{}_mean_window{}D".format(TimeSeriesInternal.DUMMY_TARGET_COLUMN, 2),
            "{}_min_window{}D".format(TimeSeriesInternal.DUMMY_TARGET_COLUMN, 2),
            "{}_max_window{}D".format(TimeSeriesInternal.DUMMY_TARGET_COLUMN, 2)
        ]
        assert(all(col in x_form.columns for col in expected_columns))
        fitted_model.forecast(X_test, np.repeat(np.NaN, len(X_test)))

    def _do_test_column_order(self, settings):
        """Test if the column order is the same in train and test set."""
        target_column_name = 'tgt'
        data_length = 20
        n_test_periods = 3
        data = pd.DataFrame({
            'date': pd.date_range(start='2000-01-01', periods=data_length, freq='YS'),
            target_column_name: [15, 1, 11, 14, 10, 4, 3, 14, 4, 2, 13, 19, 1, 10, 15, 12, 13, 5, 3, 3],
            'grain': ['g'] * data_length
        })
        expected_lags_column = '_automl_target_col_lag1AS-JAN'
        expected_rw_columns = {'_automl_target_col_min_window5AS-JAN',
                               '_automl_target_col_max_window5AS-JAN',
                               '_automl_target_col_mean_window5AS-JAN'}
        settings['n_cross_validations'] = 2
        settings['enable_voting_ensemble'] = False
        settings[TimeSeries.GRAIN_COLUMN_NAMES] = ['grain']
        settings[TimeSeries.MAX_HORIZON] = n_test_periods
        automl = self._create_native_client(settings)
        X_train, X_test = self.split_last_n_by_grain(data, n_test_periods, settings)
        y_train = X_train.pop(target_column_name).values
        local_run = automl.fit(X=X_train, y=y_train,
                               compute_target='local', show_output=False)
        _, fitted_model = local_run.get_output()
        raw_input_df = X_train.assign(**{'_automl_target_col': y_train})
        ts_transformed_df = fitted_model.steps[0][1].transform(raw_input_df)
        # The ground truth column order from transformed training data set.
        # They are used to train model.
        column_values_in_train_y = ts_transformed_df.columns.values
        # Just check if the transformers did work as expected.
        if settings[TimeSeries.TARGET_LAGS] is None:
            assert expected_lags_column not in column_values_in_train_y, "Unexpected lag."
        else:
            assert expected_lags_column in column_values_in_train_y, "Lag was not created."
        if settings[TimeSeries.TARGET_ROLLING_WINDOW_SIZE] is None:
            assert not bool(expected_rw_columns.intersection(set(column_values_in_train_y))), \
                "Unexpected rolling window."
        else:
            assert expected_rw_columns.issubset(set(column_values_in_train_y)), "Rolling window were not created."
        # The ground truth column, but without target column.
        ts_transformed_df.drop(labels=['_automl_target_col'], axis=1, inplace=True)
        column_values_in_train = ts_transformed_df.columns.values
        # Test if transformation of X_test gives the data frame with the
        # same column order as in ground truth.
        ts_transformed_df = fitted_model.steps[0][1].transform(X_test)
        column_values_in_test = ts_transformed_df.columns.values
        assert_array_equal(column_values_in_train, column_values_in_test)
        # If we transform data frame in presence of target values, we will get the
        # data frame with the dummy target column. Check if it has the same column
        # order as the transformed training set.
        y_test = X_test.pop(target_column_name).values
        ts_transformed_df = fitted_model.steps[0][1].transform(X_test, y_test)
        column_values_in_test_y = ts_transformed_df.columns.values
        assert_array_equal(column_values_in_train_y, column_values_in_test_y)

    def test_complex_frequency(self, automl_settings):
        """Test forecast if y and y_valid are dataframes."""
        HORIZON = 5
        automl_settings[TimeSeries.GRAIN_COLUMN_NAMES] = None
        automl_settings[TimeSeries.TARGET_ROLLING_WINDOW_SIZE] = 5
        automl_settings[TimeSeries.TARGET_LAGS] = 1
        automl_settings[TimeSeries.MAX_HORIZON] = HORIZON
        automl_settings['n_cross_validations'] = 2
        df = pd.DataFrame({automl_settings[TimeSeries.TIME_COLUMN_NAME]: pd.date_range(
            '2019-01-15', freq=DateOffset(months=3), periods=42),
            'someval': 42,
            'y': self.get_stationary_data(42)
        })
        X_train = df[:-HORIZON].copy()
        y_train = X_train.pop('y').values
        X_test = df[-HORIZON:].copy()
        X_test.drop('y', axis=1, inplace=True)
        del df
        automl = self._create_native_client(automl_settings)
        local_run = automl.fit(X=X_train, y=y_train,
                               compute_target='local', show_output=False)
        _, fitted_model = local_run.get_output()
        y_pred, _ = fitted_model.forecast(X_test, np.repeat(np.NaN, X_test.shape[0]))
        # Assert that the predictions were generated.
        assert(all(not pd.isnull(y) for y in y_pred))

    def test_high_freq_at_tail(self, automl_settings):
        """Test situation when at the end of train we have high freq data."""
        TGT = 'y'
        HORIZON = 2
        automl_settings[TimeSeries.MAX_HORIZON] = HORIZON
        automl_settings['n_cross_validations'] = 2
        automl_settings[TimeSeries.TARGET_LAGS] = None
        automl_settings[TimeSeries.TARGET_ROLLING_WINDOW_SIZE] = None
        automl_settings[TimeSeries.CV_STEP_SIZE] = 1
        length_df = 20
        df = pd.DataFrame({
            automl_settings[TimeSeries.TIME_COLUMN_NAME]: pd.date_range('2001-01-01', periods=length_df, freq='H'),
            'someval': 'val',
            TGT: np.arange(length_df)
        })
        # Make sure on cross validation we will get two data frames: with Hour frequency and with
        # minute frequency.
        length_df2 = 4
        expected_freq = to_offset('T')
        start = df[automl_settings[TimeSeries.TIME_COLUMN_NAME]].max() + expected_freq
        df2 = pd.DataFrame({
            automl_settings[TimeSeries.TIME_COLUMN_NAME]: pd.date_range(start, periods=length_df2, freq=expected_freq),
            'someval': 'val',
            TGT: np.arange(length_df2)
        })
        X_train = pd.concat([df, df2])
        X_train.drop(TGT, axis=1, inplace=True)
        y_train = self.get_stationary_data(length_df + length_df2)
        # The actual frequency should be minute, nit an hour. We should go to smaller granularity.
        start = X_train[automl_settings[TimeSeries.TIME_COLUMN_NAME]].max() + expected_freq
        X_test = pd.DataFrame({
            automl_settings[TimeSeries.TIME_COLUMN_NAME]: pd.date_range(start, periods=HORIZON, freq=expected_freq),
            'someval': 'val',
        })
        automl = self._create_native_client(automl_settings)
        local_run = automl.fit(X=X_train, y=y_train,
                               compute_target='local', show_output=False)
        _, fitted_model = local_run.get_output()
        y_pred, transformed_pred = fitted_model.forecast(X_test)
        assert(all(not pd.isnull(y) for y in y_pred))
        assert(y_pred.shape[0] == transformed_pred.shape[0])
        assert(y_pred.shape[0] == X_test.shape[0])
        assert(fitted_model._ts_transformer.freq_offset == expected_freq)
        assert(fitted_model._ts_transformer.freq == expected_freq.freqstr)

    def test_irregular_frame(self, automl_settings):
        """Test forecasting on the data frame with the wrong frequency."""
        HORIZON = 5
        TGT = 'y'
        automl_settings[TimeSeries.GRAIN_COLUMN_NAMES] = None
        automl_settings[TimeSeries.MAX_HORIZON] = HORIZON
        automl_settings['n_cross_validations'] = 2
        df = pd.DataFrame({
            automl_settings[TimeSeries.TIME_COLUMN_NAME]: pd.date_range('2001-01-01', periods=100, freq='D'),
            'someval': 'val',
            TGT: np.arange(100)
        })
        new_start = df[automl_settings[TimeSeries.TIME_COLUMN_NAME]].max() + to_offset('D')
        bad_freq = to_offset('23T')
        df2 = pd.DataFrame({
            automl_settings[TimeSeries.TIME_COLUMN_NAME]: pd.date_range(new_start, periods=4, freq=bad_freq),
            'someval': 'val',
            TGT: np.arange(4)
        })
        df = pd.concat([df2, df])
        df.sort_values(by=automl_settings[TimeSeries.TIME_COLUMN_NAME], axis=0, ascending=True, inplace=True)
        X_train = df[:-5].copy()
        X_test = df[-5:].copy()
        expcted_non_null = len(X_test)
        del df
        new_start = X_test[automl_settings[TimeSeries.TIME_COLUMN_NAME]].min() + bad_freq
        df2 = pd.DataFrame({
            automl_settings[TimeSeries.TIME_COLUMN_NAME]: pd.date_range(new_start, periods=2, freq=bad_freq),
            'someval': 'val',
            TGT: np.arange(2)
        })
        X_test = pd.concat([df2, X_test])
        del df2
        y_train = X_train.pop(TGT).values
        X_test.drop(TGT, inplace=True, axis=1)
        automl = self._create_native_client(automl_settings)
        local_run = automl.fit(X=X_train, y=y_train,
                               compute_target='local', show_output=False)
        _, fitted_model = local_run.get_output()
        y_pred, transformed_pred = fitted_model.forecast(X_test, ignore_data_errors=True)
        assert(np.count_nonzero(pd.isnull(y_pred)) == expcted_non_null)
        fitted_model.quantiles = [0.39]
        quantiles = fitted_model.forecast_quantiles(X_test, ignore_data_errors=True)
        transformed_pred[0.39] = quantiles[0.39].values
        # shuffle the X_test and make sure we get the same predictions and quantiles.
        X_test = X_test.sample(frac=1, random_state=42)
        y_pred, transformed_pred2 = fitted_model.forecast(X_test, ignore_data_errors=True)
        assert(np.count_nonzero(pd.isnull(y_pred)) == expcted_non_null)
        quantiles = fitted_model.forecast_quantiles(X_test, ignore_data_errors=True)
        transformed_pred2[0.39] = quantiles[0.39].values
        # The resulting frames have different order.
        with(pytest.raises(AssertionError)):
            assert_frame_equal(transformed_pred, transformed_pred2)
        # but they have to be equal.
        transformed_pred.sort_index(inplace=True)
        transformed_pred2.sort_index(inplace=True)
        assert_frame_equal(transformed_pred, transformed_pred2)

    def test_compatible_frequency(self, automl_settings):
        """Test forecast on data with more coarse grain frequency."""
        DATE = 'date'
        TGT = 'y'
        HORIZON = 11
        X_train = pd.DataFrame({
            DATE: pd.date_range(start='2001-01-01', end='2001-01-31', freq='D'),
            'someval': 42,
            TGT: np.arange(31)
        })
        y_train = X_train.pop(TGT).values
        X_test = pd.DataFrame({
            DATE: pd.date_range(start='2001-02-01', periods=2, freq='W'),
            'someval': 42,
            TGT: [31, 32]
        })
        X_test.drop(TGT, axis=1, inplace=True)
        automl_settings[TimeSeries.GRAIN_COLUMN_NAMES] = None
        automl_settings[TimeSeries.MAX_HORIZON] = HORIZON
        automl_settings['n_cross_validations'] = 2
        automl = self._create_native_client(automl_settings)
        local_run = automl.fit(X=X_train, y=y_train,
                               compute_target='local', show_output=False)
        _, fitted_model = local_run.get_output()
        y_pred, _ = fitted_model.forecast(X_test, ignore_data_errors=True)
        # Assert that the predictions were generated.
        assert(all(not pd.isnull(y) for y in y_pred))
        assert(len(y_pred) == len(X_test))

    def test_lag_by_occurrence(self, automl_settings):
        """Test forecast on data with more coarse grain frequency."""
        DATE = 'date'
        TGT = 'y'
        HORIZON = 2
        X_train = pd.DataFrame({
            DATE: pd.date_range(start='2001-01-01', end='2001-01-31', freq='D'),
            'someval': 42,
            TGT: np.arange(31)
        })
        X_train.drop([2, 4, 5, 10, 15, 17, 19], axis=0, inplace=True)
        y_train = X_train.pop(TGT).values
        X_test = pd.DataFrame({
            DATE: pd.date_range(start='2001-02-01', periods=2, freq='D'),
            'someval': 42,
            TGT: [31, 32]
        })
        X_test.drop(TGT, axis=1, inplace=True)
        automl_settings[TimeSeries.GRAIN_COLUMN_NAMES] = None
        automl_settings[TimeSeries.TARGET_ROLLING_WINDOW_SIZE] = None
        automl_settings[TimeSeries.TARGET_LAGS] = 1
        automl_settings[TimeSeries.MAX_HORIZON] = HORIZON
        automl_settings['n_cross_validations'] = 2
        automl = self._create_native_client(automl_settings)
        local_run = automl.fit(X=X_train, y=y_train,
                               compute_target='local', show_output=False)
        _, fitted_model = local_run.get_output()
        y_pred, x_trans = fitted_model.forecast(X_test)
        # Assert that the predictions were generated.
        assert(TimeSeriesInternal.DUMMY_TARGET_COLUMN + '_occurrence_lag1D' in x_trans.columns)
        assert(all(not pd.isnull(y) for y in y_pred))
        assert(len(y_pred) == len(X_test))

    def test_feature_lag_by_time(self, automl_settings):
        """ Test forecast with feature lags using non-sparse data."""
        self._do_test_feature_lag(automl_settings, sparse=False)

    def test_feature_lag_by_occurrence(self, automl_settings):
        """ Test forecast with feature lags using sparse data."""
        self._do_test_feature_lag(automl_settings, sparse=True)

    def _do_test_feature_lag(self, automl_settings, sparse=True):
        """Test forecast on data with feature lags."""
        # load multivariate data
        trainset = os.path.join(os.path.dirname(__file__),
                                '../../azureml-automl-runtime/tests/test_data/granger_test_data.csv')
        mv_data = pd.read_csv(trainset)
        NUM_OBS_PER_GRAIN = mv_data.shape[0]
        DATE_COLNAME = 'date'
        TGT = 'y'
        HORIZON = 2
        CONST_COLNAME = 'someval'
        NUM_COLNAME = 'numericvar'
        TRAIN_DATES = pd.date_range('2000-01-01', freq='D', periods=NUM_OBS_PER_GRAIN)
        TEST_DATES = pd.date_range(max(TRAIN_DATES) + to_offset('D'), freq='D', periods=2)

        X_train = pd.DataFrame({
            DATE_COLNAME: TRAIN_DATES,
            CONST_COLNAME: 42,
            NUM_COLNAME: mv_data['x'],
            TGT: mv_data['y']
        })
        if sparse:
            X_train.drop([5, 10, 15, 20, 25, 70, 75, 80, 85, 90], axis=0, inplace=True)
            X_train.reset_index(drop=True, inplace=True)
        y_train = X_train.pop(TGT).values
        X_test = pd.DataFrame({
            DATE_COLNAME: TEST_DATES,
            CONST_COLNAME: 42,
            NUM_COLNAME: np.random.normal(loc=100, scale=20, size=HORIZON).round(),
            TGT: np.random.normal(loc=100, scale=30, size=HORIZON).round()
        })
        X_test.drop(TGT, axis=1, inplace=True)
        automl_settings[TimeSeries.FEATURE_LAGS] = 'auto'
        automl_settings[TimeSeries.GRAIN_COLUMN_NAMES] = None
        automl_settings[TimeSeries.TARGET_ROLLING_WINDOW_SIZE] = None
        automl_settings[TimeSeries.TARGET_LAGS] = 1
        automl_settings[TimeSeries.MAX_HORIZON] = HORIZON
        automl_settings['n_cross_validations'] = 2
        automl = self._create_native_client(automl_settings)
        local_run = automl.fit(X=X_train, y=y_train,
                               compute_target='local', show_output=False)
        _, fitted_model = local_run.get_output()
        y_pred, x_trans = fitted_model.forecast(X_test)
        # Assert that the predictions were generated.
        expected_columns = [NUM_COLNAME]
        if sparse:
            expected_columns = [colname + '_occurrence_lag1D' for colname in expected_columns]
        else:
            expected_columns = [colname + '_lag1D' for colname in expected_columns]
        assert(set(expected_columns).issubset(x_trans.columns))
        assert(all(not pd.isnull(y) for y in y_pred))
        assert(len(y_pred) == len(X_test))

    def test_absent_grain(self, automl_settings):
        """Test if extra grains are dropped in forecasting time."""
        automl_settings[TimeSeries.GRAIN_COLUMN_NAMES] = 'grain'
        automl_settings[TimeSeries.MAX_HORIZON] = 5
        automl_settings['n_cross_validations'] = 2
        automl_settings[TimeSeries.SHORT_SERIES_HANDLING] = True
        automl_settings[TimeSeries.SHORT_SERIES_HANDLING_CONFIG] = ShortSeriesHandlingValues.SHORT_SERIES_HANDLING_DROP
        automl = self._create_native_client(automl_settings)
        X_train, y_train, X_test, _ = self.get_simple_grain_data(automl_settings)
        X_train['y'] = y_train
        bad_grain = 'grain1'
        X_train = X_train[X_train['grain'] != bad_grain]
        y_train = X_train.pop('y').values
        local_run = automl.fit(X=X_train, y=y_train,
                               compute_target='local', show_output=False)
        _, fitted_model = local_run.get_output()
        fitted_model.quantiles = [0.25, 0.75]
        y_obs, transformed = fitted_model.forecast(X_test, ignore_data_errors=True)
        assert_array_equal(y_obs, transformed[TimeSeriesInternal.DUMMY_TARGET_COLUMN].values)
        assert(len(y_obs) == len(X_test))
        quantiles = fitted_model.forecast_quantiles(X_test)
        assert(len(y_obs) == len(quantiles))
        transformed.reset_index(inplace=True, drop=False)
        quantiles.reset_index(inplace=True, drop=True)
        join_on = [automl_settings[TimeSeries.TIME_COLUMN_NAME], automl_settings[TimeSeries.GRAIN_COLUMN_NAMES]]
        transformed = transformed.merge(quantiles, on=join_on, how='inner')
        for grain, df in transformed.groupby('grain'):
            if grain == bad_grain:
                assert(all(np.isnan(y) for y in df[TimeSeriesInternal.DUMMY_TARGET_COLUMN]))
                assert(all(np.isnan(y) for y in df[0.25]))
                assert(all(np.isnan(y) for y in df[0.75]))
            else:
                assert(not any(np.isnan(y) for y in df[TimeSeriesInternal.DUMMY_TARGET_COLUMN]))
                assert(not any(np.isnan(y) for y in df[0.25]))
                assert(not any(np.isnan(y) for y in df[0.75]))

    def test_grain_with_single_value(self, automl_settings):
        """Test that grain with only one value is efficiently dropped."""
        automl_settings[TimeSeries.GRAIN_COLUMN_NAMES] = 'grain'
        automl_settings[TimeSeries.MAX_HORIZON] = 5
        automl_settings['n_cross_validations'] = 2
        automl_settings[TimeSeries.SHORT_SERIES_HANDLING] = True
        automl_settings[TimeSeries.SHORT_SERIES_HANDLING_CONFIG] = ShortSeriesHandlingValues.SHORT_SERIES_HANDLING_DROP
        automl = self._create_native_client(automl_settings)
        X_train, y_train, X_test, _ = self.get_simple_grain_data(automl_settings)
        X_train['y'] = y_train
        X_train = X_train.groupby(
            automl_settings[TimeSeries.GRAIN_COLUMN_NAMES],
            as_index=False, group_keys=False).apply(lambda x: x if x.name == 'grain1' else x[:1])
        y_train = X_train.pop('y').values
        local_run = automl.fit(X=X_train, y=y_train,
                               compute_target='local', show_output=False)
        _, fitted_model = local_run.get_output()
        y_obs, transformed = fitted_model.forecast(X_test)
        assert_array_equal(y_obs, transformed[TimeSeriesInternal.DUMMY_TARGET_COLUMN].values)
        for grain, df in transformed.groupby('grain'):
            if grain == 'grain2':
                assert(all(np.isnan(y) for y in df[TimeSeriesInternal.DUMMY_TARGET_COLUMN]))
            else:
                assert(not any(np.isnan(y) for y in df[TimeSeriesInternal.DUMMY_TARGET_COLUMN]))

    def test_one_grain_data_in_begin(self, automl_settings):
        """Test forecast if one grain having the values at the begin and end."""
        automl_settings[TimeSeries.GRAIN_COLUMN_NAMES] = 'grain'
        automl_settings[TimeSeries.MAX_HORIZON] = 1
        automl_settings['n_cross_validations'] = 3
        automl_settings[TimeSeries.SHORT_SERIES_HANDLING] = True
        automl_settings[TimeSeries.SHORT_SERIES_HANDLING_CONFIG] = ShortSeriesHandlingValues.SHORT_SERIES_HANDLING_DROP
        automl_settings[TimeSeries.TARGET_LAGS] = [1]
        data_length = 60
        bad_len = 2 * automl_settings[TimeSeries.MAX_HORIZON] + 3 + 1 + 3
        TGT = 'y'
        X = pd.DataFrame({
            automl_settings[TimeSeries.TIME_COLUMN_NAME]: pd.date_range(start='2000-01-01',
                                                                        periods=data_length,
                                                                        freq='D'),
            TGT: np.arange(data_length),
            'ext_predictor': np.asarray(range(42, 42 + data_length)),
            automl_settings[TimeSeries.GRAIN_COLUMN_NAMES]: 'good_grain'
        })

        X_bad = X.copy()
        X_bad[automl_settings[TimeSeries.GRAIN_COLUMN_NAMES]] = 'bad_grain'
        X_bad = X_bad[:bad_len + 1]
        X_bad[TGT][1:-3 - automl_settings[TimeSeries.MAX_HORIZON]] = np.NaN
        X_train = pd.concat([
            X[:-automl_settings[TimeSeries.MAX_HORIZON]],
            X_bad[:-automl_settings[TimeSeries.MAX_HORIZON]]
        ])
        X_test = pd.concat([
            X[-automl_settings[TimeSeries.MAX_HORIZON]:],
            X_bad[-automl_settings[TimeSeries.MAX_HORIZON]:]
        ])
        y_train = X_train.pop(TGT).values
        X_test.drop(TGT, inplace=True, axis=1)
        automl = self._create_native_client(automl_settings)
        local_run = automl.fit(X=X_train, y=y_train,
                               compute_target='local', show_output=False)
        _, fitted_model = local_run.get_output()
        fitted_model.quantiles = [0.25]
        y_obs, transformed = fitted_model.forecast(X_test)
        assert_array_equal(y_obs, transformed[TimeSeriesInternal.DUMMY_TARGET_COLUMN])
        quantiles = fitted_model.forecast_quantiles(X_test)
        assert(len(y_obs) == len(quantiles))
        quantiles.reset_index(inplace=True, drop=True)
        join_on = [automl_settings[TimeSeries.TIME_COLUMN_NAME], automl_settings[TimeSeries.GRAIN_COLUMN_NAMES]]
        transformed = transformed.merge(quantiles, on=join_on, how='inner')
        for grain, df in transformed.groupby(automl_settings[TimeSeries.GRAIN_COLUMN_NAMES]):
            if grain == 'bad_grain':
                assert(all(np.isnan(y) for y in df[TimeSeriesInternal.DUMMY_TARGET_COLUMN]))
                assert(all(np.isnan(y) for y in df[0.25]))
            else:
                assert(not any(np.isnan(y) for y in df[TimeSeriesInternal.DUMMY_TARGET_COLUMN]))
                assert(not any(np.isnan(y) for y in df[0.25]))

    def test_high_frequency_contamination(self, automl_settings):
        """Test that contaminating high frequency will be removed."""
        automl_settings[TimeSeries.GRAIN_COLUMN_NAMES] = 'grain'
        automl_settings[TimeSeries.MAX_HORIZON] = 5
        automl_settings['n_cross_validations'] = 2
        automl_settings[TimeSeries.SHORT_SERIES_HANDLING] = True
        automl_settings[TimeSeries.SHORT_SERIES_HANDLING_CONFIG] = ShortSeriesHandlingValues.SHORT_SERIES_HANDLING_DROP
        automl = self._create_native_client(automl_settings)
        X_train, y_train, X_test, _ = self.get_simple_grain_data(automl_settings, ntest=5, total_sz=105)
        bad_indices = {
            'grain1': [0, 4, 10],
            'grain2': [1, 7, 99]
        }
        X_train['y'] = y_train
        # We will add the contaminating frequency to the training set.
        dfs = []
        contaminate_freq = to_offset('H')
        for grain, df in X_train.groupby('grain'):
            contamination = df.iloc[bad_indices[grain]].copy()
            contamination[automl_settings[TimeSeries.TIME_COLUMN_NAME]] += contaminate_freq
            df = df.append(contamination)
            dfs.append(df)
        X_train = pd.concat(dfs)
        X_train.reset_index(drop=True, inplace=True)
        y_train = X_train.pop('y').values
        # Add some outliers to the test set.
        dfs = []
        for grain, df in X_test.groupby('grain'):
            contamination = df.iloc[[1, 3, 4]].copy()
            contamination[automl_settings[TimeSeries.TIME_COLUMN_NAME]] += contaminate_freq
            df = df.append(contamination)
            dfs.append(df)
        X_test = pd.concat(dfs)
        X_test.reset_index(drop=True, inplace=True)
        local_run = automl.fit(X=X_train, y=y_train,
                               compute_target='local', show_output=False)
        _, fitted_model = local_run.get_output()
        assert fitted_model.data_frequency == to_offset('D')
        y_obs, transformed = fitted_model.forecast(X_test, ignore_data_errors=True)
        assert_array_equal(y_obs, transformed[TimeSeriesInternal.DUMMY_TARGET_COLUMN])
        transformed.reset_index(drop=False, inplace=True)
        for grain, df in transformed.groupby('grain'):
            assert all(pd.isnull(y) for y in df[TimeSeriesInternal.DUMMY_TARGET_COLUMN].iloc[-3:])
            assert all(not pd.isnull(y) for y in df[TimeSeriesInternal.DUMMY_TARGET_COLUMN].iloc[:-3])

    def test_user_set_freq(self, automl_settings):
        """Test freq parameter set by user."""
        automl_settings[TimeSeries.MAX_HORIZON] = 5
        automl_settings['n_cross_validations'] = 2
        automl_settings[TimeSeries.FREQUENCY] = '2D'
        automl = self._create_native_client(automl_settings)
        length_df = 22
        x_df = pd.DataFrame({
            automl_settings[TimeSeries.TIME_COLUMN_NAME]: pd.date_range('2001-01-01', freq='2D', periods=length_df),
            'val': 42,
            'y': np.arange(length_df)
        })
        length_df_add = 2
        x_df_add = pd.DataFrame({
            automl_settings[TimeSeries.TIME_COLUMN_NAME]: pd.date_range(
                '2001-01-02', freq='2D', periods=length_df_add),
            'val': 42,
            'y': np.arange(length_df_add)
        })
        X_train = pd.concat([x_df, x_df_add])
        X_train.sort_values(by=automl_settings[TimeSeries.TIME_COLUMN_NAME],
                            inplace=True)
        X_train.reset_index(inplace=True, drop=True)
        day = to_offset('D')
        new_start = X_train[automl_settings[TimeSeries.TIME_COLUMN_NAME]].max() + 2 * day
        X_test = pd.DataFrame({
            automl_settings[TimeSeries.TIME_COLUMN_NAME]: pd.date_range(
                new_start, freq='D', periods=2),
            'val': 42
        })
        X_train.drop('y', axis=1, inplace=True)
        y_train = self.get_stationary_data(length_df + length_df_add)
        local_run = automl.fit(X=X_train, y=y_train,
                               compute_target='local', show_output=False)
        _, fitted_model = local_run.get_output()
        assert fitted_model.data_frequency == to_offset('2D')
        y_pred, x_pred = fitted_model.forecast(X_test, ignore_data_errors=True)
        grid = pd.date_range(
            start=X_train[automl_settings[TimeSeries.TIME_COLUMN_NAME]].max() + 2 * day,
            end=X_test[automl_settings[TimeSeries.TIME_COLUMN_NAME]].max(),
            freq='2D')
        assert_array_equal(y_pred, x_pred[TimeSeriesInternal.DUMMY_TARGET_COLUMN].values)
        x_pred.reset_index(drop=False, inplace=True)
        for ix in range(len(x_pred)):
            if x_pred[automl_settings[TimeSeries.TIME_COLUMN_NAME]][ix] in grid:
                assert not pd.isna(x_pred[TimeSeriesInternal.DUMMY_TARGET_COLUMN][ix])
            else:
                assert pd.isna(x_pred[TimeSeriesInternal.DUMMY_TARGET_COLUMN][ix])

    def test_wrong_frequency_short_grains(self, automl_settings):
        """Test wrong frequency on short grain does not break the forecast."""
        automl_settings[TimeSeries.GRAIN_COLUMN_NAMES] = 'grain'
        automl_settings[TimeSeries.MAX_HORIZON] = 5
        automl_settings['n_cross_validations'] = 2
        automl_settings[TimeSeries.SHORT_SERIES_HANDLING] = True
        automl_settings[TimeSeries.SHORT_SERIES_HANDLING_CONFIG] = ShortSeriesHandlingValues.SHORT_SERIES_HANDLING_DROP
        automl_settings[TimeSeries.TARGET_LAGS] = None
        automl_settings[TimeSeries.TARGET_ROLLING_WINDOW_SIZE] = None
        automl = self._create_native_client(automl_settings)
        df = pd.DataFrame({
            automl_settings[TimeSeries.TIME_COLUMN_NAME]: pd.date_range(
                '2001-01-01', freq='D', periods=42),
            automl_settings[TimeSeries.GRAIN_COLUMN_NAMES]: 'good',
            'val': 'not 42',
            'y': np.arange(42)
        })
        df = df.append(pd.DataFrame({
            automl_settings[TimeSeries.TIME_COLUMN_NAME]: pd.date_range(
                '2001-01-01', freq='2D', periods=14),
            automl_settings[TimeSeries.GRAIN_COLUMN_NAMES]: 'bad_grain',
            'val': 'not 42',
            'y': np.arange(14)
        }))
        X_train, X_test = self.split_last_n_by_grain(df, 5, automl_settings)
        y_train = X_train.pop('y').values
        X_test.drop('y', inplace=True, axis=1)
        X_test.reset_index(drop=True, inplace=True)
        local_run = automl.fit(X=X_train, y=y_train,
                               compute_target='local', show_output=False)
        _, fitted_model = local_run.get_output()
        fitted_model.quantiles = [0.25]
        y_obs, transformed = fitted_model.forecast(X_test)
        assert_array_equal(y_obs, transformed[TimeSeriesInternal.DUMMY_TARGET_COLUMN])
        quantiles = fitted_model.forecast_quantiles(X_test)
        assert(len(y_obs) == len(quantiles))
        quantiles.reset_index(inplace=True, drop=True)
        join_on = [automl_settings[TimeSeries.TIME_COLUMN_NAME], automl_settings[TimeSeries.GRAIN_COLUMN_NAMES]]
        transformed = transformed.merge(quantiles, on=join_on, how='inner')
        for grain, df in transformed.groupby(automl_settings[TimeSeries.GRAIN_COLUMN_NAMES]):
            if grain == 'bad_grain':
                assert(all(np.isnan(y) for y in df[TimeSeriesInternal.DUMMY_TARGET_COLUMN]))
                assert(all(np.isnan(y) for y in df[0.25]))
            else:
                assert(not any(np.isnan(y) for y in df[TimeSeriesInternal.DUMMY_TARGET_COLUMN]))
                assert(not any(np.isnan(y) for y in df[0.25]))

    def test_the_same_y_ok(self, automl_settings):
        """Test that the same y values raises the exception."""
        automl_settings[TimeSeries.GRAIN_COLUMN_NAMES] = 'grain'
        automl_settings['n_cross_validations'] = 2
        automl = self._create_native_client(automl_settings)
        X_train = pd.DataFrame({
            automl_settings[TimeSeries.TIME_COLUMN_NAME]: pd.date_range(
                '2001-01-01', freq='D', periods=42),
            automl_settings[TimeSeries.GRAIN_COLUMN_NAMES]: 'good',
            'val': 'not 42',
            'y': np.repeat(22, 42)
        })
        y_train = X_train.pop('y').values
        y_before = y_train.copy()
        automl.fit(X=X_train, y=y_train,
                   compute_target='local', show_output=False)
        assert_array_equal(y_train, y_before)

    def test_short_grain_padding_no_grain(self, automl_settings):
        """Test if short grains are being padded."""
        automl_settings[TimeSeries.GRAIN_COLUMN_NAMES] = None
        automl_settings[TimeSeries.MAX_HORIZON] = 5
        automl_settings['n_cross_validations'] = 2
        automl_settings[TimeSeries.SHORT_SERIES_HANDLING] = True
        automl_settings[TimeSeries.SHORT_SERIES_HANDLING_CONFIG] =\
            ShortSeriesHandlingValues.SHORT_SERIES_HANDLING_AUTO
        automl_settings[TimeSeries.FREQUENCY] = 'D'
        automl = self._create_native_client(automl_settings)
        X_train = pd.DataFrame([
            ['2000-01-01', 42]],
            columns=['date', 'val']
        )
        y_train = np.array([12])
        X_test = pd.DataFrame([
            ['2000-01-02', 42]],
            columns=['date', 'val']
        )
        local_run = automl.fit(X=X_train, y=y_train,
                               compute_target='local', show_output=False)
        _, fitted_model = local_run.get_output()
        y_obs, transformed = fitted_model.forecast(X_test)
        assert_array_equal(y_obs, transformed[TimeSeriesInternal.DUMMY_TARGET_COLUMN].values)
        assert not transformed[TimeSeriesInternal.DUMMY_TARGET_COLUMN].isnull().any()

    def test_short_grain_padding(self, automl_settings):
        """Test if short grains are being padded."""
        automl_settings[TimeSeries.GRAIN_COLUMN_NAMES] = 'grain'
        automl_settings[TimeSeries.MAX_HORIZON] = 5
        automl_settings['n_cross_validations'] = 2
        automl_settings[TimeSeries.SHORT_SERIES_HANDLING] = True
        automl_settings[TimeSeries.SHORT_SERIES_HANDLING_CONFIG] =\
            ShortSeriesHandlingValues.SHORT_SERIES_HANDLING_PAD
        automl = self._create_native_client(automl_settings)
        X_train, y_train, X_test, y_valid = self.get_simple_grain_data(automl_settings)
        X_train['y'] = y_train
        X_train = X_train.groupby(
            automl_settings[TimeSeries.GRAIN_COLUMN_NAMES],
            as_index=False, group_keys=False).apply(lambda x: x if x.name == 'grain1' else x[-1:])
        y_train = X_train.pop('y').values
        local_run = automl.fit(X=X_train, y=y_train,
                               compute_target='local', show_output=False)
        _, fitted_model = local_run.get_output()
        y_obs, transformed = fitted_model.forecast(X_test)
        assert_array_equal(y_obs, transformed[TimeSeriesInternal.DUMMY_TARGET_COLUMN].values)
        assert not transformed[TimeSeriesInternal.DUMMY_TARGET_COLUMN].isnull().any()
        # assert that grains are not padded if short_grain_handling_config is set to "auto".
        automl_settings[TimeSeries.SHORT_SERIES_HANDLING_CONFIG] =\
            ShortSeriesHandlingValues.SHORT_SERIES_HANDLING_AUTO
        automl = self._create_native_client(automl_settings)
        local_run = automl.fit(X=X_train, y=y_train,
                               compute_target='local', show_output=False)
        _, fitted_model = local_run.get_output()
        y_obs, transformed = fitted_model.forecast(X_test)
        transformed.reset_index(inplace=True, drop=False)
        assert not transformed[transformed['grain'] == 'grain1'][TimeSeriesInternal.DUMMY_TARGET_COLUMN].isnull().any()
        assert transformed[transformed['grain'] != 'grain1'][TimeSeriesInternal.DUMMY_TARGET_COLUMN].isnull().all()
        # assert that the grain is not padded if the validation set is used.
        automl_settings['n_cross_validations'] = None
        automl_settings[TimeSeries.SHORT_SERIES_HANDLING_CONFIG] =\
            ShortSeriesHandlingValues.SHORT_SERIES_HANDLING_AUTO
        X_valid = X_test.copy()
        freq = to_offset('D')
        dfs = []
        for grain, df in X_test.groupby('grain'):
            df[automl_settings[TimeSeries.TIME_COLUMN_NAME]] = pd.date_range(
                df[automl_settings[TimeSeries.TIME_COLUMN_NAME]].max() + freq,
                periods=automl_settings[TimeSeries.MAX_HORIZON], freq=freq)
            dfs.append(df)
        X_test = pd.concat(dfs)
        automl = self._create_native_client(automl_settings)
        local_run = automl.fit(X=X_train, y=y_train,
                               X_valid=X_valid, y_valid=y_valid,
                               compute_target='local', show_output=False)
        _, fitted_model = local_run.get_output()
        X_valid['y'] = y_valid
        X_test['y'] = np.NaN
        X_test = pd.concat([X_valid, X_test])
        y_test = X_test.pop('y').values
        y_obs, transformed = fitted_model.forecast(X_test, y_test)
        assert_array_equal(y_obs, transformed[TimeSeriesInternal.DUMMY_TARGET_COLUMN].values)
        transformed.reset_index(inplace=True, drop=False)
        # Trim the valid part
        transformed = (
            transformed[transformed[automl_settings[TimeSeries.TIME_COLUMN_NAME]] >
                        X_valid[automl_settings[TimeSeries.TIME_COLUMN_NAME]].max()])
        assert not transformed[transformed['grain'] == 'grain1'][TimeSeriesInternal.DUMMY_TARGET_COLUMN].isnull().any()
        assert transformed[transformed['grain'] != 'grain1'][TimeSeriesInternal.DUMMY_TARGET_COLUMN].isnull().all()

    def test_all_grain_with_one_value_padded(self, automl_settings):
        """Test if freq can not be retrieved."""
        automl_settings[TimeSeries.GRAIN_COLUMN_NAMES] = 'grain'
        automl_settings[TimeSeries.SHORT_SERIES_HANDLING] = True
        automl_settings[TimeSeries.SHORT_SERIES_HANDLING_CONFIG] =\
            ShortSeriesHandlingValues.SHORT_SERIES_HANDLING_AUTO
        automl_settings[TimeSeries.FREQUENCY] = 'D'
        automl_settings['n_cross_validations'] = 2
        X_train = pd.DataFrame([
            ['2000-01-01', 'a', 42, 12],
            ['2000-01-01', 'b', 42, 12],
            ['2000-01-01', 'c', 42, 12]],
            columns=['date', 'grain', 'val', 'y']
        )
        y_train = X_train.pop('y').values
        X_test = pd.DataFrame([
            ['2000-01-02', 'a', 42],
            ['2000-01-02', 'b', 42],
            ['2000-01-02', 'c', 42]],
            columns=['date', 'grain', 'val']
        )
        automl = self._create_native_client(automl_settings)
        local_run = automl.fit(X=X_train, y=y_train,
                               compute_target='local', show_output=False)
        _, fitted_model = local_run.get_output()
        y_pred, x_pred = fitted_model.forecast(X_test)
        assert not x_pred[TimeSeriesInternal.DUMMY_TARGET_COLUMN].isnull().any()
        # Test that the same happens when short_grain_handling is set to 'pad'
        automl_settings[TimeSeries.SHORT_SERIES_HANDLING_CONFIG] =\
            ShortSeriesHandlingValues.SHORT_SERIES_HANDLING_PAD
        automl = self._create_native_client(automl_settings)
        local_run = automl.fit(X=X_train, y=y_train,
                               compute_target='local', show_output=False)
        _, fitted_model = local_run.get_output()
        y_pred, x_pred = fitted_model.forecast(X_test)
        assert not x_pred[TimeSeriesInternal.DUMMY_TARGET_COLUMN].isnull().any()

    def test_all_grain_with_one_value_padded_nat(self, automl_settings):
        """Test if freq can not be retrieved."""
        automl_settings[TimeSeries.GRAIN_COLUMN_NAMES] = 'grain'
        automl_settings[TimeSeries.SHORT_SERIES_HANDLING] = True
        automl_settings[TimeSeries.SHORT_SERIES_HANDLING_CONFIG] =\
            ShortSeriesHandlingValues.SHORT_SERIES_HANDLING_AUTO
        automl_settings[TimeSeries.FREQUENCY] = 'D'
        automl_settings['n_cross_validations'] = 2
        X_train = pd.DataFrame([
            ['2000-01-01', 'a', 42, 12],
            ['2000-01-01', 'b', 42, 12],
            [pd.NaT, 'c', 42, 12]],
            columns=['date', 'grain', 'val', 'y']
        )
        y_train = X_train.pop('y').values
        X_test = pd.DataFrame([
            ['2000-01-02', 'a', 42],
            ['2000-01-02', 'b', 42],
            ['2000-01-02', 'c', 42]],
            columns=['date', 'grain', 'val']
        )
        automl = self._create_native_client(automl_settings)
        local_run = automl.fit(X=X_train, y=y_train,
                               compute_target='local', show_output=False)
        _, fitted_model = local_run.get_output()
        y_pred, x_pred = fitted_model.forecast(X_test)
        assert_array_equal(y_pred, x_pred[TimeSeriesInternal.DUMMY_TARGET_COLUMN].values)
        x_pred.reset_index(inplace=True, drop=False)
        assert x_pred[x_pred['grain'] == 'c'][TimeSeriesInternal.DUMMY_TARGET_COLUMN].isnull().all()
        assert not x_pred[x_pred['grain'] != 'c'][TimeSeriesInternal.DUMMY_TARGET_COLUMN].isnull().any()

    def test_all_grain_with_one_value_raises(self, automl_settings):
        """Test the exception is raised if there is no freq parameter."""
        automl_settings[TimeSeries.GRAIN_COLUMN_NAMES] = 'grain'
        automl_settings[TimeSeries.SHORT_SERIES_HANDLING] = True
        automl_settings[TimeSeries.SHORT_SERIES_HANDLING_CONFIG] =\
            ShortSeriesHandlingValues.SHORT_SERIES_HANDLING_PAD
        X_train = pd.DataFrame([
            ['2000-01-01', 'a', True, 41.1, 32, '44', 12],
            ['2000-01-01', 'b', False, 41.2, 33, '45', 12],
            ['2000-01-01', 'c', False, 41.3, 34, '46', 12]],
            columns=['date', 'grain', 'some_bool', 'float_val', 'val', 'str_val', 'y']
        )
        y_train = X_train.pop('y').values
        automl = self._create_native_client(automl_settings)
        with pytest.raises(ForecastingDataException) as cm:
            automl.fit(X=X_train, y=y_train,
                       compute_target='local', show_output=False)
        assert cm.value._target == 'unique_timepoints'

    def test_aggregation_one_grain(self, automl_settings):
        """Test aggregation of the data by frequency."""
        automl_settings[TimeSeries.FREQUENCY] = '3D'
        automl_settings[TimeSeries.TARGET_AGG_FUN] = AggregationFunctions.MIN
        automl_settings[TimeSeries.GRAIN_COLUMN_NAMES] = None
        automl_settings['n_cross_validations'] = 2
        automl_settings[TimeSeries.MAX_HORIZON] = 2
        del automl_settings[TimeSeries.TARGET_LAGS]
        del automl_settings[TimeSeries.TARGET_ROLLING_WINDOW_SIZE]
        X_train = pd.DataFrame({
            automl_settings[TimeSeries.TIME_COLUMN_NAME]: pd.date_range('2001-01-01', freq='D', periods=21),
            'val': [1, 2, 3] * 7,
            'cat_val': np.repeat(['a', 'b', 'c'], 7),
            'date_val': list(pd.date_range('2020-01-01', freq='D', periods=3)) * 7,
        })
        y_train = np.arange(len(X_train))
        X_test = pd.DataFrame({
            automl_settings[TimeSeries.TIME_COLUMN_NAME]: pd.date_range(
                '2001-01-22', freq='D', periods=6),
            'val': [3, 4, 5, 5, 6, 7],
            'cat_val': ['a', 'a', 'b', 'b', 'b', 'c'],
            'date_val': list(pd.date_range('2020-01-01', freq='D', periods=3)) * 2,
        })
        automl = self._create_native_client(automl_settings)
        local_run = automl.fit(X=X_train, y=y_train,
                               compute_target='local', show_output=False)
        _, fitted_model = local_run.get_output()
        y_pred, x_pred = fitted_model.forecast(X_test)
        assert not any(np.isnan(y) for y in y_pred)
        assert_array_equal(y_pred, x_pred[TimeSeriesInternal.DUMMY_TARGET_COLUMN].values)
        for col in ['val_min', 'val_max', 'val_sum', 'val_mean', 'cat_val_mode',
                    'date_val_min_Day', 'date_val_max_Day', 'date_val_mode_Day']:
            assert col in x_pred.columns, 'The column {} was not found.'.format(col)
        x_pred.reset_index(inplace=True, drop=False)
        sr_time_expected = pd.Series(pd.to_datetime(['2001-01-22', '2001-01-25']),
                                     name=automl_settings[TimeSeries.TIME_COLUMN_NAME])
        assert_series_equal(x_pred[automl_settings[TimeSeries.TIME_COLUMN_NAME]], sr_time_expected)
        x_quant = fitted_model.forecast_quantiles(X_test)
        assert not any(np.isnan(quant) for quant in x_quant[0.5])
        quantiles_list = [0.33, 0.56, 0.69]
        x_quant = fitted_model.forecast_quantiles(X_test, quantiles=quantiles_list)
        for q in quantiles_list:
            assert not any(np.isnan(quant) for quant in x_quant[q])
        x_quant = fitted_model.forecast_quantiles(X_test)
        assert [q not in x_quant.columns.tolist() for q in quantiles_list]
        assert_series_equal(x_quant[automl_settings[TimeSeries.TIME_COLUMN_NAME]], sr_time_expected)

    def test_aggregation_two_grains(self, automl_settings):
        """Test aggregation of the data by frequency."""
        GRAIN = 'grain'
        automl_settings[TimeSeries.FREQUENCY] = '3D'
        automl_settings[TimeSeries.TARGET_AGG_FUN] = AggregationFunctions.MIN
        automl_settings[TimeSeries.GRAIN_COLUMN_NAMES] = GRAIN
        automl_settings['n_cross_validations'] = 2
        automl_settings[TimeSeries.MAX_HORIZON] = 2
        del automl_settings[TimeSeries.TARGET_LAGS]
        del automl_settings[TimeSeries.TARGET_ROLLING_WINDOW_SIZE]
        X_train = pd.DataFrame({
            automl_settings[TimeSeries.TIME_COLUMN_NAME]: pd.date_range('2001-01-01', freq='D', periods=21),
            GRAIN: 'g1',
            'val': [1, 2, 3] * 7,
            'cat_val': np.repeat(['a', 'b', 'c'], 7),
            'date_val': list(pd.date_range('2020-01-01', freq='D', periods=3)) * 7,
        })
        X_train = X_train.append(pd.DataFrame({
            automl_settings[TimeSeries.TIME_COLUMN_NAME]: pd.date_range('2001-01-01', freq='D', periods=21),
            GRAIN: 'g2',
            'val': [1, 2, 3] * 7,
            'cat_val': np.repeat(['a', 'b', 'c'], 7),
            'date_val': list(pd.date_range('2020-01-01', freq='D', periods=3)) * 7,
        }))
        y_train = np.arange(len(X_train))
        X_test = pd.DataFrame({
            automl_settings[TimeSeries.TIME_COLUMN_NAME]: list(pd.date_range(
                '2001-01-22', freq='D', periods=6)) + list(
                    pd.date_range(
                        '2001-01-22', freq='D', periods=6)),
            GRAIN: np.repeat(['g1', 'g2'], 6),
            'val': [3, 4, 5, 5, 6, 7] * 2,
            'cat_val': ['a', 'a', 'b', 'b', 'b', 'c'] * 2,
            'date_val': list(pd.date_range('2020-01-01', freq='D', periods=3)) * 4,
        })
        automl = self._create_native_client(automl_settings)
        local_run = automl.fit(X=X_train, y=y_train,
                               compute_target='local', show_output=False)
        _, fitted_model = local_run.get_output()
        y_pred, x_pred = fitted_model.forecast(X_test)
        assert not any(np.isnan(y) for y in y_pred)
        assert_array_equal(y_pred, x_pred[TimeSeriesInternal.DUMMY_TARGET_COLUMN].values)
        for col in ['val_min', 'val_max', 'val_sum', 'val_mean', 'cat_val_mode',
                    'date_val_min_Day', 'date_val_max_Day', 'date_val_mode_Day']:
            assert col in x_pred.columns, 'The column {} was not found.'.format(col)
        x_pred.reset_index(inplace=True, drop=False)
        sr_time_expected = pd.Series(pd.to_datetime(['2001-01-22', '2001-01-25', '2001-01-22', '2001-01-25']),
                                     name=automl_settings[TimeSeries.TIME_COLUMN_NAME])
        assert_series_equal(x_pred[automl_settings[TimeSeries.TIME_COLUMN_NAME]], sr_time_expected)
        x_quant = fitted_model.forecast_quantiles(X_test)
        assert not any(np.isnan(quant) for quant in x_quant[0.5])
        assert_series_equal(x_quant[automl_settings[TimeSeries.TIME_COLUMN_NAME]], sr_time_expected)

    def _do_test_aggregation_with_lookback(self, X_train, X_test, automl_settings, is_sparce):
        """Test that both lookback and aggregated features were created."""
        y_train = X_train.pop(TimeSeriesInternal.DUMMY_TARGET_COLUMN).values
        automl = self._create_native_client(automl_settings)
        local_run = automl.fit(X=X_train, y=y_train,
                               compute_target='local', show_output=False)
        _, fitted_model = local_run.get_output()
        y_pred, x_pred = fitted_model.forecast(X_test)
        assert_array_equal(y_pred, x_pred[TimeSeriesInternal.DUMMY_TARGET_COLUMN])
        assert not any(np.isnan(y) for y in y_pred)
        if is_sparce:
            lag_col = TimeSeriesInternal.DUMMY_TARGET_COLUMN + '_occurrence_lag1D'
        else:
            lag_col = TimeSeriesInternal.DUMMY_TARGET_COLUMN + '_lag1D'
        assert lag_col in x_pred.columns
        for fun in ['_min', '_max', '_mean']:
            assert TimeSeriesInternal.DUMMY_TARGET_COLUMN + fun + '_window5D' in x_pred.columns
        for fun in ['sum', 'min', 'max', 'mean']:
            assert 'val_' + fun in x_pred.columns

        def check_df(df):
            """Check the validity of a data frame."""
            expected_dt = pd.Series(pd.date_range('2020-02-10', freq='2D', periods=2),
                                    name=automl_settings[TimeSeries.TIME_COLUMN_NAME])
            if automl_settings[TimeSeries.GRAIN_COLUMN_NAMES]:
                for _, df_one in df.groupby(automl_settings[TimeSeries.GRAIN_COLUMN_NAMES]):
                    assert_series_equal(
                        df_one[automl_settings[TimeSeries.TIME_COLUMN_NAME]].reset_index(drop=True), expected_dt)
                    assert df_one.shape[0] == 2
            else:
                assert_series_equal(
                    df[automl_settings[TimeSeries.TIME_COLUMN_NAME]].reset_index(drop=True), expected_dt)
                assert df.shape[0] == 2

        x_pred.reset_index(inplace=True, drop=False)
        check_df(x_pred)
        x_quant = fitted_model.forecast_quantiles(X_test)
        check_df(x_quant)
        assert not any(np.isnan(quant) for quant in x_quant[0.5])

    def test_aggregation_with_lookback(self, automl_settings):
        """Test aggregation works if lookback features are enabled."""
        LEN = 40
        ds_freq = to_offset('D')
        automl_settings[TimeSeries.FREQUENCY] = '2D'
        automl_settings[TimeSeries.TARGET_AGG_FUN] = AggregationFunctions.MIN
        automl_settings[TimeSeries.GRAIN_COLUMN_NAMES] = None
        automl_settings['n_cross_validations'] = 2
        automl_settings[TimeSeries.MAX_HORIZON] = 2
        dates = pd.date_range('2020-01-01', freq=ds_freq, periods=LEN)
        X_train = pd.DataFrame({
            automl_settings[TimeSeries.TIME_COLUMN_NAME]: dates,
            'val': np.arange(LEN),
            TimeSeriesInternal.DUMMY_TARGET_COLUMN: np.arange(LEN)
        })
        TEST_LEN = 2 * automl_settings[TimeSeries.MAX_HORIZON]
        X_test = pd.DataFrame({
            automl_settings[TimeSeries.TIME_COLUMN_NAME]: pd.date_range(
                dates.max() + ds_freq, freq=ds_freq, periods=TEST_LEN),
            'val': np.arange(40, 40 + TEST_LEN),
            TimeSeriesInternal.DUMMY_TARGET_COLUMN: np.arange(40, 40 + TEST_LEN)
        })
        self._do_test_aggregation_with_lookback(X_train, X_test, automl_settings, False)

    def test_aggregation_with_lookback_sparce(self, automl_settings):
        """Test aggregation works if lookback features are enabled."""
        LEN = 40
        ds_freq = to_offset('D')
        automl_settings[TimeSeries.FREQUENCY] = '2D'
        automl_settings[TimeSeries.TARGET_AGG_FUN] = AggregationFunctions.MIN
        automl_settings[TimeSeries.GRAIN_COLUMN_NAMES] = None
        automl_settings['n_cross_validations'] = 2
        automl_settings[TimeSeries.MAX_HORIZON] = 2
        dates = pd.date_range('2020-01-01', freq='D', periods=LEN)
        X_train = pd.DataFrame({
            automl_settings[TimeSeries.TIME_COLUMN_NAME]: dates,
            'val': np.arange(LEN),
            TimeSeriesInternal.DUMMY_TARGET_COLUMN: np.arange(LEN)
        })
        X_train = X_train.sample(frac=0.7, random_state=42)
        last_date = X_train[automl_settings[TimeSeries.TIME_COLUMN_NAME]].max()
        TEST_LEN = 2 * automl_settings[TimeSeries.MAX_HORIZON]
        X_test = pd.DataFrame({
            automl_settings[TimeSeries.TIME_COLUMN_NAME]: pd.date_range(
                last_date + ds_freq, freq='D', periods=TEST_LEN),
            'val': np.arange(40, 40 + TEST_LEN),
            TimeSeriesInternal.DUMMY_TARGET_COLUMN: np.arange(40, 40 + TEST_LEN)
        })
        self._do_test_aggregation_with_lookback(X_train, X_test, automl_settings, True)

    def test_aggregation_with_lookback_grain(self, automl_settings):
        """Test aggregation works if lookback features are enabled. on data set with grains."""
        LEN = 40
        ds_freq = to_offset('D')
        GRAIN = 'grain'
        automl_settings[TimeSeries.FREQUENCY] = '2D'
        automl_settings[TimeSeries.TARGET_AGG_FUN] = AggregationFunctions.MIN
        automl_settings[TimeSeries.GRAIN_COLUMN_NAMES] = GRAIN
        automl_settings['n_cross_validations'] = 2
        automl_settings[TimeSeries.MAX_HORIZON] = 2
        dates = pd.date_range('2020-01-01', freq=ds_freq, periods=LEN)
        X_train = pd.DataFrame({
            automl_settings[TimeSeries.TIME_COLUMN_NAME]: dates,
            GRAIN: 'g_1',
            'val': np.arange(LEN),
            TimeSeriesInternal.DUMMY_TARGET_COLUMN: np.arange(LEN)
        })
        X_train = X_train.append(pd.DataFrame({
            automl_settings[TimeSeries.TIME_COLUMN_NAME]: dates,
            GRAIN: 'g_2',
            'val': np.arange(LEN),
            TimeSeriesInternal.DUMMY_TARGET_COLUMN: np.arange(LEN)
        }))
        TEST_LEN = 2 * automl_settings[TimeSeries.MAX_HORIZON]
        X_test = pd.DataFrame({
            automl_settings[TimeSeries.TIME_COLUMN_NAME]: pd.date_range(
                dates.max() + ds_freq, freq=ds_freq, periods=TEST_LEN),
            GRAIN: 'g_1',
            'val': np.arange(40, 40 + TEST_LEN),
            TimeSeriesInternal.DUMMY_TARGET_COLUMN: np.arange(40, 40 + TEST_LEN)
        })
        X_test = X_test.append(pd.DataFrame({
            automl_settings[TimeSeries.TIME_COLUMN_NAME]: pd.date_range(
                dates.max() + ds_freq, freq=ds_freq, periods=TEST_LEN),
            GRAIN: 'g_2',
            'val': np.arange(40, 40 + TEST_LEN),
            TimeSeriesInternal.DUMMY_TARGET_COLUMN: np.arange(40, 40 + TEST_LEN)
        }))
        self._do_test_aggregation_with_lookback(X_train, X_test, automl_settings, False)

    def test_aggregation_with_early_time(self, automl_settings):
        """Test aggregation, when some dates may be aggregated to the latest training point."""
        LEN = 30
        ds_freq = to_offset('D')
        automl_settings[TimeSeries.FREQUENCY] = '2D'
        automl_settings[TimeSeries.TARGET_AGG_FUN] = AggregationFunctions.MIN
        automl_settings[TimeSeries.GRAIN_COLUMN_NAMES] = None
        automl_settings['n_cross_validations'] = 2
        automl_settings[TimeSeries.MAX_HORIZON] = 2
        dates = pd.date_range('2020-01-01', freq=ds_freq, periods=LEN)
        X = pd.DataFrame({
            automl_settings[TimeSeries.TIME_COLUMN_NAME]: dates,
            'val': np.arange(LEN),
        })
        X_train = X[:-5].copy()
        y_train = np.arange(len(X_train))
        X_test = X[-5:].copy()
        automl = self._create_native_client(automl_settings)
        local_run = automl.fit(X=X_train, y=y_train,
                               compute_target='local', show_output=False)
        _, fitted_model = local_run.get_output()
        y_pred, x_pred = fitted_model.forecast(X_test)
        assert_array_equal(y_pred, x_pred[TimeSeriesInternal.DUMMY_TARGET_COLUMN].values)
        assert len(x_pred) == 2
        assert all(not np.isnan(y) for y in y_pred)
        quant = fitted_model.forecast_quantiles(X_test)
        assert len(quant) == 2
        assert all(not np.isnan(y) for y in quant[0.5])

    def test_grains_of_wrong_type_raises(self, automl_settings):
        """Test exception when grain column contains multiple types."""
        GRAIN = 'grain'
        automl_settings[TimeSeries.GRAIN_COLUMN_NAMES] = 'grain'
        automl_settings[TimeSeries.SHORT_SERIES_HANDLING] = True
        automl_settings['n_cross_validations'] = 2
        X_train, y_train, X_test, _ = self.get_simple_grain_data(automl_settings)
        # Make all grains in the training set to be numeric so that
        # the conversion will be impossible.
        X_train[GRAIN] = X_train.apply(
            lambda x: 1 if x[GRAIN] == 'grain1' else 2, axis=1)
        X_intact = X_train.copy()
        X_train[GRAIN] = X_train.apply(
            lambda x: 1 if x[GRAIN] == 1 else pd.Timestamp('2001-01-01'), axis=1)
        X_test[GRAIN] = X_test.apply(
            lambda x: 1 if x[GRAIN] == 'grain1' else pd.Timestamp('2001-01-01'), axis=1)
        automl = self._create_native_client(automl_settings)
        with pytest.raises(ForecastingDataException) as cm:
            automl.fit(X=X_train, y=y_train,
                       compute_target='local', show_output=False)
        assert cm.value._target == 'time_series_id_columns'
        assert cm.value._reference_code == ReferenceCodes._TS_VALIDATION_GRAIN_TYPE_LOCAL
        local_run = automl.fit(X=X_intact, y=y_train,
                               compute_target='local', show_output=False)
        _, fitted_model = local_run.get_output()
        with pytest.raises(ForecastingDataException) as cm:
            fitted_model.forecast(X_test)
        assert cm.value._target == 'time_series_id_columns'
        assert cm.value._reference_code == ReferenceCodes._TS_VALIDATION_GRAIN_TYPE_INFERENCE
        with pytest.raises(ForecastingDataException) as cm:
            fitted_model.forecast_quantiles(X_test)
        assert cm.value._target == 'time_series_id_columns'
        assert cm.value._reference_code == ReferenceCodes._TS_VALIDATION_GRAIN_TYPE_INFERENCE

    def test_grains_of_wrong_type_fixed(self, automl_settings):
        """Test that setting the grain type fixes multiple types of grain column."""
        GRAIN = 'grain'
        automl_settings[TimeSeries.GRAIN_COLUMN_NAMES] = 'grain'
        automl_settings[TimeSeries.SHORT_SERIES_HANDLING] = True
        automl_settings['n_cross_validations'] = 2
        automl_settings['featurization'] = FeaturizationConfig(
            column_purposes={GRAIN: FeatureType.Text})
        X_train, y_train, X_test, _ = self.get_simple_grain_data(automl_settings)
        X_train[GRAIN] = X_train.apply(
            lambda x: 1 if x[GRAIN] == 'grain1' else pd.Timestamp('2001-01-01'), axis=1)
        X_test[GRAIN] = X_test.apply(
            lambda x: 1 if x[GRAIN] == 'grain1' else pd.Timestamp('2001-01-01'), axis=1)
        automl = self._create_native_client(automl_settings)
        local_run = automl.fit(X=X_train, y=y_train,
                               compute_target='local', show_output=False)
        _, fitted_model = local_run.get_output()
        y_pred, x_pred = fitted_model.forecast(X_test)
        assert_array_equal(y_pred, x_pred[TimeSeriesInternal.DUMMY_TARGET_COLUMN].values)
        assert all(not np.isnan(y) for y in y_pred)
        assert len(y_pred) == len(X_test)
        y_quant = fitted_model.forecast_quantiles(X_test)
        assert all(not np.isnan(y) for y in y_quant[0.5])
        assert len(y_quant) == len(X_test)

    def test_grains_of_wrong_type_fixed_valid(self, automl_settings):
        """Test that setting the grain type fixes multiple types of grain column."""
        GRAIN = 'grain'
        automl_settings[TimeSeries.GRAIN_COLUMN_NAMES] = 'grain'
        automl_settings[TimeSeries.SHORT_SERIES_HANDLING] = True
        automl_settings[TimeSeries.TARGET_ROLLING_WINDOW_SIZE] = None
        automl_settings[TimeSeries.TARGET_LAGS] = None
        automl_settings['featurization'] = FeaturizationConfig(
            column_purposes={GRAIN: FeatureType.Categorical})
        X_train, y_train, X_valid, y_valid = self.get_simple_grain_data(automl_settings)
        X_train[GRAIN] = X_train.apply(
            lambda x: 1 if x[GRAIN] == 'grain1' else pd.Timestamp('2001-01-01'), axis=1)
        X_valid[GRAIN] = X_valid.apply(
            lambda x: 1 if x[GRAIN] == 'grain1' else pd.Timestamp('2001-01-01'), axis=1)
        X_test = X_valid.copy()
        ts = X_valid[automl_settings[TimeSeries.TIME_COLUMN_NAME]].max() + to_offset('D')
        X_test[automl_settings[TimeSeries.TIME_COLUMN_NAME]] = pd.date_range(ts, freq='D', periods=len(X_test))
        automl = self._create_native_client(automl_settings)
        local_run = automl.fit(X=X_train, y=y_train, X_valid=X_valid, y_valid=y_valid,
                               compute_target='local', show_output=False)
        _, fitted_model = local_run.get_output()
        y_pred, x_pred = fitted_model.forecast(X_test)
        assert_array_equal(y_pred, x_pred[TimeSeriesInternal.DUMMY_TARGET_COLUMN].values)
        assert all(not np.isnan(y) for y in y_pred)
        assert len(y_pred) == len(X_test)
        y_quant = fitted_model.forecast_quantiles(X_test)
        assert all(not np.isnan(y) for y in y_quant[0.5])
        assert len(y_quant) == len(X_test)

    def test_train_string_valid_categorical(self, automl_settings):
        """Test data sets when trainig set is string and test set is categorical."""
        GRAIN = 'secret_grain'
        automl_settings[TimeSeries.GRAIN_COLUMN_NAMES] = GRAIN
        (X_train, y_train,
         X_valid, y_valid,
         _, _) = self.get_mock_grain_data(automl_settings)
        # Make test and valid categorical.
        X_valid[GRAIN] = pd.Categorical(X_valid[GRAIN])
        automl = self._create_native_client(automl_settings)
        local_run = automl.fit(X=X_train, y=y_train,
                               X_valid=X_valid, y_valid=y_valid,
                               compute_target='local', show_output=False)
        _, fitted_model = local_run.get_output()
        y_pred, x_pred = fitted_model.forecast(X_valid)
        assert_array_equal(y_pred, x_pred[TimeSeriesInternal.DUMMY_TARGET_COLUMN].values)
        assert all(not np.isnan(y) for y in y_pred)
        assert len(y_pred) == len(X_valid)
        y_quant = fitted_model.forecast_quantiles(X_valid)
        assert all(not np.isnan(y) for y in y_quant[0.5])
        assert len(y_quant) == len(X_valid)

    def test_padding_of_dates_and_categoricals(self, automl_settings):
        """Test automl run on short series padding with categorical and date columns."""
        LEN = 4
        automl_settings[TimeSeries.GRAIN_COLUMN_NAMES] = None
        automl_settings[TimeSeries.SHORT_SERIES_HANDLING] = True
        automl_settings[TimeSeries.SHORT_SERIES_HANDLING_CONFIG] = \
            ShortSeriesHandlingValues.SHORT_SERIES_HANDLING_AUTO
        automl_settings[TimeSeries.TARGET_ROLLING_WINDOW_SIZE] = None
        automl_settings[TimeSeries.TARGET_LAGS] = None
        automl_settings[TimeSeries.MAX_HORIZON] = 2
        automl_settings['n_cross_validations'] = 2
        X = pd.DataFrame({
            automl_settings[TimeSeries.TIME_COLUMN_NAME]: pd.date_range('2001-01-01', freq='D', periods=LEN),
            'date_val': pd.date_range('2021-01-01', freq='Y', periods=LEN),
            'text_val': 'a',
            'num_val': 42
        })
        X_train = X[:-automl_settings[TimeSeries.MAX_HORIZON]]
        X_test = X[-automl_settings[TimeSeries.MAX_HORIZON]:]
        y_train = np.array([1, 2])
        automl = self._create_native_client(automl_settings)
        local_run = automl.fit(X=X_train, y=y_train,
                               compute_target='local', show_output=False)
        _, fitted_model = local_run.get_output()
        y_pred, x_pred = fitted_model.forecast(X_test)
        assert_array_equal(y_pred, x_pred[TimeSeriesInternal.DUMMY_TARGET_COLUMN].values)
        assert all(not np.isnan(y) for y in y_pred)
        y_quant = fitted_model.forecast_quantiles(X_test)
        assert all(not np.isnan(y) for y in y_quant[0.5].values)

    def test_padding_dates_and_categoricals_grains(self, automl_settings):
        """Test padding of short series with grains."""
        LEN = 4
        GRAIN = 'grain'
        automl_settings[TimeSeries.GRAIN_COLUMN_NAMES] = GRAIN
        automl_settings[TimeSeries.SHORT_SERIES_HANDLING] = True
        automl_settings[TimeSeries.SHORT_SERIES_HANDLING_CONFIG] = \
            ShortSeriesHandlingValues.SHORT_SERIES_HANDLING_AUTO
        automl_settings[TimeSeries.TARGET_ROLLING_WINDOW_SIZE] = None
        automl_settings[TimeSeries.TARGET_LAGS] = None
        automl_settings[TimeSeries.MAX_HORIZON] = 2
        automl_settings['n_cross_validations'] = 2
        X = pd.DataFrame({
            automl_settings[TimeSeries.TIME_COLUMN_NAME]: pd.date_range('2001-01-01', freq='D', periods=LEN),
            GRAIN: 1,
            'date_val': pd.date_range('2021-01-01', freq='Y', periods=LEN),
            'text_val': 'a',
            'num_val': 42
        })
        X = X.append(pd.DataFrame({
            automl_settings[TimeSeries.TIME_COLUMN_NAME]: pd.date_range('2002-01-01', freq='D', periods=LEN),
            GRAIN: 2,
            'date_val': pd.date_range('2020-01-01', freq='Y', periods=LEN),
            'text_val': 'b',
            'num_val': 77
        }))
        X_train, X_test = self.split_last_n_by_grain(X, automl_settings[TimeSeries.MAX_HORIZON], automl_settings)
        y_train = np.array([1, 2, 1, 2])
        automl = self._create_native_client(automl_settings)
        local_run = automl.fit(X=X_train, y=y_train,
                               compute_target='local', show_output=False)
        _, fitted_model = local_run.get_output()
        y_pred, x_pred = fitted_model.forecast(X_test)
        assert_array_equal(y_pred, x_pred[TimeSeriesInternal.DUMMY_TARGET_COLUMN].values)
        assert all(not np.isnan(y) for y in y_pred)
        y_quant = fitted_model.forecast_quantiles(X_test)
        assert all(not np.isnan(y) for y in y_quant[0.5].values)

    def test_padding_of_dates_all_nan(self, automl_settings):
        """Test automl run on short series padding with categorical and date columns."""
        LEN = 4
        automl_settings[TimeSeries.GRAIN_COLUMN_NAMES] = None
        automl_settings[TimeSeries.SHORT_SERIES_HANDLING] = True
        automl_settings[TimeSeries.SHORT_SERIES_HANDLING_CONFIG] = \
            ShortSeriesHandlingValues.SHORT_SERIES_HANDLING_AUTO
        automl_settings[TimeSeries.TARGET_ROLLING_WINDOW_SIZE] = None
        automl_settings[TimeSeries.TARGET_LAGS] = None
        automl_settings[TimeSeries.MAX_HORIZON] = 2
        automl_settings['n_cross_validations'] = 2
        X = pd.DataFrame({
            automl_settings[TimeSeries.TIME_COLUMN_NAME]: pd.date_range('2001-01-01', freq='D', periods=LEN),
            'date_val': pd.NaT,
            'text_val': 'a',
            'num_val': 42
        })
        X_train = X[:-automl_settings[TimeSeries.MAX_HORIZON]]
        X_test = X[-automl_settings[TimeSeries.MAX_HORIZON]:]
        y_train = np.array([1, 2])
        automl = self._create_native_client(automl_settings)
        local_run = automl.fit(X=X_train, y=y_train,
                               compute_target='local', show_output=False)
        _, fitted_model = local_run.get_output()
        y_pred, x_pred = fitted_model.forecast(X_test)
        assert_array_equal(y_pred, x_pred[TimeSeriesInternal.DUMMY_TARGET_COLUMN].values)
        assert all(not np.isnan(y) for y in y_pred)
        y_quant = fitted_model.forecast_quantiles(X_test)
        assert all(not np.isnan(y) for y in y_quant[0.5].values)

    def _do_forecast_on_data_with_singular_grain_and_heuristics(self, automl_settings):
        """Do the actual test"""
        automl_settings[TimeSeries.GRAIN_COLUMN_NAMES] = 'grain'
        automl_settings[TimeSeries.TARGET_ROLLING_WINDOW_SIZE] = 'auto'
        automl_settings[TimeSeries.TARGET_LAGS] = 'auto'
        automl_settings[TimeSeries.MAX_HORIZON] = 1
        automl_settings['n_cross_validations'] = 2
        X_train = pd.DataFrame({
            automl_settings[TimeSeries.TIME_COLUMN_NAME]: pd.date_range('2001-01-01', freq='D', periods=30),
            'grain': 'good',
            'y': np.arange(30)
        })
        X_train = X_train.append(pd.DataFrame([[pd.Timestamp('2001-01-01'), 'bad', 42]],
                                              columns=[automl_settings[TimeSeries.TIME_COLUMN_NAME], 'grain',
                                                       'y']))
        y_train = X_train.pop('y').values
        X_test = pd.DataFrame([[pd.Timestamp('2001-01-31'), 'good'],
                               [pd.Timestamp('2001-01-02'), 'bad']],
                              columns=[automl_settings[TimeSeries.TIME_COLUMN_NAME], 'grain'])
        automl = self._create_native_client(automl_settings)
        local_run = automl.fit(X=X_train, y=y_train,
                               compute_target='local', show_output=False)
        _, fitted_model = local_run.get_output()
        y_pred, x_pred = fitted_model.forecast(X_test)
        assert_array_equal(y_pred, x_pred[TimeSeriesInternal.DUMMY_TARGET_COLUMN].values)
        y_quant = fitted_model.forecast_quantiles(X_test)
        assert_array_equal(y_pred, y_quant[0.5].values)
        assert len(y_pred) == len(X_test)
        if automl_settings[TimeSeries.SHORT_SERIES_HANDLING_CONFIG] ==\
                ShortSeriesHandlingValues.SHORT_SERIES_HANDLING_PAD:
            assert all(not np.isnan(y_pr) for y_pr in y_pred)
        else:
            x_pred.reset_index(inplace=True, drop=False)
            assert all(np.isnan(y_pr)
                       for y_pr in x_pred[x_pred['grain'] == 'bad'][TimeSeriesInternal.DUMMY_TARGET_COLUMN])
            assert all(not np.isnan(y_pr)
                       for y_pr in x_pred[x_pred['grain'] != 'bad'][TimeSeriesInternal.DUMMY_TARGET_COLUMN])

    def test_forecast_on_data_with_singular_grain_and_heuristics_auto(self, automl_settings):
        """Test heuristic settings on data set where there is one point in a grain."""
        automl_settings[TimeSeries.SHORT_SERIES_HANDLING] = True
        automl_settings[TimeSeries.SHORT_SERIES_HANDLING_CONFIG] = \
            ShortSeriesHandlingValues.SHORT_SERIES_HANDLING_AUTO
        self._do_forecast_on_data_with_singular_grain_and_heuristics(automl_settings)

    def test_forecast_on_data_with_singular_grain_and_heuristics_pad(self, automl_settings):
        """Test heuristic settings on data set where there is one point in a grain."""
        automl_settings[TimeSeries.SHORT_SERIES_HANDLING] = True
        automl_settings[TimeSeries.SHORT_SERIES_HANDLING_CONFIG] = \
            ShortSeriesHandlingValues.SHORT_SERIES_HANDLING_PAD
        self._do_forecast_on_data_with_singular_grain_and_heuristics(automl_settings)

    def test_forecast_on_data_with_singular_grain_and_heuristics_drop(self, automl_settings):
        """Test heuristic settings on data set where there is one point in a grain."""
        automl_settings[TimeSeries.SHORT_SERIES_HANDLING] = True
        automl_settings[TimeSeries.SHORT_SERIES_HANDLING_CONFIG] = \
            ShortSeriesHandlingValues.SHORT_SERIES_HANDLING_DROP
        self._do_forecast_on_data_with_singular_grain_and_heuristics(automl_settings)

    def test_compatible_frequencies_train_valid(self, automl_settings):
        """Test we are not failing on compatible frequencies."""
        automl_settings[TimeSeries.GRAIN_COLUMN_NAMES] = None
        automl_settings[TimeSeries.TARGET_ROLLING_WINDOW_SIZE] = None
        automl_settings[TimeSeries.TARGET_LAGS] = None
        automl_settings[TimeSeries.MAX_HORIZON] = 4
        X_train = pd.DataFrame({
            automl_settings[TimeSeries.TIME_COLUMN_NAME]: pd.date_range('2001-01-01', freq='D', periods=30),
            'y': np.arange(30)
        })
        y_train = X_train.pop('y').values
        X_valid = pd.DataFrame({
            automl_settings[TimeSeries.TIME_COLUMN_NAME]: pd.date_range('2001-01-31', freq='2D', periods=4),
            'y': np.arange(4)
        })
        y_valid = X_valid.pop('y').values
        automl = self._create_native_client(automl_settings)
        local_run = automl.fit(X=X_train, y=y_train, X_valid=X_valid, y_valid=y_valid,
                               compute_target='local', show_output=False)
        _, fitted_model = local_run.get_output()
        y_pred, x_pred = fitted_model.forecast(X_valid)
        assert all(not np.isnan(y) for y in y_pred)
        assert_array_equal(y_pred, x_pred[TimeSeriesInternal.DUMMY_TARGET_COLUMN].values)
        assert_array_equal(x_pred.index.get_level_values(automl_settings[TimeSeries.TIME_COLUMN_NAME]).values,
                           X_valid[automl_settings[TimeSeries.TIME_COLUMN_NAME]].values)

    def test_train_valid_user_freq(self, automl_settings):
        """Test that if user set frequency, we are checking compliance with it as opposed to detected one."""
        automl_settings[TimeSeries.GRAIN_COLUMN_NAMES] = None
        automl_settings[TimeSeries.TARGET_ROLLING_WINDOW_SIZE] = None
        automl_settings[TimeSeries.TARGET_LAGS] = None
        automl_settings[TimeSeries.MAX_HORIZON] = 4
        automl_settings[TimeSeries.FREQUENCY] = 'D'
        X_train = pd.DataFrame({
            "date": pd.date_range('2001-01-01', freq='2D', periods=20),
            "y": np.arange(20)
        })
        start = X_train['date'].max() + to_offset('D')
        X_valid = pd.DataFrame({
            "date": pd.date_range(start, freq='3D', periods=4),
            "y": np.arange(4)
        })
        y_train = X_train.pop('y').values
        y_valid = X_valid.pop('y').values
        automl = self._create_native_client(automl_settings)
        local_run = automl.fit(X=X_train, y=y_train, X_valid=X_valid, y_valid=y_valid,
                               compute_target='local', show_output=False)
        _, fitted_model = local_run.get_output()
        y_pred, x_pred = fitted_model.forecast(X_valid)
        assert all(not np.isnan(y) for y in y_pred)
        assert_array_equal(y_pred, x_pred[TimeSeriesInternal.DUMMY_TARGET_COLUMN].values)
        assert_array_equal(x_pred.index.get_level_values(automl_settings[TimeSeries.TIME_COLUMN_NAME]).values,
                           X_valid[automl_settings[TimeSeries.TIME_COLUMN_NAME]].values)

    def get_mock_grain_data(self, settings):
        """Return the mock data with horizont = 1."""
        data_dict = {
            'date': pd.date_range("2011-01-01", "2011-01-18"),
            'is_raining': [1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1],
            'temperature': [10, 20, 30, 40, 10, 20, 30, 40, 30, 20, 10, 15, 30, 20, 10, 15, 145, 28],
        }
        y_train = np.array([15, 1, 11, 14, 10, 4, 3, 14] * 2)
        y_valid = np.array([4, 2, 13, 19, 1] * 2)
        y_test = np.array([10, 15, 12, 13, 5] * 2)
        df = pd.DataFrame(data_dict)
        df = pd.concat([df.assign(**{settings[TimeSeries.GRAIN_COLUMN_NAMES]: np.repeat('grain1', 18)}),
                        df.assign(**{settings[TimeSeries.GRAIN_COLUMN_NAMES]: np.repeat('grain2', 18)})])
        df_tv, X_test = self.split_last_n_by_grain(df, 5, settings)
        X_train, X_valid = self.split_last_n_by_grain(df_tv, 5, settings)
        return (X_train, y_train,
                X_valid, y_valid,
                X_test, y_test)

    def get_stationary_data(self, size):
        np.random.seed(10)
        y_ = (10 * np.random.uniform(-1, 1, [size])).astype(np.int64)
        mu = 10
        sigma = 0.01
        e = np.random.normal(mu, sigma, size).astype(np.int64)
        y = y_ + e
        return y

    def get_simple_grain_data(self, settings, ntest=5, total_sz=42, is_stationary=True):
        """Return the mock data with horizont = 1."""
        data_dict = {
            'date': pd.date_range("2011-01-01", freq='D', periods=total_sz),
            'is_raining': np.repeat(1, total_sz),
            'temperature': np.arange(30, 30 + total_sz),
            'some_bool': True
        }
        train_sz = total_sz - ntest
        if is_stationary:
            y = self.get_stationary_data(total_sz)
            y_train = np.array(list(y[0:train_sz]) * 2)
            y_test = np.array(list(y[train_sz:]) * 2)
        else:
            y_train = np.array(list(np.arange(train_sz)) * 2)
            y_test = np.array(list(np.arange(train_sz, train_sz + 5)) * 2)

        df = pd.DataFrame(data_dict)
        df = pd.concat([df.assign(**{settings[TimeSeries.GRAIN_COLUMN_NAMES]: np.repeat('grain1', total_sz)}),
                        df.assign(**{settings[TimeSeries.GRAIN_COLUMN_NAMES]: np.repeat('grain2', total_sz)})])
        X_train, X_test = self.split_last_n_by_grain(df, ntest, settings)
        return (X_train, y_train,
                X_test, y_test)

    def get_mock_data(self, settings, max_horizon, ntest=5, nvalidate=5):
        """
        Return the mock data frames to test LagLeadOperator and RollingWindow.

        :returns: The tuple of train and test data frames.
                  **Note:** Test data frame contains only columns created by
                  common featurizers like TimeSeriesImputer.
        :rtype: tuple

        """
        target_column_name = 'target'
        data_dict = {
            'date': pd.date_range("2011-01-01", "2011-01-18"),
            'is_raining': [1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1],
            'temperature': [10, 20, 30, 40, 10, 20, 30, 40, 30, 20, 10, 15, 30, 20, 10, 15, 145, 28],
            target_column_name: [15, 1, 11, 14, 10, 4, 3, 14, 4, 2, 13, 19, 1, 10, 15, 12, 13, 5]
        }
        df = pd.DataFrame(data_dict)
        df_tv, X_test = self.split_last_n_by_grain(df, ntest, settings)
        X_train, X_validate = self.split_last_n_by_grain(df_tv, nvalidate, settings)
        y_train = X_train.pop(target_column_name).values
        y_validate = X_validate.pop(target_column_name).values
        y_test = X_test.pop(target_column_name).values
        return (X_train, y_train,
                X_validate, y_validate,
                X_test, y_test)

    def split_last_n_by_grain(self, df, n, settings):
        """
        Group df by grain and split on last n rows for each group
        """
        if settings[TimeSeries.GRAIN_COLUMN_NAMES]:
            df_grouped = (df.sort_values(settings[TimeSeries.TIME_COLUMN_NAME])  # Sort by ascending time
                          .groupby(settings[TimeSeries.GRAIN_COLUMN_NAMES], group_keys=False))
        else:
            df_grouped = df.sort_values(settings[TimeSeries.TIME_COLUMN_NAME])
        df_head = df_grouped.apply(lambda dfg: dfg.iloc[:-n])
        df_tail = df_grouped.apply(lambda dfg: dfg.iloc[-n:])
        return df_head, df_tail

    def _create_native_client(self, settings):
        """Create mock native client."""
        automl = AutoMLNativeClient(workspace=DummyWorkspace())
        automl.initialize_client(**settings)
        native_client_patch_forecast_provider(automl)
        return automl

    def test_timeseries_with_only_date_column(self):
        x, y = load_diabetes(return_X_y=True)
        X_train, X_valid, y_train, y_valid = train_test_split(x,
                                                              y,
                                                              test_size=0.2,
                                                              random_state=0)
        date_column_name = "date"
        nrows_train, ncols_train = X_train.shape
        nrows_test, ncols_test = X_valid.shape
        column_names = [str(i) for i in range(ncols_train)]
        X_train = pd.DataFrame(X_train, columns=column_names)
        X_valid = pd.DataFrame(X_valid, columns=column_names)
        time_axis = pd.date_range('1980-01-01', periods=(nrows_train + nrows_test), freq='D')
        X_train[date_column_name] = time_axis[:nrows_train]
        X_valid[date_column_name] = time_axis[nrows_train:]
        X_train = X_train[[date_column_name]]
        X_valid = X_valid[[date_column_name]]
        featurization = FeaturizationConfig(blocked_transformers=['TimeIndexFeaturizer'])
        automl_settings = {
            "iterations": 3,
            "primary_metric": 'normalized_root_mean_squared_error',
            'task_type': constants.Tasks.REGRESSION,
            'n_cross_validations': None,
            'debug_flag': {'service_url': 'url'},
            'debug_log': 'automl_tests.log',
            'is_timeseries': True,
            'iteration_timeout_minutes': None,
            TimeSeries.TIME_COLUMN_NAME: 'date',
            'featurization': featurization,
        }
        automl = self._create_native_client(automl_settings)
        local_run = automl.fit(X=X_train, y=y_train,
                               X_valid=X_valid, y_valid=y_valid,
                               compute_target='local', show_output=False)
        scores, fitted_model = local_run.get_output()
        y_pred, x_pred = fitted_model.forecast(X_valid)
        assert not any(np.isnan(y) for y in y_pred)
        assert_array_equal(y_pred, x_pred[TimeSeriesInternal.DUMMY_TARGET_COLUMN].values)
        assert len(y_pred) == X_valid.shape[0], "Wrong number of predictions."


if __name__ == "__main__":
    pytest.main(['-x', '-n', 'auto', '-k', os.path.basename(__file__)])
