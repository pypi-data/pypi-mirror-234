"""Define finetune executor class."""
from ML_management.executor_template.executor_pattern import JobExecutorPattern
from ML_management.executor_template.upload_model_mode import UploadModelMode
from ML_management.models.model_type_to_methods_map import ModelMethodName


class FinetuneExecutor(JobExecutorPattern):
    """Finetune executor from pattern with defined settings parameters."""

    def __init__(self):
        super().__init__(
            executor_name="finetune",
            desired_model_methods=[ModelMethodName.finetune_function],
            executor_upload_model_mode=UploadModelMode.new_version,
        )

    def execute(self):
        """Define execute function that calls finetune_function of model with corresponding params."""
        return self.model.finetune_function(**self.model_methods_parameters[ModelMethodName.finetune_function])
