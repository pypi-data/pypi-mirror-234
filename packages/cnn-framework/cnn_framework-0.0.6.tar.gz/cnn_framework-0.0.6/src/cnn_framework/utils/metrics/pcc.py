import torch
from torchmetrics import PearsonCorrCoef

from .abstract_metric import AbstractMetric


class PCC(AbstractMetric):
    """
    Pearson Correlation Coefficient.
    """

    def __init__(self, *args):
        super().__init__(*args)
        self.metric = PearsonCorrCoef().to(self.device)
        self.name = "PCC"

    def update(self, predictions, targets, _=None):
        self.metric.update(torch.flatten(predictions), torch.flatten(targets).float())

    def get_score(self):
        return self.metric.compute().item(), None

    def reset(self):
        self.metric = PearsonCorrCoef().to(self.device)
