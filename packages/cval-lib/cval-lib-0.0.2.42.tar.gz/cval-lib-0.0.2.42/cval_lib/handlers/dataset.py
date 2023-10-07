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

from typing import List

from requests import Session

from cval_lib.configs.main_config import MainConfig
from cval_lib.handlers._abstract_handler import AbstractHandler
from cval_lib.handlers.detection import Detection
from cval_lib.handlers.embedding import Embedding
from cval_lib.handlers.result import Result
from cval_lib.models.dataset import DatasetModel, DatasetResponse


class Dataset(AbstractHandler):
    """
    Within the framework of the created system,
    datasets are spaces in which data for machine learning is stored.
    Creating a dataset is similar to creating a folder.
    """

    def __init__(self, session: Session):
        self.dataset_request = DatasetModel(dataset_name='', dataset_description='')
        self.route = f'{MainConfig().main_url}/dataset'
        self.dataset_id = None
        self.result = Result(session)
        self._embedding = Embedding(session, _is_not_second=False)
        self.embedding = self._embedding.monkey_patch_url
        self.detection = Detection(session)
        super().__init__(session)

    def __repr__(self):
        return f'<dataset {self.dataset_id}>'

    def _construct_request(self, name: str, description: str):
        self.dataset_request = DatasetModel()
        if name is not None:
            self.dataset_request.dataset_name = name
        if description is not None:
            self.dataset_request.dataset_description = description

    def create(
            self,
            name: str = None,
            description: str = None,
    ) -> str:
        """
        this method creates a dataset
        :param name: the name of dataset
        :param description: the name of dataset
        :return: id of dataset (dataset_id)
        """
        self._construct_request(name, description)
        self._post(url=self.route, json=self.dataset_request.dict())
        self.dataset_id = self.send().json().get('dataset_id')
        self._embedding.dataset_id = self.dataset_id
        return self.dataset_id

    def update(
            self,
            dataset_id: str = None,
            name: str = None,
            description: str = None,
    ) -> 'DatasetModel':
        """
        this method updates a dataset
        :param dataset_id: id of dataset
        :param name: the name of dataset
        :param description: the description of dataset
        :return: DatasetResponse model with updates
        """
        dataset_id = self.set_dataset_id(dataset_id)
        self._construct_request(name, description)
        self._put(url=self.route + f'/{dataset_id}', json=self.dataset_request.dict(), )
        self.dataset_request = self.send().json()
        return self.dataset_request

    def set_dataset_id(self, dataset_id: str = None):
        if dataset_id is None:
            dataset_id = self.dataset_id
        self.dataset_id = dataset_id
        if self.dataset_id is None:
            raise ValueError('dataset_id cannot be None')
        self._embedding.dataset_id = dataset_id
        return self.dataset_id

    def get(
            self,
            dataset_id: str = None,
    ) -> 'DatasetModel':
        """
        this method returns a dataset name and description by dataset_id
        :param dataset_id: id of dataset
        :return: DatasetResponse model with updates
        """
        dataset_id = self.set_dataset_id(dataset_id)
        self._get(url=self.route + f'/{dataset_id}')
        return DatasetModel.parse_obj(self.send().json())

    def get_all(
            self,
            name: str = None,
            description: str = None,
    ) -> List['DatasetResponse']:
        """
        this method returns a dataset name and description by dataset_id
        :param name: the name of dataset. regexp
        :param description: the description of dataset. regexp
        :return: DatasetResponse model with updates
        """
        self._construct_request(name, description)
        self._get(url=self.route + 's/all', params=self.dataset_request.dict())
        return [DatasetResponse.parse_obj(i) for i in self.send().json()]
