"""
Introducing CVAL Rest API, a powerful tool for AI developers in the computer vision field.
Our service combines the concepts of human-in-the-loop and active learning to improve the quality of
your models and minimize annotation costs for classification, detection, and segmentation cases.

With CVAL, you can iteratively improve your models by following our active learning loop.
First, manually or semi-automatically annotate a random set of images.
Next, train your model and use uncertainty and diversity methods to score the remaining images for annotation.
Then, manually or semi-automatically annotate the images marked as more confident to increase the accuracy of the model.
Repeat this process until you achieve an acceptable quality of the model.

Our service makes it easy to implement this workflow and improve your models quickly and efficiently.
Try our demo notebook to see how CVAL can revolutionize your computer vision projects.

To obtain a client_api_key, please send a request to k.suhorukov@digital-quarters.com
"""
from __future__ import annotations

from typing import List, Optional
from pydantic import validator

from pydantic import BaseModel, Field

from cval_lib.models._base import ExecModel, fields
from cval_lib.models.weights import WeightsConfigModel


@fields(
    'category_id: Optional[int]',
    'score: Optional[float]',
    'embedding_id: Optional[str]',
    'probabilities: Optional[List[float]]',
)
class BBoxScores(BaseModel):
    """
    :param category_id: id of the category in FramePrediction namespace
    :param score: prediction of model on that bbox
    :param embedding_id: id of the embedding
    :param probabilities: the probabilities for each object category are relative to a predicted bounding box
    The order in the list is determined by the category number. sum must be = 1
    """
    category_id: Optional[int]
    score: Optional[float]
    embedding_id: Optional[str]
    probabilities: Optional[List[float]]

    @validator('score')
    def validate_score(cls, value):
        if not (0 < value < 1):
            raise ValueError('the predicted score should be in the range (0, 1)')
        return value

    @validator('probabilities')
    def validate_probabilities(cls, value: Optional[List[float]]):
        if value is not None:
            for prob in value:
                if prob < 0:
                    raise ValueError('Each probability must be > 0')
        return value


@fields(
    'frame_id: str',
    'predictions: Optional[List[BBoxScores]]'
)
class FramePrediction(BaseModel):
    """
    :param frame_id: id of the frame
    :param predictions: bbox scores
    """
    frame_id: str = Field(max_length=32)
    predictions: Optional[List[BBoxScores]]


@fields(
    'num_of_samples: int',
    'dataset_id: Optional[str]',
    'use_null_detections: bool = True',
    'bbox_selection_policy: Optional[str]',
    'selection_strategy: str',
    'sort_strategy: Optional[str]',
    'frames: List[FramePrediction]',
    'probs_weights: Optional[List[float]]',
)
class DetectionSamplingOnPremise(ExecModel):
    """
    :param num_of_samples: absolute number of samples to select
    :param bbox_selection_policy:
    Which bounding box to select when there are multiple boxes on an image,
    according to their confidence.
    Supports: min, max, mean
    :param selection_strategy: Currently supports: margin, least, ratio, entropy, clustering
    :param probs_weights:
    Determines the significance (weight) of the prediction probability for each class.
    The order in the list corresponds to the order of the classes.
    It is essential for a multi-class entropy method.
    :param frames: prediction for th picture and the bbox
    :type frames: List[FramePrediction]
    :raises ValueError if value not in allowed
    """
    num_of_samples: int
    dataset_id: Optional[str]
    use_null_detections: bool = True
    bbox_selection_policy: Optional[str]
    selection_strategy: str
    sort_strategy: Optional[str]
    frames: List[FramePrediction]
    probs_weights: Optional[List[float]]

    def send(self, user_api_key: str, sync: bool = True):
        return self._send(user_api_key, '/api/on-premise/sampling/detection', sync)


@fields(
    'weights_of_model: Optional[WeightsConfigModel]',
    'model: Optional[str]',
    'use_pretrain_model: Optional[bool]',
)
class DetectionTest(ExecModel):
    """
    model: type of the model. Currently, supports: ...
    pretrain: Whether to use a pre-trained model or not
    :raises ValueError if value not in allowed
    """
    weights_of_model: Optional[WeightsConfigModel]
    model: Optional[str]
    use_pretrain_model: Optional[bool]

    def send(self, user_api_key: str, dataset_id: str, sync: bool = True):
        return self._send(user_api_key, f'/dataset/{dataset_id}/test/detection', sync)


@fields(
    'num_samples: int',
    'selection_strategy: str',
    'batch_unlabeled: int = -1',
    'use_pretrain_model: bool = True',
    'use_backbone_freezing: bool = False',
    'bbox_selection_policy: str',
    'bbox_selection_quantile_range: list[float]',
)
class DetectionSampling(DetectionTest):
    """
    :param num_samples: absolute number of samples to select
    :param batch_unlabeled: the limit of unlabeled samples that can be processed during selection
    :param selection_strategy:  strategy. Currently, supports ...
    :param use_pretrain_model: Whether to use a pre-trained model or not
    :param use_backbone_freezing: Whether to use backbone freezing in the training process
    :param bbox_selection_policy:
    which bounding box to select when there are multiple boxes on an image,
    according to their confidence. Currently, supports: min, max, sum
    :bbox_selection_quantile_range:
    in what range of confidence will the bbox selection policy be applied
    """
    num_samples: int
    selection_strategy: str
    batch_unlabeled: int = -1
    use_pretrain_model: bool = True
    use_backbone_freezing: bool = False
    bbox_selection_policy: str
    bbox_selection_quantile_range: List[float]

    def send(self, user_api_key: str, dataset_id: str, sync: bool = True):
        return self._send(user_api_key, f'/dataset/{dataset_id}/sampling/detection', sync)
