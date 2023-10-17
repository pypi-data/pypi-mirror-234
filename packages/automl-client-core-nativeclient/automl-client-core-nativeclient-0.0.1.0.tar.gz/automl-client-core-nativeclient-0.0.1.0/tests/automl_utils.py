import json
import os
import urllib3
import uuid

import adal
import numpy as np
import pandas as pd

from azureml.automl.core.shared import constants


os.environ['CURL_CA_BUNDLE'] = ''
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def _get_y_for_timeseries(fitted_model, X_test):
    # If the model is a time series then output
    # y_pred will not have the same dimension as
    # y_test. We need to change the y_pred dimension in this case.
    y_pred = fitted_model.predict(X_test)
    if len(y_pred) == X_test.shape[0]:
        return y_pred
    # Generate transformed X_test for data analysis.
    X_test = X_test.copy()
    X_test[constants.TimeSeriesInternal.DUMMY_TARGET_COLUMN] = np.NaN
    X_transformed = fitted_model.steps[0][1].transform(X_test)
    lst_index = list(X_transformed.index.names)[:len(X_transformed.index.names) - 1]
    df_clean = clean_up_x_values(X_transformed, y_pred)
    # Sort input values by the X_test.
    df_clean.reset_index(inplace=True, drop=False)
    X_transformed.reset_index(inplace=True, drop=False)
    for col in lst_index:
        df_clean[col] = df_clean[col].astype(X_transformed[col].dtype)
    X_test.drop(constants.TimeSeriesInternal.DUMMY_TARGET_COLUMN, axis=1, inplace=True)
    # Grain column may or may not be in X_test
    if constants.TimeSeriesInternal.DUMMY_GRAIN_COLUMN in lst_index:
        del lst_index[lst_index.index(constants.TimeSeriesInternal.DUMMY_GRAIN_COLUMN)]
    df_clean = X_test[lst_index].merge(df_clean, how='left', on=lst_index, left_index=False, right_index=False)
    return df_clean.pop(constants.TimeSeriesInternal.DUMMY_TARGET_COLUMN).values.astype('float')


def clean_up_y_values(X_transformed, y):
    """
    Return the y values corresponding only to the latest origin dates

    :param X_transformed: The trans formed data frame.
    :type X: pd.DataFrame
    :param y: The predicted array, having the same size as X_transformed.
    :type y: np.array
    :returns: the corrected array of y.
    :rtype: np.array

    """

    df_clean = clean_up_x_values(X_transformed, y)
    y_pred = df_clean.pop(constants.TimeSeriesInternal.DUMMY_TARGET_COLUMN).values
    return y_pred


def clean_up_x_values(X_transformed, y):
    """
    Return the data frame corresponding only to the latest origin dates

    :param X_transformed: The transformed data frame.
    :type X: pd.DataFrame
    :param y: The predicted array, having the same size as X_transformed.
    :type y: np.array
    :returns: the corrected array of y.
    :rtype: pd.DataFrame

    """
    X_transformed[constants.TimeSeriesInternal.DUMMY_TARGET_COLUMN] = y
    # For each date we need to get the latest origin.
    series = _get_latest_origins(X_transformed)
    df_clean = pd.DataFrame(pd.concat(series, axis=1)).transpose()
    # Sort y values by the order of input.
    lst_index = list(X_transformed.index.names)[:len(X_transformed.index.names) - 1]
    df_clean.set_index(lst_index, inplace=True)
    return df_clean


def _get_latest_origins(X):
    """
    Return series, containing the latest origin.

    If X contains only index, filter by it and return the
    series for the latest data frame.
    :param X: The data frame to return the latest origin from.
    :type X: pd.DataFrame
    :returns: The array of series with latest data frame.
    :rtype: list<pd.Series>

    """
    series_to_return = []
    if isinstance(X.index, pd.MultiIndex):
        for index in X.index.levels[0]:
            try:
                df_subindex = X.loc[index]
            except KeyError:
                continue
            if df_subindex.shape[0] == 0:
                continue
            df_subindex[X.index.names[0]] = index
            series_to_return += _get_latest_origins(df_subindex)
    # The last index is origin.
    elif isinstance(X.index, pd.Index):
        max_date = max(X.index.values)
        series_to_return.append(X.loc[max_date])
    return series_to_return


def load_config():
    config_file_path = os.path.join(
        os.path.dirname(__file__),
        'e2e_config.json')
    with open(config_file_path, 'r') as config_file:
        return json.load(config_file)


class MiroProxyAuthentication:
    def __init__(self, configs):
        import os
        self._sp_key = os.environ.get('automl_sp_key')
        self._authority_url = configs['authority_host_url'] + \
            '/' + configs['automl_service_principal_tenant']
        self._resource_url = configs['resource_url']
        self._client_id = configs['automl_service_principal_id']

    def get_authentication_header(self):
        context = adal.AuthenticationContext(
            self._authority_url, api_version=None)
        mgmt_token = context.acquire_token_with_client_credentials(
            self._resource_url, self._client_id, self._sp_key)
        auth_header = {"Authorization": "Bearer " + mgmt_token['accessToken']}
        return auth_header
