# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from mlflow.exceptions import MlflowException


class AzureMLMLFlowException(MlflowException):

    def __init__(self, message, **kwargs):
        super().__init__(message, **kwargs)
