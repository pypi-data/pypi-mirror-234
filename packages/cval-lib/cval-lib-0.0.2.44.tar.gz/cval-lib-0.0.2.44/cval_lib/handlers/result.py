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
from cval_lib.models.queue import QueueInfo
from cval_lib.models.result import ResultResponse


class Result(AbstractHandler):
    """
    The result is the entity in which the processing data is stored
    """
    def __init__(
            self,
            session: Session,
            **kwargs,
    ):
        self.route = f'{MainConfig.main_url}/result'
        self.task_id = None
        super().__init__(session, )

    def _set_task_id(self, task_id: str = None):
        if task_id is None:
            task_id = self.task_id
        if task_id is None:
            raise ValueError('task_id cannot be None')
        self.task_id = task_id

    def get(self, task_id: str = None) -> ResultResponse:
        """
        returns the result value
        :param task_id: id of result
        :return: ResultResponse
        """
        self._set_task_id(task_id)
        self._get(self.route + f'/{self.task_id}')
        return ResultResponse.parse_obj(self.send().json())

    def get_many(self, dataset_id: str = None, limit=100, ) -> List[ResultResponse]:
        """
        returns the result value Iterable
        :param dataset_id: id of dataset
        :param limit: limit of returned objects
        :return:
        """
        self._get(self.route + 's', params={'limit': limit, 'dataset_id': dataset_id})
        return [ResultResponse.parse_obj(i) for i in self.send().json()]

    def queue(self) -> QueueInfo:
        self._get(MainConfig.main_url + '/api/queue')
        return QueueInfo.parse_obj(self.send())
