"""Executor template for custom executor."""
from abc import ABC, abstractmethod
from typing import List, Optional

from ML_management.executor_template.upload_model_mode import UploadModelMode
from ML_management.mlmanagement import mlmanagement, variables
from ML_management.mlmanagement.module_finder import ModuleFinder
from ML_management.mlmanagement.variables import EXPERIMENT_NAME_FOR_EXECUTOR
from ML_management.mlmanagement.visibility_options import VisibilityOptions
from ML_management.models.model_type_to_methods_map import ModelMethodName
from mlflow.pyfunc import PythonModel


class JobExecutorPattern(PythonModel, ABC):
    """Define custom job executor."""

    def __init__(self, executor_name: str, desired_model_methods: List[ModelMethodName], executor_upload_model_mode: UploadModelMode):
        """
        Init JobExecutorPattern class.

        :param executor_name: The name of the executor
        :param desired_model_methods: Specify list of desired model methods for this executor
        :param executor_upload_model_mode: How to log model after job
        """
        self.executor_name = executor_name
        self.desired_model_methods = desired_model_methods
        self.executor_upload_model_mode = executor_upload_model_mode

        # That parameters will be set automatically while loading the model.
        """
        :param self.artifacts: A dictionary containing ``<name, local_path>`` entries.
        """
        self.artifacts: dict = {}

        # That parameters will be set automatically in job before the 'execute' func would be executed.
        """
        :param self.model: python model class
        :param self.dataset: object for dataset
        :param self.model_methods_parameters: the dict of parameters for each desired_model_methods.
            One could use it in execute() function like that:
                def execute(self):
                    self.model.train_function(**self.model_methods_parameters[ModelMethodName.train_function])
            In that case method 'execute' calls train_function method of the model with corresponding parameters for that method
            See examples in default_executors folder.
        :param self.model_methods_schema: the dict of schema parameters for each desired_model_methods.
        """
        self.model = None
        self.dataset = None
        self.model_methods_parameters: dict = {}
        self.model_methods_schema: dict = {}

    @abstractmethod
    def execute(self, **executor_params):
        """
        Do execution step.

        Parameter self.model with the desired model will be set automatically in the job before 'execute' execution.
        To get data_path use self.data_path parameter, which also will be set in the job.
        'executor_methods_params' are executor parameters. One has to define it as ordinary kwargs with type annotation.
        Also, you could use self.model_methods_parameters for call desired model method with right params.
        return param: artifacts: A dictionary containing ``<name, artifact_uri>`` entries.
                      For example, consider the following ``artifacts`` dictionary::

                        {
                            "my_file": "s3://my-bucket/path/to/my/file",
                            "my_file2": "/home/username/path/to/my/file"
                        }

                      In this case, the ``"my_file"`` artifact is downloaded from S3.
                      The ``"my_file2"`` artifact is downloaded from local path.

                      If ``None``, no artifacts are added to the model.
        """
        raise NotImplementedError

    def upload_executor(
        self,
        pip_requirements=None,
        extra_pip_requirements=None,
        conda_env=None,
        artifacts: Optional[dict] = None,
        visibility: VisibilityOptions = VisibilityOptions.PRIVATE,
        extra_modules_names: Optional[List[str]] = None,
        used_modules_names: Optional[List[str]] = None,
    ):
        """
        Upload wrapper to MLmanagement server.

        :param pip_requirements: {{ pip_requirements }}

        :param extra_pip_requirements: {{ extra_pip_requirements }}
        `pip_requirements` and 'extra_pip_requirements' must be either a string path to a pip requirements file on the
            local filesystem or an iterable of pip requirement strings.

        :param conda_env: {{ conda_env }}
        'conda_env' must be a dict specifying the conda environment for this model.

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

                          If ``None``, no artifacts are added to the executor.

        :param visibility: either a private or public executor.

        :param extra_modules_names: names of modules that should be pickled by value
            in addition to auto-detected modules.

        :param used_modules_names: modules that should be pickled by value, disables the auto-detection of modules.
        """
        old_experiment_name = variables.active_experiment_name
        mlmanagement.set_experiment(EXPERIMENT_NAME_FOR_EXECUTOR)
        try:
            with mlmanagement.start_run(nested=True):
                mlmanagement.log_model(
                    artifact_path="",
                    artifacts=artifacts,
                    python_model=self,
                    registered_model_name=self.executor_name,
                    pip_requirements=pip_requirements,
                    extra_pip_requirements=extra_pip_requirements,
                    conda_env=conda_env,
                    visibility=visibility,
                    extra_modules_names=extra_modules_names,
                    used_modules_names=used_modules_names,
                    root_module_name=ModuleFinder.get_my_caller_module_name(),
                )
        except Exception as err:
            raise err
        finally:
            variables.active_experiment_name = old_experiment_name
