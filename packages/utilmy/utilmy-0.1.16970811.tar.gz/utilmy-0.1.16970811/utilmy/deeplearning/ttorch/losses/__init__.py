"""# pytorch-loss
Docs::


    Also tried to implement swish, hard-swish(hswish) and mish activation functions.

    Additionally, cuda based one-hot function is added (support label smooth).

    Newly add an "Exponential Moving Average(EMA)" operator.

    Add convolution ops, such as coord-conv2d, and dynamic-conv2d(dy-conv2d).

    Some operators are implemented with pytorch cuda extension, so you need to compile it first:


    After installing, now you can pick up what you need and use the losses or ops like one of thes:
    ```python
    from losses import SwishV1, SwishV2, SwishV3
    from losses import HSwishV1, HSwishV2, HSwishV3
    from losses import MishV1, MishV2, MishV3
    from losses import convert_to_one_hot, convert_to_one_hot_cu, OnehotEncoder
    from losses import EMA

    from losses import TripletLoss
    from losses import SoftDiceLossV1, SoftDiceLossV2, SoftDiceLossV3
    from losses import PCSoftmaxCrossEntropyV1, PCSoftmaxCrossEntropyV2
    from losses import LargeMarginSoftmaxV1, LargeMarginSoftmaxV2, LargeMarginSoftmaxV3
    from losses import LabelSmoothSoftmaxCEV1, LabelSmoothSoftmaxCEV2, LabelSmoothSoftmaxCEV3
    from losses import generalized_iou_loss
    from losses import FocalLossV1, FocalLossV2, FocalLossV3
    from losses import Dual_Focal_loss
    from losses import GeneralizedSoftDiceLoss, BatchSoftDiceLoss
    from losses import AMSoftmax
    from losses import AffinityFieldLoss, AffinityLoss
    from losses import OhemCELoss, OhemLargeMarginLoss
    from losses import LovaszSoftmaxV1, LovaszSoftmaxV3
    from losses import TaylorCrossEntropyLossV1, TaylorCrossEntropyLossV3
    from losses import InfoNceDist
    from losses import PartialFCAMSoftmax

    from losses import TaylorSoftmaxV1, TaylorSoftmaxV3
    from losses import LogTaylorSoftmaxV1, LogTaylorSoftmaxV3

    from losses import CoordConv2d, DY_Conv2d
    ```
    Note that some losses or ops have 3 versions, like `LabelSmoothSoftmaxCEV1`, `LabelSmoothSoftmaxCEV2`, `LabelSmoothSoftmaxCEV3`, here `V1` means the implementation with pure pytorch ops and use `torch.autograd` for backward computation, `V2` means implementation with pure pytorch ops but use self-derived formula for backward computation, and `V3` means implementation with cuda extension. Generally speaking, the `V3` ops are faster and more memory efficient, since I have tried to squeeze everything in one cuda kernel function, which in most cases brings less overhead than a combination of pytorch ops.


    For those who happen to find this repo, if you see errors in my code, feel free to open an issue to correct me.



"""
from typing import Optional, Sequence

import torch
from torch import Tensor, nn
from torch.nn import functional as F

from .swish import SwishV1, SwishV2, SwishV3
from .hswish import HSwishV1, HSwishV2, HSwishV3
from .frelu import FReLU
from .mish import MishV1, MishV2, MishV3
from .one_hot import convert_to_one_hot, convert_to_one_hot_cu, OnehotEncoder
from .ema import EMA

from .triplet_loss import TripletLoss
from .soft_dice_loss import SoftDiceLossV1, SoftDiceLossV2, SoftDiceLossV3
from .pc_softmax import PCSoftmaxCrossEntropyV1, PCSoftmaxCrossEntropyV2
from .large_margin_softmax import LargeMarginSoftmaxV1, LargeMarginSoftmaxV2, LargeMarginSoftmaxV3
from .label_smooth import LabelSmoothSoftmaxCEV1, LabelSmoothSoftmaxCEV2, LabelSmoothSoftmaxCEV3
from .generalized_iou_loss import generalized_iou_loss
from .focal_loss import FocalLossV1, FocalLossV2, FocalLossV3
from .dual_focal_loss import Dual_Focal_loss
from .dice_loss import GeneralizedSoftDiceLoss, BatchSoftDiceLoss
from .amsoftmax import AMSoftmax
from .affinity_loss import AffinityFieldLoss, AffinityLoss
from .ohem_loss import OhemCELoss, OhemLargeMarginLoss
from .conv_ops import CoordConv2d, DY_Conv2d
from .lovasz_softmax import LovaszSoftmaxV1, LovaszSoftmaxV3
from .taylor_softmax import TaylorSoftmaxV1, TaylorSoftmaxV3, LogTaylorSoftmaxV1, LogTaylorSoftmaxV3, TaylorCrossEntropyLossV1, TaylorCrossEntropyLossV3
from .info_nce_dist import InfoNceDist
from .partial_fc_amsoftmax import PartialFCAMSoftmax

from .layer_norm import LayerNormV1, LayerNormV2, LayerNormV3


class FocalLoss(nn.Module):
    """ Focal Loss, as described in https://arxiv.org/abs/1708.02002.
    Docs::

        It is essentially an enhancement to cross entropy loss and is
        useful for classification tasks when there is a large class imbalance.
        x is expected to contain raw, unnormalized scores for each class.
        y is expected to contain class labels.
        Shape:
            - x: (batch_size, C) or (batch_size, C, d1, d2, ..., dK), K > 0.
            - y: (batch_size,) or (batch_size, d1, d2, ..., dK), K > 0.
    """

    def __init__(self,
                 alpha: Optional[Tensor] = None,
                 gamma: float = 0.,
                 reduction: str = 'mean',
                 ignore_index: int = -100):
        """Constructor.
        Args:
            alpha (Tensor, optional): Weights for each class. Defaults to None.
            gamma (float, optional): A constant, as described in the paper.
                Defaults to 0.
            reduction (str, optional): 'mean', 'sum' or 'none'.
                Defaults to 'mean'.
            ignore_index (int, optional): class label to ignore.
                Defaults to -100.
        """
        if reduction not in ('mean', 'sum', 'none'):
            raise ValueError(
                'Reduction must be one of: "mean", "sum", "none".')

        super().__init__()
        self.alpha = alpha
        self.gamma = gamma
        self.ignore_index = ignore_index
        self.reduction = reduction

        self.nll_loss = nn.NLLLoss(
            weight=alpha, reduction='none', ignore_index=ignore_index)

    def __repr__(self):
        arg_keys = ['alpha', 'gamma', 'ignore_index', 'reduction']
        arg_vals = [self.__dict__[k] for k in arg_keys]
        arg_strs = [f'{k}={v}' for k, v in zip(arg_keys, arg_vals)]
        arg_str = ', '.join(arg_strs)
        return f'{type(self).__name__}({arg_str})'

    def forward(self, x: Tensor, y: Tensor) -> Tensor:
        if x.ndim > 2:
            # (N, C, d1, d2, ..., dK) --> (N * d1 * ... * dK, C)
            c = x.shape[1]
            x = x.permute(0, *range(2, x.ndim), 1).reshape(-1, c)
            # (N, d1, d2, ..., dK) --> (N * d1 * ... * dK,)
            y = y.view(-1)

        unignored_mask = y != self.ignore_index
        y = y[unignored_mask]
        if len(y) == 0:
            return 0.
        x = x[unignored_mask]

        # compute weighted cross entropy term: -alpha * log(pt)
        # (alpha is already part of self.nll_loss)
        log_p = F.log_softmax(x, dim=-1)
        ce = self.nll_loss(log_p, y)

        # get true class column from each row
        all_rows = torch.arange(len(x))
        log_pt = log_p[all_rows, y]

        # compute focal term: (1 - pt)^gamma
        pt = log_pt.exp()
        focal_term = (1 - pt)**self.gamma

        # the full loss: -alpha * ((1 - pt)^gamma) * log(pt)
        loss = focal_term * ce

        if self.reduction == 'mean':
            loss = loss.mean()
        elif self.reduction == 'sum':
            loss = loss.sum()

        return loss


def focal_loss(alpha: Optional[Sequence] = None,
               gamma: float = 0.,
               reduction: str = 'mean',
               ignore_index: int = -100,
               device='cpu',
               dtype=torch.float32) -> FocalLoss:
    """Factory function for FocalLoss.
    Docs::

            alpha (Sequence, optional): Weights for each class. Will be converted
                to a Tensor if not None. Defaults to None.
            gamma (float, optional): A constant, as described in the paper.
                Defaults to 0.
            reduction (str, optional): 'mean', 'sum' or 'none'.
                Defaults to 'mean'.
            ignore_index (int, optional): class label to ignore.
                Defaults to -100.
            device (str, optional): Device to move alpha to. Defaults to 'cpu'.
            dtype (torch.dtype, optional): dtype to cast alpha to.
                Defaults to torch.float32.
        Returns:
            A FocalLoss object
    """
    if alpha is not None:
        if not isinstance(alpha, Tensor):
            alpha = torch.tensor(alpha)
        alpha = alpha.to(device=device, dtype=dtype)

    fl = FocalLoss(
        alpha=alpha,
        gamma=gamma,
        reduction=reduction,
        ignore_index=ignore_index)
    return