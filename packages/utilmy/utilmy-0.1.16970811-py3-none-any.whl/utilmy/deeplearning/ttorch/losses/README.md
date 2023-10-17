# pytorch-loss

My implementation of label-smooth, amsoftmax, partial-fc, focal-loss, dual-focal-loss, triplet-loss, giou-loss, affinity-loss, pc_softmax_cross_entropy, ohem-loss(softmax based on line hard mining loss), large-margin-softmax(bmvc2019), lovasz-softmax-loss, and dice-loss(both generalized soft dice loss and batch soft dice loss). Maybe this is useful in my future work.


Also tried to implement swish, hard-swish(hswish) and mish activation functions.

Additionally, cuda based one-hot function is added (support label smooth).

Newly add an "Exponential Moving Average(EMA)" operator.

Add convolution ops, such as coord-conv2d, and dynamic-conv2d(dy-conv2d).

Some operators are implemented with pytorch cuda extension, so you need to compile it first: 
```
    $ python setup.py install
```

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
