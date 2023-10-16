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

from typing import Any, Optional

from pydantic import BaseModel

from cval_lib.models._base import fields
from cval_lib.models.queue import QueueInfo


@fields(
    'weights_id: str',
    'retrain_model: bool',
    'old_weights_version: str',
    'new_weights_version: str',
)
class WeightsConfigResponse(BaseModel):
    """
    :param weights_id: id of weights
    :param retrain_model: use model retrain
    :param old_weights_version: previous weights version
    :param new_weights_version: current weights version
    """
    weights_id: str
    retrain_model: bool
    old_weights_version: str
    new_weights_version: str


@fields(
    'weights_id: Optional[str]',
    'version: Optional[str]'
)
class WeightsSimpleResponse(BaseModel):
    """
    :param weights_id: id of weights
    :param version: current weights version
    """
    weights_id: Optional[str]
    version: Optional[str]


@fields(
    'task_id: str',
    'dataset_id: Optional[str]',
    'time_start: float',
    'time_end: Optional[float]',
    'type_of_task: str',
    'action: str',
    'weights: Optional[WeightsConfigResponse]',
    'result: Any',
)
class ResultResponse(BaseModel):
    """
    :param task_id: id of result for polling
    :param dataset_id: id of dataset
    :param time_start: starting unix timestamp
    :param time_end: ending unix timestamp
    :param type_of_task: type of task: detection, classification
    :param action: action of result: sampling or test
    :param weights: weights of result
    """
    task_id: str
    dataset_id: Optional[str]
    time_start: float
    time_end: Optional[float]
    type_of_task: str
    action: str
    weights: Optional[WeightsConfigResponse]
    result: Any
    queue_info: Optional[QueueInfo]
