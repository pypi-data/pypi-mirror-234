from ..utils.model_params.base_model_params import BaseModelParams
from ..utils.dimensions import Dimensions


class SimCLRModelParams(BaseModelParams):
    """
    SimCLR model params.
    """

    def __init__(self):
        super().__init__("sim_clr")

        self.input_dimensions = Dimensions(height=128, width=128)

        self.batch_size = 32  # the greater the better
        self.learning_rate = 0.3 * self.batch_size / 256
        self.weight_decay = 1e-6
        self.nb_warmup_epochs = 10

        self.train_ratio = 0.8
        self.val_ratio = 0.1
        self.test_ratio = 0.1

        self.nb_modalities = 3

        self.n_views = 2
        self.temperature = 0.07
