# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Constants for azureml-evaluate-mlflow"""


class ForecastFlavors:
    """The constants for forecast flavors."""

    # The parameter name
    FLAVOUR = "forecast_flavour"
    # Flavors
    RECURSIVE_FORECAST = "forecast"
    ROLLING_FORECAST = "rolling_forecast"

    ALL = {RECURSIVE_FORECAST, ROLLING_FORECAST}


class ForecastColumns:
    """The columns, returned in the forecast data frame."""

    _ACTUAL_COLUMN_NAME = '_automl_actual'
    _FORECAST_COLUMN_NAME = '_automl_forecast'
