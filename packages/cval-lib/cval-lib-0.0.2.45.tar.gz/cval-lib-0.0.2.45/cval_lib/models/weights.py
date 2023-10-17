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

from typing import Optional

from pydantic import BaseModel

from typing import List

from cval_lib.models._base import fields


@fields(
    'weights_id: str',
    'retrain_model: bool = False',
    'weights_version: Optional[str]',
)
class WeightsConfigModel(BaseModel):
    """
    :param weights_id: weights ID to be used in active learning
    :param retrain_model: perform a model retrain
    :param weights_version: Weights Version to be used in the operation
    """
    weights_id: str
    retrain_model: bool = False
    weights_version: Optional[str]


@fields(
    'ID: str',
    'timestamp: float',
    'ver: str',
    'task_id: str',
)
class Version(BaseModel):
    """
    :param ID: internal id of version
    :param timestamp: UNIX timestamp creation time
    :param ver: version
    :param task_id: id of task
    """
    ID: str
    timestamp: float
    ver: str
    task_id: str


@fields(
    'ID: str',
    'model: float',
)
class WeightsOfModel(BaseModel):
    ID: str
    model: str


@fields(
    'weights_of_model: WeightsOfModel',
    'versions: List[Version]',
)
class WeightsBase(BaseModel):
    """
    :param weights_of_model: internal id of version
    :param versions: list of versions
    """
    weights_of_model: WeightsOfModel
    versions: List[Version]
