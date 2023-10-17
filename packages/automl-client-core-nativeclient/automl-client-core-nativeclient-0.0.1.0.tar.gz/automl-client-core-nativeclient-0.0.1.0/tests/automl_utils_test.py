import unittest
import pandas as pd
import numpy as np

from automl_utils import clean_up_y_values, _get_y_for_timeseries
from numpy.ma.testutils import assert_array_equal
from unittest.mock import Mock, MagicMock
from azureml.automl.core.shared.constants import TimeSeriesInternal


class AutoMlFcTest(unittest.TestCase):
    """Test for cleaning of data frame origins in the AutoMlTest."""

    GRAIN_DF = pd.DataFrame({
        'date': pd.to_datetime(['2019-01-01'] * 8 + ['2019-01-02'] * 7 + ['2019-01-03'] * 2),
        'grain_col1': list(np.repeat(['1', '2'], 4)) + ['1'] * 4 + ['2'] * 3 + ['1', '2'],
        'grain_col2': ['a', 'a', 'b', 'b'] * 3 + ['a', 'a', 'b'] + ['a', 'b'],
        'origin': pd.to_datetime(['2018-12-30', '2018-12-31'] * 4 +
                                 ['2018-12-31', '2019-01-01'] * 3 +
                                 ['2018-12-31'] + ['2019-01-02'] * 2),
        'y': np.arange(17)
    })

    def test_clean_data_frame(self):
        """Test if data frame is clean with grains."""
        data = AutoMlFcTest.GRAIN_DF.copy()
        data.set_index(['date', 'grain_col1', 'grain_col2', 'origin'], inplace=True)
        data.sort_index(inplace=True)
        y_test = data.pop('y').values
        y_clean = clean_up_y_values(data, y_test)
        assert_array_equal(y_clean, np.array([1, 3, 5, 7, 9, 11, 13, 14, 15, 16]))

    def test_no_grains(self):
        """Test if the data frame is clean without grains."""
        data = pd.DataFrame({
                            'date': pd.to_datetime(['2019-01-01'] * 4 + ['2019-01-02'] * 3 +
                                                   ['2019-01-03'] * 2 + ['2019-01-04']),
                            'grain': np.repeat('a', 10),
                            'origin': pd.to_datetime(['2018-12-28', '2018-12-29', '2018-12-30', '2018-12-31'] +
                                                     ['2018-12-30', '2018-12-31', '2019-01-01'] +
                                                     ['2019-01-01', '2019-01-02'] + ['2019-01-03']),
                            'y': np.arange(10)
                            })
        data.set_index(['date', 'grain', 'origin'], inplace=True)
        data.sort_index(inplace=True)
        y_test = data.pop('y').values
        y_clean = clean_up_y_values(data, y_test)
        assert_array_equal(y_clean, np.array([3, 6, 8, 9]))

    def test_get_y_for_timeseries(self):
        """Test that data obtained from the model are cleaned correctly."""
        data = AutoMlFcTest.GRAIN_DF.copy()
        data.set_index(['date', 'grain_col1', 'grain_col2', 'origin'], inplace=True)
        y = data['y'].astype('float').values
        y += 0.000000001
        data['y'] = y
        data.sort_index(inplace=True)
        test_data = pd.DataFrame({
            'date': pd.to_datetime(['2019-01-01'] * 4 + ['2019-01-02'] * 4 + ['2019-01-03'] * 2),
            'grain_col1': list(np.repeat(['1', '2'], 2)) * 2 + ['1', '2'],
            'grain_col2': ['a', 'b'] * 5,
            'y': np.array([1., 3., 5., 7., 9., 11., 13., 14., 15., 16.]) + 0.000000001
        })
        test_data.set_index(['date', 'grain_col1', 'grain_col2'], inplace=True)
        test_data.sort_index(inplace=True)

        def do_test(X_test, y_test):
            fitted_model = Mock()
            fitted_model.predict = MagicMock(return_value=data['y'].values)
            mock_ts_transform = Mock()
            mock_ts_transform.transform = MagicMock(return_value=data.copy())
            fitted_model.steps = [('mock_ts', mock_ts_transform)]
            y_pred = _get_y_for_timeseries(fitted_model, X_test)
            assert_array_equal(y_test, y_pred, 'Unexpected array was returned.')

        X_test = test_data.reset_index(drop=False, inplace=False)
        y_test = X_test.pop('y').values
        do_test(X_test, y_test)
        X_test = test_data.reset_index(drop=False, inplace=False)
        X_test = X_test.sample(frac=1, random_state=42)
        y_test = X_test.pop('y').values
        do_test(X_test, y_test)

    def test_get_y_no_grains(self):
        """Test if the data frame is clean without grains."""
        data = pd.DataFrame({
                            'date': pd.to_datetime(['2019-01-01'] * 4 + ['2019-01-02'] * 3 +
                                                   ['2019-01-03'] * 2 + ['2019-01-04']),
                            TimeSeriesInternal.DUMMY_GRAIN_COLUMN: TimeSeriesInternal.DUMMY_GRAIN_COLUMN,
                            'origin': pd.to_datetime(['2018-12-28', '2018-12-29', '2018-12-30', '2018-12-31'] +
                                                     ['2018-12-30', '2018-12-31', '2019-01-01'] +
                                                     ['2019-01-01', '2019-01-02'] + ['2019-01-03']),
                            'y': np.arange(10)
                            })
        test_data = pd.DataFrame({
            'date': pd.to_datetime(['2019-01-01', '2019-01-02', '2019-01-03', '2019-01-04']),
            'y': np.array([3, 6, 8, 9])
        })
        data.set_index(['date', TimeSeriesInternal.DUMMY_GRAIN_COLUMN, 'origin'], inplace=True)
        data.sort_index(inplace=True)
        fitted_model = Mock()
        fitted_model.predict = MagicMock(return_value=data['y'].values)
        mock_ts_transform = Mock()
        mock_ts_transform.transform = MagicMock(return_value=data.copy())
        fitted_model.steps = [('mock_ts', mock_ts_transform)]
        y_pred = _get_y_for_timeseries(fitted_model, test_data)
        assert_array_equal(test_data['y'].values, y_pred, 'Unexpected array was returned.')


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
