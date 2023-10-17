"""Common variables."""
import os

server_url = None

active_run_stack = []
active_experiment_name = None

EXPERIMENT_NAME_FOR_EXECUTOR = "executors"
EXPERIMENT_NAME_FOR_DATASET_LOADER = "dataset_loaders"


def _get_server_ml_api() -> str:
    """Get server '/mlflow' endpoint URL."""
    return os.path.join(_get_server_url(), "mlflow")


def _get_server_url() -> str:
    """
    Get server URL.

    If you set the URL using 'mlmanagement.set_server_url' function,
    it takes precedence over the URL from the environment variable 'server_url'
    """
    return os.environ.get("server_url", "http://mlmanagement.ru") if not server_url else server_url
