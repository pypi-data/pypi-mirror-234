"""Map supported dataset loader function name to infer jsonschema."""
from enum import Enum

from ML_management.dataset_loader_template import dataset_loader_pattern


class DatasetLoaderMethodName(str, Enum):
    """Map supported dataset loader function name to infer jsonschema."""

    get_dataset = "dataset_loader_method_schema"


dataset_loader_pattern_to_methods = {dataset_loader_pattern.DatasetLoaderPattern: [DatasetLoaderMethodName.get_dataset]}
