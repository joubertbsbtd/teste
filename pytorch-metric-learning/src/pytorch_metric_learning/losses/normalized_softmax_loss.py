from .weight_regularizer_mixin import WeightRegularizerMixin
from .base_metric_loss_function import BaseMetricLossFunction
import torch
from ..utils import loss_and_miner_utils as lmu

class NormalizedSoftmaxLoss(WeightRegularizerMixin, BaseMetricLossFunction):
    def __init__(self, temperature, embedding_size, num_classes, **kwargs):
        super().__init__(**kwargs)
        self.temperature = temperature
        self.W = torch.nn.Parameter(torch.randn(embedding_size, num_classes))
        self.cross_entropy = torch.nn.CrossEntropyLoss(reduction='none')
        
    def compute_loss(self, embeddings, labels, indices_tuple):
        miner_weights = lmu.convert_to_weights(indices_tuple, labels)
        normalized_W = torch.nn.functional.normalize(self.W, p=2, dim=0)
        exponent = torch.matmul(embeddings, normalized_W) / self.temperature
        unweighted_loss = self.cross_entropy(exponent, labels)
        return torch.mean(unweighted_loss*miner_weights) + self.regularization_loss(self.W.t())