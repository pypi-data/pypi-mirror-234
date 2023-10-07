"""Define evaluate executor class."""
from ML_management.executor_template.executor_pattern import JobExecutorPattern
from ML_management.executor_template.upload_model_mode import UploadModelMode
from ML_management.models.model_type_to_methods_map import ModelMethodName


class EvalExecutor(JobExecutorPattern):
    """Eval executor from pattern with defined settings parameters."""

    def __init__(self):
        super().__init__(
            executor_name="eval", desired_model_methods=[ModelMethodName.evaluate_function], executor_upload_model_mode=UploadModelMode.none
        )

    def execute(self):
        """Define execute function that calls evaluate_function of model with corresponding params."""
        return self.model.evaluate_function(**self.model_methods_parameters[ModelMethodName.evaluate_function])
