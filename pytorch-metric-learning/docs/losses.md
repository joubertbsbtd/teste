# Losses
All loss functions are used as follows:

```python
from pytorch_metric_learning import losses
loss_func = losses.SomeLoss()
loss = loss_func(embeddings, labels)
```

Or if you are using a loss in conjunction with a miner:

```python
from pytorch_metric_learning import miners, losses
miner_func = miners.SomeMiner()
loss_func = losses.SomeLoss()
miner_output = miner_func(embeddings, labels)
losses = loss_func(embeddings, labels, miner_output)
```

## AngularLoss 
[Deep Metric Learning with Angular Loss](https://arxiv.org/pdf/1708.01682.pdf)

```python
losses.AngularLoss(alpha,**kwargs)
```

**Parameters**:

* **alpha**: The angle (as described in the paper), specified in degrees.


## ArcFaceLoss 
[ArcFace: Additive Angular Margin Loss for Deep Face Recognition](https://arxiv.org/pdf/1801.07698.pdf)

```python
losses.ArcFaceLoss(margin, num_classes, embedding_size, scale=64, **kwargs)
```

**Parameters**:

* **margin**: The angular margin penalty in degrees. 
* **num_classes**: The number of classes in your training dataset.
* **embedding_size**: The size of the embeddings that you pass into the loss function. For example, if your batch size is 128 and your network outputs 512 dimensional embeddings, then set ```embedding_size``` to 512.
* **scale**: The exponent multiplier in the loss's softmax expression. (This is the inverse of the softmax temperature.)

**Other info**: 

* This also extends [WeightRegularizerMixin](losses.md#weightregularizermixin), so it accepts a ```regularizer``` and ```reg_weight``` as optional init arguments.
* This loss **requires an optimizer**. You need to create an optimizer and pass this loss's parameters to that optimizer. For example:
```python
loss_func = losses.ArcFaceLoss(...)
loss_optimizer = torch.optim.SGD(loss_func.parameters(), lr=0.01)
# then during training:
loss_optimizer.step()
```

## BaseMetricLossFunction
All loss functions extend this class and therefore inherit its ```__init__``` parameters.

```python
losses.BaseMetricLossFunction(normalize_embeddings=True, num_class_per_param=None, learnable_param_names=None)
```

**Parameters**:

* **normalize_embeddings**: If True, embeddings will be normalized to have a Euclidean norm of 1 before the loss is computed.
* **num_class_per_param**: If _learnable_param_names_ is set, then this represents the number of classes for each parameter. If your parameters don't have a separate value for each class, then you can leave this at None.
* **learnable_param_names**: A list of strings where each element is the name of attributes that should be converted to nn.Parameter. If None, then no parameters are converted. 

**Required Implementations**:
```python
def compute_loss(self, embeddings, labels, indices_tuple=None):
    raise NotImplementedError
```


## CircleLoss 
[Circle Loss: A Unified Perspective of Pair Similarity Optimization](https://arxiv.org/pdf/2002.10857.pdf)

```python
losses.CircleLoss(m=0.4, gamma=80, triplets_per_anchor='all', **kwargs)
```

**Parameters**:

* **m**:  The relaxation factor that controls the radious of the decision boundary.
* **gamma**: The scale factor that determines the largest scale of each similarity score.
* **triplets_per_anchor**: The number of triplets per element to sample within a batch. Can be an integer or the string "all". For example, if your batch size is 128, and triplets_per_anchor is 100, then 12800 triplets will be sampled. If triplets_per_anchor is "all", then all possible triplets in the batch will be used.


## ContrastiveLoss
```python
losses.ContrastiveLoss(pos_margin=0, 
					neg_margin=1, 
					use_similarity=False, 
					power=1, 
					avg_non_zero_only=True, 
					**kwargs):
```


**Parameters**:

* **pos_margin**: The distance (or similarity) over (under) which positive pairs will contribute to the loss.
* **neg_margin**: The distance (or similarity) under (over) which negative pairs will contribute to the loss.  
* **use_similarity**: If True, will use dot product between vectors instead of euclidean distance.
* **power**: Each pair's loss will be raised to this power.
* **avg_non_zero_only**: Only pairs that contribute non-zero loss will be used in the final loss. 

Note that the default values for ```pos_margin``` and ```neg_margin``` are suitable if ```use_similarity = False```. If you set ```use_similarity = True```, then more appropriate values would be ```pos_margin = 1``` and ```neg_margin = 0```.

## CosFaceLoss 
[CosFace: Large Margin Cosine Loss for Deep Face Recognition](https://arxiv.org/pdf/1801.09414.pdf)

```python
losses.CosFaceLoss(margin, num_classes, embedding_size, scale=64, **kwargs)
```

**Parameters**:

* **margin**: The cosine margin penalty: ```cos(theta) - margin```. The paper got optimal performance with margin values between 0.25 and 0.45.
* **num_classes**: The number of classes in your training dataset.
* **embedding_size**: The size of the embeddings that you pass into the loss function. For example, if your batch size is 128 and your network outputs 512 dimensional embeddings, then set ```embedding_size``` to 512.
* **scale**: The exponent multiplier in the loss's softmax expression. (This is the inverse of the softmax temperature.)

**Other info**: 

* This also extends [WeightRegularizerMixin](losses.md#weightregularizermixin), so it accepts a ```regularizer``` and ```reg_weight``` as optional init arguments.
* This loss **requires an optimizer**. You need to create an optimizer and pass this loss's parameters to that optimizer. For example:
```python
loss_func = losses.CosFaceLoss(...)
loss_optimizer = torch.optim.SGD(loss_func.parameters(), lr=0.01)
# then during training:
loss_optimizer.step()
```

## CrossBatchMemory 
This wraps a loss function, and implements [Cross-Batch Memory for Embedding Learning](https://arxiv.org/pdf/1912.06798.pdf). It stores embeddings from previous iterations in a queue, and uses them to form more pairs/triplets with the current iteration's embeddings.

```python
losses.CrossBatchMemory(loss, embedding_size, memory_size=1024, miner=None)
```

**Parameters**:

* **loss**: The loss function to be wrapped. For example, you could pass in ```ContrastiveLoss()```.
* **embedding_size**: The size of the embeddings that you pass into the loss function. For example, if your batch size is 128 and your network outputs 512 dimensional embeddings, then set ```embedding_size``` to 512.
* **memory_size**: The size of the memory queue.
* **miner**: An optional [tuple miner](miners.md), which will be used to mine pairs/triplets from the memory queue.


## FastAPLoss
[Deep Metric Learning to Rank](http://openaccess.thecvf.com/content_CVPR_2019/papers/Cakir_Deep_Metric_Learning_to_Rank_CVPR_2019_paper.pdf)

```python
losses.FastAPLoss(num_bins, **kwargs)
```

**Parameters**:

* **num_bins**: The number of soft histogram bins for calculating average precision

## GenericPairLoss
```python
losses.GenericPairLoss(use_similarity, mat_based_loss, squared_distances=False, **kwargs)
```

**Parameters**:

* **use_similarity**: Set to True if the loss function uses pairwise similarity (dot product of each embedding pair). Otherwise, euclidean distance will be used.
* **mat_based_loss**: See required implementations.
* **squared_distances**: If True, then the euclidean distance will be squared.

**Required Implementations**:
```python
# If mat_based_loss is True, then this takes in mat, pos_mask, and neg_mask
# If False, this takes in pos_pairs and neg_pairs
def _compute_loss(self):
    raise NotImplementedError
```

## GeneralizedLiftedStructureLoss

```python
losses.GeneralizedLiftedStructureLoss(neg_margin, **kwargs)
```

**Parameters**:

* **neg_margin**: The margin in the expression ```e^(margin - negative_distance)```

## IntraPairVarianceLoss
[Deep Metric Learning with Tuplet Margin Loss](http://openaccess.thecvf.com/content_ICCV_2019/papers/Yu_Deep_Metric_Learning_With_Tuplet_Margin_Loss_ICCV_2019_paper.pdf)
```python
losses.IntraPairVarianceLoss(pos_eps=0.01, neg_eps=0.01, **kwargs)
```

**Parameters**:

* **pos_eps**: The offset in the expression ```(1-pos_eps)*mu_ap - cos(theta_ap)```. See equation 15 in the paper.
* **neg_eps**: The offset in the expression ```cos(theta_an) - (1+neg_eps)*mu_an```. See equation 16 in the paper.

You should probably use this in conjunction with another loss, as described in the paper. You can accomplish this by using [MultipleLosses](losses.md#multiplelosses):
```python
main_loss = losses.TupletMarginLoss(margin=5)
var_loss = losses.IntraPairVarianceLoss()
complete_loss = losses.MultipleLosses([main_loss, var_loss], weights=[1, 0.5])
```

## LargeMarginSoftmaxLoss
[Large-Margin Softmax Loss for Convolutional Neural Networks](https://arxiv.org/pdf/1612.02295.pdf)

```python
losses.LargeMarginSoftmaxLoss(margin, num_classes, embedding_size, scale=1, normalize_weights=False, **kwargs)
```

**Parameters**:

* **margin**: An integer which dictates the size of the angular margin. Specifically, it multiplies the angle between the embeddings and weights: ```cos(margin*theta)```. 
* **num_classes**: The number of classes in your training dataset.
* **embedding_size**: The size of the embeddings that you pass into the loss function. For example, if your batch size is 128 and your network outputs 512 dimensional embeddings, then set ```embedding_size``` to 512.
* **scale**: The exponent multiplier in the loss's softmax expression. (This is the inverse of the softmax temperature.)
* **normalize_weights**: If True, the learned weights will be normalized to have Euclidean norm of 1, before the loss is computed. Note that when this parameter is True, it becomes equivalent to [SphereFaceLoss](losses.md#spherefaceloss).

**Other info**: 

* This also extends [WeightRegularizerMixin](losses.md#weightregularizermixin), so it accepts a ```regularizer``` and ```reg_weight``` as optional init arguments.
* This loss **requires an optimizer**. You need to create an optimizer and pass this loss's parameters to that optimizer. For example:
```python
loss_func = losses.LargeMarginSoftmaxLoss(...)
loss_optimizer = torch.optim.SGD(loss_func.parameters(), lr=0.01)
# then during training:
loss_optimizer.step()
```

## MarginLoss
[Sampling Matters in Deep Embedding Learning](https://arxiv.org/pdf/1706.07567.pdf)
```python
losses.MarginLoss(margin, nu, beta, triplets_per_anchor="all", **kwargs)
```

**Parameters**:

* **margin**: The radius of the minimalbuffer between positive and negative pairs.
* **nu**: The regularization weight for the magnitude of beta.
* **beta**: The center of the minimal buffer between positive and negative pairs.
* **triplets_per_anchor**: The number of triplets per element to sample within a batch. Can be an integer or the string "all". For example, if your batch size is 128, and triplets_per_anchor is 100, then 12800 triplets will be sampled. If triplets_per_anchor is "all", then all possible triplets in the batch will be used.

To make beta a learnable parameter (as done in the paper), pass in the keyword argument:
```python
learnable_param_names=["beta"]
```
You can then pass the loss function's parameters() to any PyTorch optimizer.

## MultipleLosses
This is a simple wrapper for multiple losses. Pass in a list of already-initialized loss functions. Then, when you call forward on this object, it will return the sum of all wrapped losses.
```python
losses.MultipleLosses(losses, weights=None)
```
**Parameters**:

* **losses**: A list of initialized loss functions. On the forward call of MultipleLosses, each wrapped loss will be computed, and then the average will be returned.
* **weights**: Optional. A list of loss weights, which will be multiplied by the corresponding losses obtained by the loss functions. The default is to multiply each loss by 1.

## MultiSimilarityLoss
[Multi-Similarity Loss with General Pair Weighting for Deep Metric Learning](http://openaccess.thecvf.com/content_CVPR_2019/papers/Wang_Multi-Similarity_Loss_With_General_Pair_Weighting_for_Deep_Metric_Learning_CVPR_2019_paper.pdf)
```python
losses.MultiSimilarityLoss(alpha, beta, base=0.5, **kwargs)
```
**Parameters**:

* **alpha**: The weight applied to positive pairs.
* **beta**: The weight applied to negative pairs.
* **base**: The offset applied to the exponent in the loss.


## NCALoss
[Neighbourhood Components Analysis](https://www.cs.toronto.edu/~hinton/absps/nca.pdf)
```python
losses.NCALoss(softmax_scale=1, **kwargs)
```

**Parameters**:

* **softmax_scale**: The exponent multiplier in the loss's softmax expression. (This is the inverse of the softmax temperature.)

## NormalizedSoftmaxLoss
[Classification is a Strong Baseline for Deep Metric Learning](https://arxiv.org/pdf/1811.12649.pdf)
```python
losses.NormalizedSoftmaxLoss(temperature, embedding_size, num_classes, **kwargs)
```
**Parameters**:

* **temperature**: The exponent divisor in the softmax funtion.
* **embedding_size**: The size of the embeddings that you pass into the loss function. For example, if your batch size is 128 and your network outputs 512 dimensional embeddings, then set ```embedding_size``` to 512.
* **num_classes**: The number of classes in your training dataset.

**Other info**

* This also extends [WeightRegularizerMixin](losses.md#weightregularizermixin), so it accepts a ```regularizer``` and ```reg_weight``` as optional init arguments.
* This loss **requires an optimizer**. You need to create an optimizer and pass this loss's parameters to that optimizer. For example:
```python
loss_func = losses.NormalizedSoftmaxLoss(...)
loss_optimizer = torch.optim.SGD(loss_func.parameters(), lr=0.01)
# then during training:
loss_optimizer.step()
```

## NPairsLoss
[Improved Deep Metric Learning with Multi-class N-pair Loss Objective](http://www.nec-labs.com/uploads/images/Department-Images/MediaAnalytics/papers/nips16_npairmetriclearning.pdf)
```python
losses.NPairsLoss(l2_reg_weight=0, **kwargs)
```

**Parameters**:

* **l2_reg_weight**: The regularization weight for the L2 norm of the embeddings.

## NTXentLoss
This is the normalized temperature-scaled cross entropy loss used in [A Simple Framework for Contrastive Learning of Visual Representations](https://arxiv.org/abs/2002.05709).
```python
losses.NTXentLoss(temperature, **kwargs)
```

**Parameters**:

* **temperature**: The exponent divisor in the softmax funtion.

## ProxyAnchorLoss
[Proxy Anchor Loss for Deep Metric Learning](https://arxiv.org/pdf/2003.13911.pdf)
```python
losses.ProxyAnchorLoss(num_classes, embedding_size, margin = 0.1, alpha = 32, **kwargs)
```

**Parameters**:

* **num_classes**: The number of classes in your training dataset.
* **embedding_size**: The size of the embeddings that you pass into the loss function. For example, if your batch size is 128 and your network outputs 512 dimensional embeddings, then set ```embedding_size``` to 512.
* **margin**: This is subtracted from the cosine similarity of positive pairs, and added to the cosine similarity of negative pairs. See delta in equation 4 of the paper.
* **alpha**: This is the multiplier in the exponent of the LogSumExp expression. See equation 4 in the paper.

**Other info**

* This also extends [WeightRegularizerMixin](losses.md#weightregularizermixin), so it accepts a ```regularizer``` and ```reg_weight``` as optional init arguments.
* This loss **requires an optimizer**. You need to create an optimizer and pass this loss's parameters to that optimizer. For example:
```python
loss_func = losses.ProxyAnchorLoss(...)
loss_optimizer = torch.optim.SGD(loss_func.parameters(), lr=0.01)
# then during training:
loss_optimizer.step()
```

## ProxyNCALoss
[No Fuss Distance Metric Learning using Proxies](https://arxiv.org/pdf/1703.07464.pdf)
```python
losses.ProxyNCALoss(num_classes, embedding_size, **kwargs)
```

**Parameters**:

* **num_classes**: The number of classes in your training dataset.
* **embedding_size**: The size of the embeddings that you pass into the loss function. For example, if your batch size is 128 and your network outputs 512 dimensional embeddings, then set ```embedding_size``` to 512.
* **softmax_scale**: See [NCALoss](losses.md#ncaloss)

**Other info**

* This also extends [WeightRegularizerMixin](losses.md#weightregularizermixin), so it accepts a ```regularizer``` and ```reg_weight``` as optional init arguments.
* This loss **requires an optimizer**. You need to create an optimizer and pass this loss's parameters to that optimizer. For example:
```python
loss_func = losses.ProxyNCALoss(...)
loss_optimizer = torch.optim.SGD(loss_func.parameters(), lr=0.01)
# then during training:
loss_optimizer.step()
```

## SignalToNoiseRatioContrastiveLoss
[Signal-to-Noise Ratio: A Robust Distance Metric for Deep Metric Learning](http://openaccess.thecvf.com/content_CVPR_2019/papers/Yuan_Signal-To-Noise_Ratio_A_Robust_Distance_Metric_for_Deep_Metric_Learning_CVPR_2019_paper.pdf)
```python
losses.SignalToNoiseRatioContrastiveLoss(pos_margin, 
										neg_margin, 
										regularizer_weight, 
										avg_non_zero_only=True, 
										**kwargs)
```

**Parameters**:

* **pos_margin**: The noise-to-signal ratio over which positive pairs will contribute to the loss.
* **neg_margin**: The noise-to-signal ratio under which negative pairs will contribute to the loss.
* **regularizer_weight**: The regularizer encourages the embeddings to have zero-mean distributions. 
* **avg_non_zero_only**: Only pairs that contribute non-zero loss will be used in the final loss. 

## SoftTripleLoss   
[SoftTriple Loss: Deep Metric Learning Without Triplet Sampling](http://openaccess.thecvf.com/content_ICCV_2019/papers/Qian_SoftTriple_Loss_Deep_Metric_Learning_Without_Triplet_Sampling_ICCV_2019_paper.pdf)
```python
losses.SoftTripleLoss(embedding_size, 
					num_classes, 
					centers_per_class, 
					la=20, 
					gamma=0.1, 
					reg_weight=0.2, 
					margin=0.01, 
					**kwargs)
```

**Parameters**:

* **embedding_size**: The size of the embeddings that you pass into the loss function. For example, if your batch size is 128 and your network outputs 512 dimensional embeddings, then set ```embedding_size``` to 512.
* **num_classes**: The number of classes in your training dataset.
* **centers_per_class**: The number of weight vectors per class. (The regular cross entropy loss has 1 center per class.)
* **la**: The exponent multiplier in the loss's softmax expression. (This is the inverse of the softmax temperature.)
* **gamma**: The similarity-to-centers multiplier.
* **reg_weight**: The regularization weight which encourages class centers to be close to each other.
* **margin**: The margin in the expression e^(similarities - margin).

**Other info**

* This loss **requires an optimizer**. You need to create an optimizer and pass this loss's parameters to that optimizer. For example:
```python
loss_func = losses.SoftTripleLoss(...)
loss_optimizer = torch.optim.SGD(loss_func.parameters(), lr=0.01)
# then during training:
loss_optimizer.step()
```

## SphereFaceLoss 
[SphereFace: Deep Hypersphere Embedding for Face Recognition](https://arxiv.org/pdf/1704.08063.pdf)

```python
losses.SphereFaceLoss(margin, num_classes, embedding_size, scale=1, **kwargs)
```

**Parameters**:

* **margin**: An integer which dictates the size of the angular margin. Specifically, it multiplies the angle between the embeddings and weights: ```cos(margin*theta)```. 
* **num_classes**: The number of classes in your training dataset.
* **embedding_size**: The size of the embeddings that you pass into the loss function. For example, if your batch size is 128 and your network outputs 512 dimensional embeddings, then set ```embedding_size``` to 512.
* **scale**: The exponent multiplier in the loss's softmax expression. (This is the inverse of the softmax temperature.)

**Other info**

* This also extends [WeightRegularizerMixin](losses.md#weightregularizermixin), so it accepts a ```regularizer``` and ```reg_weight``` as optional init arguments.
* This loss **requires an optimizer**. You need to create an optimizer and pass this loss's parameters to that optimizer. For example:
```python
loss_func = losses.SphereFaceLoss(...)
loss_optimizer = torch.optim.SGD(loss_func.parameters(), lr=0.01)
# then during training:
loss_optimizer.step()
```

## TripletMarginLoss

```python
losses.TripletMarginLoss(margin=0.05, 
						distance_norm=2, 
						power=1, 
						swap=False, 
						smooth_loss=False, 
						avg_non_zero_only=True, 
						triplets_per_anchor="all", 
						**kwargs)
```

**Parameters**:

* **margin**: The desired difference between the anchor-positive distance and the anchor-negative distance.
* **distance_norm**: The norm used when calculating distance between embeddings
* **power**: Each pair's loss will be raised to this power.
* **swap**: Use the positive-negative distance instead of anchor-negative distance, if it violates the margin more.
* **smooth_loss**: Use the log-exp version of the triplet loss
* **avg_non_zero_only**: Only triplets that contribute non-zero loss will be used in the final loss.
* **triplets_per_anchor**: The number of triplets per element to sample within a batch. Can be an integer or the string "all". For example, if your batch size is 128, and triplets_per_anchor is 100, then 12800 triplets will be sampled. If triplets_per_anchor is "all", then all possible triplets in the batch will be used.

## TupletMarginLoss
[Deep Metric Learning with Tuplet Margin Loss](http://openaccess.thecvf.com/content_ICCV_2019/papers/Yu_Deep_Metric_Learning_With_Tuplet_Margin_Loss_ICCV_2019_paper.pdf)
```python
losses.TupletMarginLoss(margin, scale=64, **kwargs)
```

**Parameters**:

* **margin**: The angular margin (in degrees) applied to positive pairs. The paper uses a value of 5.73 degrees (0.1 radians).
* **scale**: The exponent multiplier in the logsumexp expression.

The paper combines this loss with [IntraPairVarianceLoss](losses.md#intrapairvarianceloss). You can accomplish this by using [MultipleLosses](losses.md#multiplelosses):
```python
main_loss = losses.TupletMarginLoss(margin=5)
var_loss = losses.IntraPairVarianceLoss()
complete_loss = losses.MultipleLosses([main_loss, var_loss], weights=[1, 0.5])
```

## WeightRegularizerMixin
Losses can extend this class in addition to BaseMetricLossFunction. You should extend this class if your loss function can make use of a [weight regularizer](regularizers.md).
```python
losses.WeightRegularizerMixin(regularizer, reg_weight, **kwargs)
```

**Parameters**:

* **regularizer**: The [regularizer](regularizers.md) to apply to the loss's learned weights.
* **reg_weight**: The amount the regularization loss will be multiplied by.

Extended by:

* [ArcFaceLoss](losses.md#arcfaceloss)
* [CosFaceLoss](losses.md#cosfaceloss)
* [LargeMarginSoftmaxLoss](losses.md#largemarginsoftmaxloss)
* [NormalizedSoftmaxLoss](losses.md#normalizedsoftmaxloss)
* [ProxyAnchorLoss](losses.md#proxyanchorloss)
* [ProxyNCALoss](losses.md#proxyncaloss)
* [SphereFaceLoss](losses.md#spherefaceloss)