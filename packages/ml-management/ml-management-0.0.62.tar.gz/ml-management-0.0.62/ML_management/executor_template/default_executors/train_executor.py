"""Define train executor class."""
from ML_management.executor_template.executor_pattern import JobExecutorPattern
from ML_management.executor_template.upload_model_mode import UploadModelMode
from ML_management.models.model_type_to_methods_map import ModelMethodName


class TrainExecutor(JobExecutorPattern):
    """Train executor from pattern with defined settings parameters."""

    def __init__(self):
        super().__init__(
            executor_name="train",
            desired_model_methods=[ModelMethodName.train_function],
            executor_upload_model_mode=UploadModelMode.new_model,
        )

    def execute(self):
        """Define execute function that calls train_function of model with corresponding params."""
        return self.model.train_function(**self.model_methods_parameters[ModelMethodName.train_function])
