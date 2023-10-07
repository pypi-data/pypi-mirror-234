"""Custom exception definition (necessary for RegistryManager)."""

from ML_management.mlmanagement.base_exceptions import RegistyException


class VersionNotFound(RegistyException):
    """Define Version Not Found Exception."""

    def __init__(self, model_name: str, version: int, model_type: str = "model"):
        self.model_name = model_name
        self.model_type = model_type
        self.version = version
        self.message = f'There is no version {self.version} for {self.model_type} "{self.model_name}"'
        super().__init__(self.message)

    def __reduce__(self):
        """Define reduce method to make exception picklable."""
        return (VersionNotFound, (self.model_name, self.version, self.model_type))


class MetricNotLogged(RegistyException):
    """Define Metric Not Logged exception."""

    def __init__(self, model_name: str, metric: str):
        self.model_name = model_name
        self.metric = metric
        self.message = f'Metric "{self.metric}" is not logged for model "{self.model_name}"'
        super().__init__(self.message)

    def __reduce__(self):
        """Define reduce method to make exception picklable."""
        return (MetricNotLogged, (self.model_name, self.metric))


class ModelNotRegistered(RegistyException):
    """Define Model Not Registered exception."""

    def __init__(self, model_name: str, model_type: str = "model"):
        self.model_name = model_name
        self.model_type = model_type
        self.message = f'{model_type} "{model_name}" is not registered'
        super().__init__(self.message)

    def __reduce__(self):
        """Define reduce method to make exception picklable."""
        return (ModelNotRegistered, (self.model_name, self.model_type))


class NoMetricProvided(RegistyException):
    """Define No Metric Provided exception."""

    def __init__(self, criteria: str):
        self.criteria = criteria
        self.message = f'Choice criteria "{self.criteria}" is passed, but no metric name is provided'
        super().__init__(self.message)

    def __reduce__(self):
        """Define reduce method to make exception picklable."""
        return (NoMetricProvided, (self.criteria))


class UnsupportedCriteria(RegistyException):
    """Define Unsupported Criteria exception."""

    def __init__(self, criteria: str, supported_criteria: list):
        self.criteria = criteria
        self.supported_criteria = supported_criteria
        self.message = f'Choice criteria "{self.criteria}" is unsupported, must be one of: {self.supported_criteria}'
        super().__init__(self.message)

    def __reduce__(self):
        """Define reduce method to make exception picklable."""
        return (UnsupportedCriteria, (self.criteria, self.supported_criteria))
