"""This module create and send request to MLManagement server."""
import inspect
import json
import os
import shutil
from tempfile import TemporaryDirectory

import cloudpickle
import requests
from ML_management.mlmanagement import variables
from ML_management.mlmanagement.jsonschema_inference import infer_jsonschema
from ML_management.mlmanagement.model_type import ModelType
from ML_management.mlmanagement.server_mlmanager_exceptions import InvalidExperimentName, InvalidVisibilityOption, ModelTypeIsNotFound
from ML_management.mlmanagement.variables import (
    EXPERIMENT_NAME_FOR_DATASET_LOADER,
    EXPERIMENT_NAME_FOR_EXECUTOR,
    active_run_stack,
    server_ml_api,
)
from mlflow.exceptions import MlflowException, RestException
from requests_toolbelt import MultipartEncoder

import mlflow


def create_kwargs(frame, is_it_class_function=False):
    """Get name and kwargs of function by its frame."""
    function_name = inspect.getframeinfo(frame)[2]  # get name of function
    _, _, _, kwargs = inspect.getargvalues(frame)  # get kwargs of function
    if "self" in kwargs:
        del kwargs["self"]
    if is_it_class_function:
        if "dst_path" in kwargs:
            del kwargs["dst_path"]
    return (
        function_name,
        kwargs,
    )  # return name of mlflow function and kwargs for that function


def request_log_model(function_name, kwargs, extra_attrs, module_name):
    """
    Send request for log_model function.

    Steps for log model:
    0) Infer jsonschema, raise if it is invalid
    1) open temporary directory
    2) Do mlflow.save_model() locally
    3) Pack it to zip file
    4) Send it to server to log model there.
    """
    extra_imports_args = [
        "submodules",
        "module_name",
        "used_modules_names",
        "extra_modules_names",
        "root_module_name",
    ]
    delete_args_for_save_model_func = [
        "artifact_path",
        "registered_model_name",
        "await_registration_for",
        # now, extra arguments
        "upload_model_mode",
        "source_model_name",
        "source_model_version",
        "visibility",
    ]  # not need for save_model
    delete_args_for_log_func = [
        "python_model",
        "artifacts",
        "conda_env",
        "pip_requirements",
        "extra_pip_requirements",
    ]  # not need for log model on server
    for delete_arg in extra_imports_args:
        del kwargs[delete_arg]
    kwargs_for_save_model = kwargs.copy()
    for delete_arg in delete_args_for_save_model_func:
        del kwargs_for_save_model[delete_arg]

    python_model = kwargs_for_save_model["python_model"]

    # import some modules here because of circular import
    from ML_management.dataset_loader_template.dataset_loader_pattern import DatasetLoaderPattern
    from ML_management.dataset_loader_template.dataset_loader_pattern_to_methods_map import dataset_loader_pattern_to_methods
    from ML_management.executor_template.executor_pattern import JobExecutorPattern
    from ML_management.executor_template.executor_pattern_to_methods_map import executor_pattern_to_methods
    from ML_management.models.model_type_to_methods_map import model_pattern_to_methods
    from ML_management.models.patterns.model_pattern import Model

    with TemporaryDirectory() as temp_dir:
        model_folder = "model"
        path_for_model_folder = os.path.join(temp_dir, model_folder)
        zip_file_folder = "zip_file"
        path_for_zip_file = os.path.join(temp_dir, zip_file_folder)
        if python_model is not None:
            if not isinstance(python_model, JobExecutorPattern):
                del kwargs["visibility"]
            if isinstance(python_model, Model):
                kwargs["model_type"] = ModelType.MODEL
                model_to_methods = model_pattern_to_methods
                if variables.active_experiment_name in [EXPERIMENT_NAME_FOR_EXECUTOR, EXPERIMENT_NAME_FOR_DATASET_LOADER]:
                    raise InvalidExperimentName(ModelType.MODEL.value, variables.active_experiment_name)
            elif isinstance(python_model, JobExecutorPattern):
                kwargs["model_type"] = ModelType.EXECUTOR
                model_to_methods = executor_pattern_to_methods
                if variables.active_experiment_name != EXPERIMENT_NAME_FOR_EXECUTOR:
                    raise InvalidExperimentName(ModelType.EXECUTOR.value, variables.active_experiment_name)
                if kwargs["visibility"] is None:
                    raise InvalidVisibilityOption(ModelType.EXECUTOR.value)
                # collect all needed model's methods
                kwargs["model_method_names"] = python_model.desired_model_methods
                kwargs["executor_upload_model_mode"] = python_model.executor_upload_model_mode
            elif isinstance(python_model, DatasetLoaderPattern):
                kwargs["model_type"] = ModelType.DATASET_LOADER
                model_to_methods = dataset_loader_pattern_to_methods
                if variables.active_experiment_name != EXPERIMENT_NAME_FOR_DATASET_LOADER:
                    raise InvalidExperimentName(kwargs["model_type"].value, variables.active_experiment_name)
            else:
                raise ModelTypeIsNotFound()

            # now we need to infer schemas for methods.
            methods_schema = {}
            for model_type, methods_name_to_schema_map in model_to_methods.items():
                if isinstance(python_model, model_type):
                    for method_name_to_schema in methods_name_to_schema_map:
                        model_method = getattr(python_model, method_name_to_schema.name, None)
                        model_method_schema = infer_jsonschema(model_method)
                        methods_schema[method_name_to_schema.value] = model_method_schema
            kwargs["model_methods_schema"] = json.dumps(methods_schema)

            mlflow.pyfunc.save_model(path=path_for_model_folder, **kwargs_for_save_model)

            for delete_arg in delete_args_for_log_func:
                del kwargs[delete_arg]
            kwargs["loader_module"] = mlflow.pyfunc.model.__name__
            model_filename = shutil.make_archive(path_for_zip_file, "zip", path_for_model_folder)

        elif kwargs["loader_module"] is not None:
            # now one could log only ModelType.MODEL type by 'loader_module' parameter.
            kwargs["model_type"] = ModelType.MODEL
            del kwargs["visibility"]
            if variables.active_experiment_name in [EXPERIMENT_NAME_FOR_EXECUTOR, EXPERIMENT_NAME_FOR_DATASET_LOADER]:
                raise InvalidExperimentName(ModelType.MODEL.value, variables.active_experiment_name)
            # 'model_methods_schema' not defined
            kwargs["model_methods_schema"] = json.dumps({})

            if not os.path.isdir(kwargs["data_path"]):
                raise Exception("Directory {0} doesn't exist".format(kwargs["data_path"]))
            model_filename = shutil.make_archive(path_for_zip_file, "zip", kwargs["data_path"])
        else:
            raise Exception("Either python_model or loader_module parameter must be specified")

        with open(model_filename, "rb") as file:
            return request(function_name, kwargs, extra_attrs, file, module_name=module_name)


def request_log_artifacts(function_name, kwargs, extra_attrs):
    """Send request for log artifact."""
    local_path = kwargs["local_path"]
    if not os.path.isdir(local_path):
        with open(local_path, "rb") as file:
            return request(function_name, kwargs, extra_attrs, artifact_file=file)
    with TemporaryDirectory() as temp_dir:
        artifact_filename = shutil.make_archive(os.path.join(temp_dir, "zip_file"), "zip", local_path)
        with open(artifact_filename, "rb") as file:
            return request(function_name, kwargs, extra_attrs, artifact_file=file)


def request(function_name, kwargs, extra_attrs, model_file=None, artifact_file=None, for_class=None, module_name=None):
    """Create mlflow_request and send it to server."""
    mlflow_request = {
        "function_name": function_name,
        "kwargs": kwargs,
        "for_class": for_class,
        "extra_attrs": extra_attrs,
        "module_name": module_name,
        "experiment_name": variables.active_experiment_name,
        "active_run_ids": list(map(lambda run: run.info.run_id, active_run_stack)),
    }
    files = {
        "mlflow_request": json.dumps(mlflow_request),
        "model_zip": ("filename", model_file, "multipart/form-data"),
        "artifact_file": ("artifacts_filename", artifact_file, "multipart/form-data"),
    }

    multipart = MultipartEncoder(fields=files)
    return requests.post(
        server_ml_api,
        data=multipart,
        headers={"Content-Type": multipart.content_type},
        auth=(os.getenv("login", ""), os.getenv("password", "")),
    )


def send_request_to_server(function_name, kwargs, extra_attrs, for_class, module_name):
    """
    Send request to server.

    Takes frame of mlflow func and extra_attr
    extra_attr is needed if original mlflow function is in the mlflow.<extra_attr> package
    for example function log_model is in mlflow.pyfunc module (mlflow.pyfunc.log_model())
    """
    # special case for log_model, load_model, save_model
    if function_name == "log_model":
        response = request_log_model(function_name, kwargs, extra_attrs, module_name)
    elif function_name == "save_model":
        return mlflow.pyfunc.save_model(**kwargs)
    elif function_name == "log_artifact":
        response = request_log_artifacts(function_name, kwargs, extra_attrs)
    else:
        response = request(function_name, kwargs, extra_attrs, for_class=for_class, module_name=module_name)

    response_content = response.content

    try:
        decoded_result = cloudpickle.loads(response_content)
    except Exception:
        raise Exception(response_content.decode())

    # raise error if mlflow is supposed to raise error
    if isinstance(decoded_result, MlflowException):
        is_rest = decoded_result.json_kwargs.pop("isRest", False)
        if is_rest:
            created_json = {
                "error_code": decoded_result.error_code,
                "message": decoded_result.message,
            }
            decoded_result = RestException(created_json)
        raise decoded_result
    elif isinstance(decoded_result, Exception):
        raise decoded_result
    return decoded_result


def _check_if_call_from_predict_function():
    """
    Check if call to server was from predict function of model.

    Calls from predict function are prohibited and will do and return nothing.
    """
    from ML_management.models.model_type_to_methods_map import ModelMethodName
    from ML_management.models.patterns.model_pattern import Model

    predict_func_name = ModelMethodName.predict_function.name

    for frame in inspect.stack():
        if frame.function == predict_func_name and Model in frame[0].f_locals.get("self").__class__.__mro__:
            return True
    return False


def request_for_function(frame, extra_attrs=None, for_class=None, module_name=None):
    """
    Send request to server or call mlflow function straightforward.

    Input parameters:
    :param frame: frame of equivalent mlflow function
    :param extra_attrs: list of extra modules for mlflow library, for example "tracking" (mlflow.tracking)
    :param for_class: parameters in case of mlflow class (for example mlflow.tracking.MLflowClient() class)
    """
    if _check_if_call_from_predict_function():
        return None
    if extra_attrs is None:
        extra_attrs = []
    if module_name is None:
        module_name = "mlflow"

    function_name, kwargs = create_kwargs(frame, for_class is not None)

    return send_request_to_server(function_name, kwargs, extra_attrs, for_class, module_name)
