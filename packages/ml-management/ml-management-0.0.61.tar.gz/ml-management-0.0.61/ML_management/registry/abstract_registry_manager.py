"""Define Model Registry Manager."""
from abc import abstractmethod

from mlflow.entities.model_registry.model_version import ModelVersion
from mlflow.store.entities import PagedList


class AbstractRegistryManager:
    """Abstract Registry Manager to choose necessary version of the model."""

    @abstractmethod
    def get_latest_model_version(
        self,
        *args,
        **kwargs,
    ) -> ModelVersion:
        """Get the latest version of a model "name"."""
        raise NotImplementedError

    @abstractmethod
    def get_latest_dataset_loader_version(
        self,
        *args,
        **kwargs,
    ) -> ModelVersion:
        """Get the latest version of a dataset loader "name"."""
        raise NotImplementedError

    @abstractmethod
    def get_latest_executor_version(
        self,
        *args,
        **kwargs,
    ) -> ModelVersion:
        """Get the latest version of an executor "name"."""
        raise NotImplementedError

    @abstractmethod
    def get_best_model_version(self, *args, **kwargs) -> ModelVersion:
        """Get best version of model "name" according to a metric."""
        raise NotImplementedError

    @abstractmethod
    def get_initial_model_version(self, *args, **kwargs) -> ModelVersion:
        """Get initial version of model "name"."""
        raise NotImplementedError

    @abstractmethod
    def get_initial_dataset_loader_version(self, *args, **kwargs) -> ModelVersion:
        """Get initial version of dataset loader "name"."""
        raise NotImplementedError

    @abstractmethod
    def get_initial_executor_version(self, *args, **kwargs) -> ModelVersion:
        """Get initial version of executor "name"."""
        raise NotImplementedError

    @abstractmethod
    def get_all_model_versions(self, *args, **kwargs) -> PagedList[ModelVersion]:
        """
        Get all versions of a given model and return PagedList of ModelVersion objects.

        https://mlflow.org/docs/latest/python_api/mlflow.entities.html#mlflow.entities.model_registry.ModelVersion

        Parameters:
            name (str): Model name used for model registration.

        Returns:
            PagedList[ModelVersion]: Available model versions
        """
        raise NotImplementedError

    @abstractmethod
    def get_all_dataset_loader_versions(self, *args, **kwargs) -> PagedList[ModelVersion]:
        """
        Get all versions of a given dataset loader and return PagedList of ModelVersion objects.

        https://mlflow.org/docs/latest/python_api/mlflow.entities.html#mlflow.entities.model_registry.ModelVersion

        Parameters:
            name (str): Dataset loader name used for model registration.

        Returns:
            PagedList[ModelVersion]: Available dataset loader versions
        """
        raise NotImplementedError

    @abstractmethod
    def get_all_executor_versions(self, *args, **kwargs) -> PagedList[ModelVersion]:
        """
        Get all versions of a given executor and return PagedList of ModelVersion objects.

        https://mlflow.org/docs/latest/python_api/mlflow.entities.html#mlflow.entities.model_registry.ModelVersion

        Parameters:
            name (str): Executor name used for model registration.

        Returns:
            PagedList[ModelVersion]: Available executor versions
        """
        raise NotImplementedError
