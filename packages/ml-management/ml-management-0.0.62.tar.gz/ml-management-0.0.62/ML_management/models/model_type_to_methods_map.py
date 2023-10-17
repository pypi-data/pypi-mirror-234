"""Map supported model types to their unique abstract functions."""
from enum import Enum

from ML_management.models.patterns.evaluable_model import EvaluatableModel
from ML_management.models.patterns.model_pattern import Model
from ML_management.models.patterns.model_with_losses import ModelWithLosses
from ML_management.models.patterns.retrainable_model import RetrainableModel
from ML_management.models.patterns.torch_model import TorchModel
from ML_management.models.patterns.trainable_model import TrainableModel


class ModelMethodName(str, Enum):
    """Map supported model function names to infer jsonschemas."""

    train_function = "train_method_schema"
    predict_function = "predict_method_schema"
    finetune_function = "finetune_method_schema"
    get_nn_module = "get_nn_module_method_schema"
    evaluate_function = "evaluate_method_schema"
    get_target_layer = "get_target_layer_method_schema"
    get_losses = "get_losses_method_schema"


# link model pattern to it abstract functions
model_pattern_to_methods = {
    Model: [ModelMethodName.predict_function],
    TrainableModel: [ModelMethodName.train_function],
    RetrainableModel: [ModelMethodName.finetune_function],
    TorchModel: [ModelMethodName.get_nn_module, ModelMethodName.get_target_layer],
    EvaluatableModel: [ModelMethodName.evaluate_function],
    ModelWithLosses: [ModelMethodName.get_losses],
}
