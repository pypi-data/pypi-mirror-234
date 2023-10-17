from __future__ import annotations

from typing import List
from typing import Optional

from pydantic import BaseModel

from cval_lib.models._base import ExecModel, fields


@fields(
    'img_external_id: str',
    'img_label: int',
)
class Label(BaseModel):
    """
    :param img_external_id: img\'s external dataset_id
    :param img_label: img\'s label
    """
    img_external_id: str
    img_label: int



@fields(
    'segmentation: list',
    'area: float',
    'iscrowd: int',
    'image_id: int',
    'bbox: List[float]',
    'category_id: int',
    'id: int'
)
class Annotation(BaseModel):
    segmentation: List
    area: float
    iscrowd: int
    image_id: int
    bbox: List[float]
    category_id: int
    id: int


@fields(
    'license: int',
    'file_name: str',
    'coco_url: str',
    'height: int',
    'width: int',
    'date_captured: str',
    'flickr_url: str',
    'id: int',
)
class Image(BaseModel):
    license: int
    file_name: str
    coco_url: str
    height: int
    width: int
    date_captured: str
    flickr_url: str
    id: int


@fields(
    'supercategory: str',
    'id: int',
    'name: str',
)
class Category(BaseModel):
    supercategory: str
    id: int
    name: str


@fields(
    'description: str',
    'url: str',
    'version: str',
    'year: int',
    'contributor: str',
    'date_created: str',
)
class Info(BaseModel):
    description: str
    url: str
    version: str
    year: int
    contributor: str
    date_created: str


@fields(
    'url: str',
    'id: int',
    'name: str',
)
class License(BaseModel):
    url: str
    id: int
    name: str


@fields(
    'annotations: List[Annotation]',
    'images: List[Image]',
    'categories: List[Category]',
    'info: Info',
    'licenses: List[License]',
)
class DetectionAnnotationCOCO(ExecModel):
    """
    cocodataset annotation model
    https://haobin-tan.netlify.app/ai/computer-vision/object-detection/coco-dataset-format/
    """
    annotations: List[Annotation]
    images: List[Image]
    categories: List[Category]
    info: Info
    licenses: List[License]

    def send(self, user_api_key: str, dataset_id: str, sync: bool = True):
        return self._send(user_api_key, f'/dataset/{dataset_id}/annotation/detection', sync)


@fields(
    'train_labels: Optional[List[Label]]',
    'val_labels: Optional[List[Label]]',
    'test_labels: Optional[List[Label]]',
)
class ClassificationLabels(ExecModel):
    train_labels: Optional[List[Label]]
    val_labels: Optional[List[Label]]
    test_labels: Optional[List[Label]]

    def send(self, user_api_key: str, dataset_id: str, sync: bool = True):
        return self._send(user_api_key, f'/dataset/{dataset_id}/annotation/classification', sync)


@fields(
    'dataset_id: str',
    'labels_quantity: int',
    'labels: List[Label]',
)
class LabelsResponse(BaseModel):
    """
    :param dataset_id: id of the dataset
    :param labels_quantity: number of labels
    """
    dataset_id: str
    labels_quantity: int
    labels: List[Label]
