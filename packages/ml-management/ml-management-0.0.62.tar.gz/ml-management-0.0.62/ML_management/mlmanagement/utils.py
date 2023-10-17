"""Functions for internal usage."""
import inspect

from ML_management.mlmanagement import mlmanagement
from ML_management.mlmanagement.mlmanager import request_for_function

import mlflow


def _load_model_type(run_id, unwrap: bool = True):
    """Load model from local path."""
    local_path = mlmanagement.MlflowClient().download_artifacts(run_id, "")
    loaded_model = mlflow.pyfunc.load_model(local_path)
    if unwrap:
        artifacts_dict = loaded_model._model_impl.context._artifacts
        loaded_model = loaded_model.unwrap_python_model()
        loaded_model.artifacts = artifacts_dict
    return loaded_model


def _add_eval_run(run_id: str):
    """Set the active run as the eval run for the model with 'run_id'."""
    return request_for_function(inspect.currentframe())
