"""
Mlflow server inside ML_management.

ML_manager sends request to our server on /mlflow endpoint
Server calls original mlflow function accordingly
"""
import atexit
import inspect
import io
import os
import subprocess
import sys
import tempfile
import traceback
import zipfile
from typing import Any, Dict, List, Optional, Union

import cloudpickle
import numpy
import pandas
from ML_management.executor_template.upload_model_mode import UploadModelMode
from ML_management.mlmanagement import variables
from ML_management.mlmanagement.abstract_mlflow_client import AbstractMlflowClient
from ML_management.mlmanagement.mlmanager import request_for_function
from ML_management.mlmanagement.model_type import ModelType
from ML_management.mlmanagement.module_finder import ModuleFinder
from ML_management.mlmanagement.server_mlmanager_exceptions import ModelTypeIsNotFound
from ML_management.mlmanagement.utils import _load_model_type
from ML_management.mlmanagement.variables import active_run_stack
from mlflow.entities import Experiment, Run, RunStatus
from mlflow.entities.model_registry import ModelVersion, RegisteredModel
from mlflow.models import Model
from mlflow.store.entities import PagedList
from mlflow.tracking.fluent import _RUN_ID_ENV_VAR
from mlflow.utils import env
from scipy.sparse import csc_matrix, csr_matrix

import mlflow
from mlflow import ActiveRun


def monkey_patching_exit(self, exc_type, exc_val, exc_tb):
    """Redefine __exit__ function of class ActiveRun."""
    status = RunStatus.FINISHED if exc_type is None else RunStatus.FAILED
    end_run(RunStatus.to_string(status))
    return exc_type is None


# Rewrite __exit__ method to enable using Python ``with`` syntax of ActiveRun class.
ActiveRun.__exit__ = monkey_patching_exit


def start_run_if_not_exist():
    """If run doesn't exist call start_run() function."""
    if len(active_run_stack) == 0:
        start_run()


def set_experiment(experiment_name: Optional[str] = None, experiment_id: Optional[str] = None) -> Experiment:
    """
    Set the given experiment as the active experiment.

    The experiment must either be specified by name via
    experiment_name or by ID via experiment_id. The experiment name and ID cannot both be specified.
    Set global variable active_experiment_name to that experiment_name.
    """
    request_for_function(inspect.currentframe())
    variables.active_experiment_name = experiment_name


def get_experiment_by_name(name: str) -> Optional[Experiment]:
    """Retrieve an experiment by experiment name from the backend store."""
    return request_for_function(inspect.currentframe())


def search_runs(
    experiment_ids: Optional[List[str]] = None,
    filter_string: str = "",
    run_view_type: int = 1,
    max_results: int = 100000,
    order_by: Optional[List[str]] = None,
    output_format: str = "pandas",
    search_all_experiments: bool = False,
    experiment_names: Optional[List[str]] = None,
) -> Union[List[Run], "pandas.DataFrame"]:
    """Search experiments that fit the search criteria."""
    return request_for_function(inspect.currentframe())


def start_run(
    run_id: Optional[str] = None,
    experiment_id: Optional[str] = None,
    run_name: Optional[str] = None,
    nested: bool = False,
    tags: Optional[Dict[str, Any]] = None,
    description: Optional[str] = None,
) -> ActiveRun:
    """
    Start a new MLflow run, setting it as the active run under which metrics and parameters will be logged.

    The return value can be used as a context manager within a with block; otherwise, you must call end_run() to
    terminate the current run.
    If you pass a run_id or the MLFLOW_RUN_ID environment variable is set, start_run attempts to resume a run with
    the specified run ID and other parameters are ignored. run_id takes precedence over MLFLOW_RUN_ID.
    If resuming an existing run, the run status is set to RunStatus.RUNNING.
    Add that created run to active_run_stack.
    """
    if len(active_run_stack) > 0 and not nested:
        raise Exception(
            (
                "Run with UUID {} is already active. To start a new run, first end the "
                + "current run with mlmanagement.end_run(). To start a nested "
                + "run, call start_run with nested=True"
            ).format(active_run_stack[0].info.run_id)
        )
    _active_run = request_for_function(inspect.currentframe())
    active_run_stack.append(_active_run)
    return _active_run


def _add_job_registration_metainfo(
    registration_timestamp,
    init_model_version_run_id,
    dataset_loader_version_run_id,
    executor_version_run_id,
    name,
    job_executor_name,
    job_executor_version,
    dataset_loader_name,
    dataset_loader_version,
    model_name,
    model_version,
    new_model_name,
    experiment_name,
    periodic_type,
    cron_expression,
    metric_name,
    optimal_min,
    choice_criteria,
    executor_model_params_json,
    data_params_json,
    collector_name,
    gpu,
):
    """Add job metainfo on job registration. For internal use only."""
    return request_for_function(inspect.currentframe())


def _add_job_start_metainfo(
    job_name,
    start_timestamp,
):
    """Add job metainfo on execution start. For internal use only."""
    return request_for_function(inspect.currentframe())


def _add_job_end_metainfo(
    job_name,
    end_timestamp,
):
    """Add job metainfo on execution end. For internal use only."""
    return request_for_function(inspect.currentframe())


def _add_job_fail_metainfo(
    job_name,
    end_timestamp,
):
    """Add job metainfo on execution fail. For internal use only."""
    return request_for_function(inspect.currentframe())


def log_model(
    artifact_path,
    loader_module=None,
    data_path=None,
    code_path=None,
    conda_env=None,
    python_model=None,
    artifacts=None,
    registered_model_name="default_name",
    signature: mlflow.models.signature.ModelSignature = None,
    input_example: Union[pandas.core.frame.DataFrame, numpy.ndarray, dict, list, csr_matrix, csc_matrix, str, bytes] = None,
    await_registration_for=300,
    pip_requirements=None,
    extra_pip_requirements=None,
    metadata=None,
    source_model_name=None,
    source_model_version=None,
    upload_model_mode=None,
    visibility=None,
    extra_modules_names=None,
    used_modules_names=None,
    root_module_name: str = "__main__",
):
    """
    Log a Pyfunc model with custom inference logic and optional data dependencies as an MLflow artifact.

    Current run is using.
    You cannot specify the parameters: loader_module, data_path and the parameters: python_model, artifacts together.
    """
    if extra_modules_names and used_modules_names:
        raise RuntimeError("Parameters 'extra_modules_names' and 'used_modules_names' cannot be used at the same time.")
    if upload_model_mode == UploadModelMode.none:
        raise RuntimeError("You can't log a model using the 'upload_model_mode' parameter set to none.")
    start_run_if_not_exist()
    if used_modules_names is not None:
        submodules = set(used_modules_names)
        ModuleFinder.import_modules_by_name(submodules)
    else:
        submodules = ModuleFinder().find_root_submodules(root_name=root_module_name)
        if extra_modules_names:
            extra_set = set(extra_modules_names)
            ModuleFinder.import_modules_by_name(extra_set)
            submodules = submodules.union(extra_set)
    try:
        for module_name in submodules:
            cloudpickle.register_pickle_by_value(sys.modules[module_name])
        result = request_for_function(inspect.currentframe(), ["pyfunc"])
        return result
    finally:
        for module_name in submodules:
            cloudpickle.unregister_pickle_by_value(sys.modules[module_name])


def log_metric(key: str, value: float, step: Optional[int] = None) -> None:
    """Log a metric under the current run. If no run is active, this method will create a new active run."""
    start_run_if_not_exist()
    return request_for_function(inspect.currentframe())


def log_artifact(local_path: str, artifact_path: Optional[str] = None) -> None:
    """
    Log a local file or directory as an artifact of the currently active run.

    If no run is active, this method will create a new active run.
    """
    start_run_if_not_exist()
    return request_for_function(inspect.currentframe())


def log_param(key: str, value: Any) -> Any:
    """
    Log a parameter (e.g. model hyperparameter) under the current run.

    If no run is active, this method will create a new active run.
    """
    start_run_if_not_exist()
    return request_for_function(inspect.currentframe())


def log_params(params: Dict[str, Any]) -> None:
    """
    Log a batch of params for the current run.

    If no run is active, this method will create a new active run.
    """
    start_run_if_not_exist()
    return request_for_function(inspect.currentframe())


def set_tag(key: str, value: Any) -> None:
    """Set a tag under the current run. If no run is active, this method will create a new active run."""
    start_run_if_not_exist()
    return request_for_function(inspect.currentframe())


def autolog(
    log_every_n_epoch=1,
    log_every_n_step=None,
    log_models=True,
    log_datasets=True,
    disable=False,
    exclusive=False,
    disable_for_unsupported_versions=False,
    silent=False,
    registered_model_name=None,
) -> None:
    """
    Enable (or disable) and configure autologging for all supported integrations.

    The parameters are passed to any autologging integrations that support them.
    """
    start_run_if_not_exist()
    return request_for_function(inspect.currentframe(), ["pytorch"])


default_model = Model()


def save_model(
    path, loader_module=None, data_path=None, code_path=None, conda_env=None, mlflow_model=default_model, python_model=None, artifacts=None
):
    """
    Save a Pyfunc model with custom inference logic and optional data dependencies to a path on the local filesystem.

    You cannot specify the parameters: loader_module, data_path and the parameters: python_model, artifacts together.
    """
    return request_for_function(inspect.currentframe(), ["pyfunc"])


def active_run() -> Optional[ActiveRun]:
    """Get the currently active Run, or None if no such run exists."""
    return active_run_stack[-1] if len(active_run_stack) > 0 else None


def get_run(run_id: str) -> Run:
    """
    Fetch the run from backend store.

    The resulting Run contains a collection of run metadata – RunInfo, as well as a collection of run parameters,
    tags, and metrics – RunData.
    In the case where multiple metrics with the same key are logged for the run, the RunData contains the most recently
    logged value at the largest step for each metric.
    """
    return request_for_function(inspect.currentframe())


finished_run_status = RunStatus.to_string(RunStatus.FINISHED)


def end_run(status: str = finished_run_status) -> None:
    """End an active MLflow run (if there is one)."""
    if len(active_run_stack) > 0:
        # Clear out the global existing run environment variable as well.
        env.unset_variable(_RUN_ID_ENV_VAR)
        run = active_run_stack[-1]
        MlflowClient().set_terminated(run.info.run_id, status)
        active_run_stack.pop()


def set_server_url(url: str) -> None:
    """
    Set server URL.

    If you set the URL using this function, it takes precedence over the URL from the environment variable 'server_url'.
    """
    variables.server_url = url


def get_server_url() -> str:
    """Get the current server URL."""
    return variables._get_server_url()


def set_model_version_requirements(name: str, version: int, model_type: ModelType) -> None:
    """Installing requirements of the model locally."""
    if model_type == ModelType.MODEL:
        requirements = MlflowClient().get_model_version_requirements(name=name, version=version)
    elif model_type == ModelType.EXECUTOR:
        requirements = MlflowClient().get_executor_version_requirements(name=name, version=version)
    elif model_type == ModelType.DATASET_LOADER:
        requirements = MlflowClient().get_dataset_loader_version_requirements(name=name, version=version)
    else:
        raise ModelTypeIsNotFound()
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--no-cache-dir", "--default-timeout=100", *requirements])
    except Exception:
        print(traceback.format_exc())
        print(f"Requirements for {name} weren't installed correctly.")


def load_model(name: str, version: int, install_requirements: bool = False, unwrap: bool = True):
    """Download all model's files for loading model locally."""
    if install_requirements:
        set_model_version_requirements(name=name, version=version, model_type=ModelType.MODEL)
    run_id = MlflowClient().get_model_version(name, version).run_id
    return _load_model_type(run_id, unwrap)


def load_dataset(name: str, version: int, install_requirements: bool = False, unwrap: bool = True):
    """Download all model's files for loading model locally."""
    if install_requirements:
        set_model_version_requirements(name=name, version=version, model_type=ModelType.DATASET_LOADER)
    run_id = MlflowClient().get_dataset_loader_version(name, version).run_id
    return _load_model_type(run_id, unwrap)


def load_executor(name: str, version: int, install_requirements: bool = False, unwrap: bool = True):
    """Download all model's files for loading model locally."""
    if install_requirements:
        set_model_version_requirements(name=name, version=version, model_type=ModelType.EXECUTOR)
    run_id = MlflowClient().get_executor_version(name, version).run_id
    return _load_model_type(run_id, unwrap)


atexit.register(end_run)


class MlflowClient(AbstractMlflowClient):
    """Initialize an MLflow Client."""

    def __init__(self):
        self.extra_attrs = ["tracking"]
        self.for_class = {"class_name": self.__class__.__name__, "class_kwargs": {}}

    def set_model_version_tag(
        self, name: str, version: Optional[str] = None, key: Optional[str] = None, value: Optional[Any] = None, stage: Optional[str] = None
    ) -> None:
        """Set model version tag."""
        return request_for_function(
            inspect.currentframe(),
            extra_attrs=self.extra_attrs,
            for_class=self.for_class,
        )

    def set_dataset_loader_version_tag(
        self, name: str, version: Optional[str] = None, key: Optional[str] = None, value: Optional[Any] = None, stage: Optional[str] = None
    ) -> None:
        """Set dataset loader version tag."""
        return request_for_function(
            inspect.currentframe(),
            extra_attrs=self.extra_attrs,
            for_class=self.for_class,
        )

    def set_executor_version_tag(
        self, name: str, version: Optional[str] = None, key: Optional[str] = None, value: Optional[Any] = None, stage: Optional[str] = None
    ) -> None:
        """Set executor version tag."""
        return request_for_function(
            inspect.currentframe(),
            extra_attrs=self.extra_attrs,
            for_class=self.for_class,
        )

    def get_run(self, run_id: str) -> Run:
        """Get run by id."""
        return request_for_function(
            inspect.currentframe(),
            extra_attrs=self.extra_attrs,
            for_class=self.for_class,
        )

    def get_registered_model(self, name: str) -> RegisteredModel:
        """Get registered model by name."""
        return request_for_function(
            inspect.currentframe(),
            extra_attrs=self.extra_attrs,
            for_class=self.for_class,
        )

    def get_registered_dataset_loader(self, name: str) -> RegisteredModel:
        """Get registered dataset loader by name."""
        return request_for_function(
            inspect.currentframe(),
            extra_attrs=self.extra_attrs,
            for_class=self.for_class,
        )

    def get_registered_executor(self, name: str) -> RegisteredModel:
        """Get registered executor by name."""
        return request_for_function(
            inspect.currentframe(),
            extra_attrs=self.extra_attrs,
            for_class=self.for_class,
        )

    # TODO after updating to a new version, the result is paginated
    # and needs to be converted to pagination scheme of our project.
    def search_model_versions(
        self,
        filter_string: Optional[str] = None,
        max_results: int = 10000,
        order_by: Optional[List[str]] = None,
        page_token: Optional[str] = None,
    ) -> PagedList[ModelVersion]:
        """Search for model versions in backend that satisfy the filter criteria."""
        return request_for_function(
            inspect.currentframe(),
            extra_attrs=self.extra_attrs,
            for_class=self.for_class,
        )

    def set_terminated(self, run_id: str, status: Optional[str] = None, end_time: Optional[int] = None) -> None:
        """Set a run’s status to terminated."""
        return request_for_function(
            inspect.currentframe(),
            extra_attrs=self.extra_attrs,
            for_class=self.for_class,
        )

    def get_model_version(self, name: str, version: int) -> ModelVersion:
        """Get model version by model name and version number."""
        return request_for_function(
            inspect.currentframe(),
            for_class=self.for_class,
        )

    def get_dataset_loader_version(self, name: str, version: int) -> ModelVersion:
        """Get dataset loader version by dataset loader name and version number."""
        return request_for_function(
            inspect.currentframe(),
            for_class=self.for_class,
        )

    def get_executor_version(self, name: str, version: int) -> ModelVersion:
        """Get executor version by executor name and version number."""
        return request_for_function(
            inspect.currentframe(),
            for_class=self.for_class,
        )

    def download_artifacts(self, run_id: str, path: str, dst_path: Optional[str] = None) -> str:
        """Download an artifact file or directory from a run to a local directory, and return a local path for it."""
        file = request_for_function(
            inspect.currentframe(),
            extra_attrs=self.extra_attrs,
            for_class=self.for_class,
        )

        # save artifacts to local store
        if dst_path is None:
            dst_path = tempfile.mkdtemp()
        dst_path = os.path.abspath(os.path.normpath(dst_path))
        local_path = os.path.join(dst_path, os.path.normpath(path))
        if zipfile.is_zipfile(io.BytesIO(file)):
            zip_model = zipfile.ZipFile(io.BytesIO(file))
            try:
                if not os.path.exists(local_path):
                    os.makedirs(local_path)
            except OSError as ex:
                if ex.errno == 2:
                    ex.filename = dst_path
                raise ex
            zip_model.extractall(local_path)
        else:
            dirs = os.path.dirname(local_path)
            if not os.path.exists(dirs):
                os.makedirs(dirs)
            with open(local_path, "wb") as f:
                f.write(file)
        return local_path

    def get_model_version_requirements(self, name: str, version: int) -> list:
        """Download an artifact file and return list of requirements of the model."""
        return request_for_function(
            inspect.currentframe(),
            extra_attrs=self.extra_attrs,
            for_class=self.for_class,
        )

    def get_model_version_conda_env(self, name: str, version: int) -> dict:
        """Download an artifact file and return json file of conda environment."""
        return request_for_function(
            inspect.currentframe(),
            extra_attrs=self.extra_attrs,
            for_class=self.for_class,
        )

    def get_dataset_loader_version_requirements(self, name: str, version: int) -> list:
        """Download an artifact file and return list of requirements of the model."""
        return request_for_function(
            inspect.currentframe(),
            extra_attrs=self.extra_attrs,
            for_class=self.for_class,
        )

    def get_dataset_loader_version_conda_env(self, name: str, version: int) -> dict:
        """Download an artifact file and return json file of conda environment."""
        return request_for_function(
            inspect.currentframe(),
            extra_attrs=self.extra_attrs,
            for_class=self.for_class,
        )

    def get_executor_version_requirements(self, name: str, version: int) -> list:
        """Download an artifact file and return list of requirements of the model."""
        return request_for_function(
            inspect.currentframe(),
            extra_attrs=self.extra_attrs,
            for_class=self.for_class,
        )

    def get_executor_version_conda_env(self, name: str, version: int) -> dict:
        """Download an artifact file and return json file of conda environment."""
        return request_for_function(
            inspect.currentframe(),
            extra_attrs=self.extra_attrs,
            for_class=self.for_class,
        )
