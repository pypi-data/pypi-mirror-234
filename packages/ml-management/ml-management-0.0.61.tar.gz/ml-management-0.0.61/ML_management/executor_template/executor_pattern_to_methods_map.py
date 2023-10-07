"""Map supported executor function name to infer jsonschema to tag."""
from enum import Enum

from ML_management.executor_template import executor_pattern


class ExecutorMethodName(str, Enum):
    """Map supported executor function name to infer jsonschema."""

    execute = "executor_method_schema"


executor_pattern_to_methods = {executor_pattern.JobExecutorPattern: [ExecutorMethodName.execute]}
