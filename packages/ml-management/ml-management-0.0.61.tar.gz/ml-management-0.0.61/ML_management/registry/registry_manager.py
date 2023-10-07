"""Define Model Registry Manager."""
import inspect

from ML_management.mlmanagement.mlmanager import request_for_function
from ML_management.mlmanagement.singleton_pattern import Singleton
from ML_management.registry.abstract_registry_manager import AbstractRegistryManager
from mlflow.entities.model_registry.model_version import ModelVersion
from mlflow.store.entities import PagedList


class RegistryManager(AbstractRegistryManager, metaclass=Singleton):
    """Registry Manager to choose necessary version of the model."""

    def __init__(self):
        self.module_name = "RegistryManager"

    def get_latest_model_version(self, name: str) -> ModelVersion:
        """Get the latest version of a model "name"."""
        return request_for_function(
            inspect.currentframe(),
            module_name=self.module_name,
        )

    def get_latest_dataset_loader_version(self, name: str) -> ModelVersion:
        """Get the latest version of a dataset loader "name"."""
        return request_for_function(
            inspect.currentframe(),
            module_name=self.module_name,
        )

    def get_latest_executor_version(self, name: str) -> ModelVersion:
        """Get the latest version of an executor "name"."""
        return request_for_function(
            inspect.currentframe(),
            module_name=self.module_name,
        )

    def get_best_model_version(self, name: str, metric: str, optimal_min: bool = False) -> ModelVersion:
        """Get best version of model "name" according to a metric."""
        return request_for_function(
            inspect.currentframe(),
            module_name=self.module_name,
        )

    def get_initial_model_version(self, name: str) -> ModelVersion:
        """Get initial version of model "name"."""
        return request_for_function(
            inspect.currentframe(),
            module_name=self.module_name,
        )

    def get_initial_dataset_loader_version(self, name: str) -> ModelVersion:
        """Get initial version of dataset loader "name"."""
        return request_for_function(
            inspect.currentframe(),
            module_name=self.module_name,
        )

    def get_initial_executor_version(self, name: str) -> ModelVersion:
        """Get initial version of executor "name"."""
        return request_for_function(
            inspect.currentframe(),
            module_name=self.module_name,
        )

    def get_all_model_versions(self, name: str) -> PagedList[ModelVersion]:
        """
        Get all versions of a given model and return PagedList of ModelVersion objects.

        https://mlflow.org/docs/latest/python_api/mlflow.entities.html#mlflow.entities.model_registry.ModelVersion

        Parameters:
            name (str): Model name used for model registration.

        Returns:
            PagedList[ModelVersion]: Available model versions
        """
        return request_for_function(
            inspect.currentframe(),
            module_name=self.module_name,
        )

    def get_all_dataset_loader_versions(self, name: str) -> PagedList[ModelVersion]:
        """
        Get all versions of a given dataset loader and return PagedList of ModelVersion objects.

        https://mlflow.org/docs/latest/python_api/mlflow.entities.html#mlflow.entities.model_registry.ModelVersion

        Parameters:
            name (str): Dataset loader name used for model registration.

        Returns:
            PagedList[ModelVersion]: Available dataset loader versions
        """
        return request_for_function(
            inspect.currentframe(),
            module_name=self.module_name,
        )

    def get_all_executor_versions(self, name: str) -> PagedList[ModelVersion]:
        """
        Get all versions of a given executor and return PagedList of ModelVersion objects.

        https://mlflow.org/docs/latest/python_api/mlflow.entities.html#mlflow.entities.model_registry.ModelVersion

        Parameters:
            name (str): Executor name used for model registration.

        Returns:
            PagedList[ModelVersion]: Available executor versions
        """
        return request_for_function(
            inspect.currentframe(),
            module_name=self.module_name,
        )
