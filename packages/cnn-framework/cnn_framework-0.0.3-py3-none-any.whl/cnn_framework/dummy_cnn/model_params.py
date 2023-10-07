from ..utils.model_params.base_model_params import BaseModelParams
from ..utils.dimensions import Dimensions


class DummyModelParams(BaseModelParams):
    """
    Dummy model params.
    """

    def __init__(self):
        super().__init__("dummy_cnn")

        self.input_dimensions = Dimensions(height=128, width=128)

        self.num_epochs = 20
        self.learning_rate = 1e-4

        self.train_ratio = 0.8
        self.val_ratio = 0.1
        self.test_ratio = 0.1

        self.nb_classes = 2
        self.class_names = ["Square", "Circle"]
        self.nb_modalities = 3
