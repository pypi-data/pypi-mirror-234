"""Define Abstract class for Model with necessary methods and methods to implement."""
from abc import ABC, abstractmethod
from typing import List, Optional

from ML_management.mlmanagement import mlmanagement, variables
from ML_management.mlmanagement.module_finder import ModuleFinder

import mlflow


class Model(mlflow.pyfunc.PythonModel, ABC):
    """Abstract class for model that Job will use."""

    def __init__(self):
        """Initialize Model class."""
        # That parameters will be set automatically while loading the model.
        """
        :param self.artifacts: A dictionary containing ``<name, local_path>`` entries.
        """
        self.artifacts: dict = {}
        # That parameters will be set automatically in job before the 'execute' func would be executed.
        """
        "param self.dataset: DatasetLoader object
        """
        self.dataset = None

    @abstractmethod
    def predict_function(self, **kwargs):
        """Every model should make predictions."""
        raise NotImplementedError

    def upload_model(
        self,
        registered_model_name: str,
        artifacts: dict = None,
        experiment_name: str = None,
        pip_requirements=None,
        extra_pip_requirements=None,
        conda_env=None,
        extra_modules_names: Optional[List[str]] = None,
        used_modules_names: Optional[List[str]] = None,
    ):
        """
        Upload wrapper to MLmanagement server.

        :param pyfunc_model_name: The run-relative artifact path to which to log the Python model.
        :param artifacts: A dictionary containing ``<name, artifact_uri>`` entries. Remote artifact URIs
                          are resolved to absolute filesystem paths, producing a dictionary of
                          ``<name, absolute_path>`` entries. ``python_model`` can reference these
                          resolved entries as the ``artifacts`` property of the ``context`` parameter
                          in :func:`PythonModel.load_context() <mlflow.pyfunc.PythonModel.load_context>`
                          and :func:`PythonModel.predict() <mlflow.pyfunc.PythonModel.predict>`.
                          For example, consider the following ``artifacts`` dictionary::

                            {
                                "my_file": "s3://my-bucket/path/to/my/file"
                            }

                          In this case, the ``"my_file"`` artifact is downloaded from S3. The
                          ``python_model`` can then refer to ``"my_file"`` as an absolute filesystem
                          path via ``context.artifacts["my_file"]``.

                          If ``None``, no artifacts are added to the model.
        :param registered_model_name: This argument may change or be removed in a
                                      future release without warning. If given, create a model
                                      version under ``registered_model_name``, also creating a
                                      registered model if one with the given name does not exist
        :param experiment_name: Name of experiment to which load the model
        :param pip_requirements: {{ pip_requirements }}
        :param extra_pip_requirements: {{ extra_pip_requirements }}
        `pip_requirements` and 'extra_pip_requirements' must be either a string path to a pip requirements file on the
            local filesystem or an iterable of pip requirement strings.
        :param conda_env: {{ conda_env }}
        'conda_env' must be a dict specifying the conda environment for this model.
        :param extra_modules_names: names of modules that should be pickled by value
            in addition to auto-detected modules.
        :param used_modules_names: modules that should be pickled by value, disables the auto-detection of modules.
        """
        old_experiment_name = variables.active_experiment_name
        if experiment_name:
            mlmanagement.set_experiment(experiment_name)
        try:
            with mlmanagement.start_run(nested=True):
                mlmanagement.log_model(
                    artifact_path="",
                    python_model=self,
                    artifacts=artifacts,
                    registered_model_name=self.model_name if hasattr(self, "model_name") else registered_model_name,
                    source_model_name=self.source_model_name
                    if hasattr(self, "source_model_name")
                    else None,  # set that after model download from mlflow
                    source_model_version=self.source_model_version
                    if hasattr(self, "source_model_version")
                    else None,  # set that after model download from mlflow
                    pip_requirements=pip_requirements,
                    extra_pip_requirements=extra_pip_requirements,
                    conda_env=conda_env,
                    extra_modules_names=extra_modules_names,
                    used_modules_names=used_modules_names,
                    root_module_name=ModuleFinder.get_my_caller_module_name(),
                )
        except Exception as err:
            raise err
        finally:
            variables.active_experiment_name = old_experiment_name
