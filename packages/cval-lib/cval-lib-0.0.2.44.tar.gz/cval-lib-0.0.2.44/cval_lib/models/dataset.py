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
from pydantic import BaseModel, Field

from cval_lib.models._base import ExecModel, fields


@fields(
    'dataset_name: Optional[str]',
    'dataset_description: Optional[str]',
)
class DatasetModel(ExecModel):
    """
    :param dataset_name: the name of dataset
    :param dataset_description: the description of dataset
    :raises pydantic.error_wrappers.ValidationError:
    if len(dataset_name) > 32 or len(dataset_description) > 256
    """
    dataset_name: Optional[str] = Field(max_length=32, )
    dataset_description: Optional[str] = Field(max_length=256, )

    def send(self, user_api_key: str, dataset_id: str = None, sync: bool = True):
        return self._send(
            user_api_key,
            f'/dataset{f"/{dataset_id}" if dataset_id is not None else ""}',
            sync,
            method='post' if dataset_id is None else 'put'
        )


@fields(
    'dataset_id: str',
)
class DatasetDefaultResponse(BaseModel):
    """
    :param dataset_id: id of dataset
    """
    dataset_id: str


@fields(
    'dataset_id: str',
    'dataset_description: str',
    'dataset_name: str',
)
class DatasetResponse(DatasetModel):
    """
    :param dataset_id: id of dataset
    :param dataset_name: the name of dataset
    :param dataset_description: the description of dataset
    :raises pydantic.error_wrappers.ValidationError:
    if len(dataset_name) > 32 or len(dataset_description) > 256
    """
    dataset_id: str
