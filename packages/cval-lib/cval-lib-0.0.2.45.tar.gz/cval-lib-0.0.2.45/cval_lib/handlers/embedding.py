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

from requests import Session, Response

from cval_lib.configs.main_config import MainConfig
from cval_lib.handlers._abstract_handler import AbstractHandler
from cval_lib.models.embedding import FrameEmbeddingModel, EmbeddingsMetaResponse


class Embedding(AbstractHandler):
    """
    Embeddings are vector representations of images
    obtained using pytorch or any other library
    """

    def __init__(
            self,
            session: Session,
            dataset_id: str = None,
            part_of_dataset: str = None,
            _is_not_second=True,
    ):
        if _is_not_second and dataset_id is None:
            raise ValueError('dataset_id must be not None')
        if _is_not_second and part_of_dataset is None:
            raise ValueError('part_of_dataset must be not None')
        self.dataset_id = dataset_id
        self.part_of_dataset = part_of_dataset
        self.route = f'{MainConfig().main_url}/dataset/{dataset_id}/{part_of_dataset}/'
        super().__init__(session)

    def monkey_patch_url(self, part_of_dataset: str, ) -> 'Embedding':
        self.part_of_dataset = part_of_dataset
        return self

    def get_meta(self, start_limit: int = 0, stop_limit: int = 1000) -> 'EmbeddingsMetaResponse':
        """
        :param start_limit: upper limit of items
        :param stop_limit: lower limit of items
        :return: List[ImageEmbeddingModel]
        """
        self._get(f'{MainConfig.main_url}/dataset/{self.dataset_id}/{self.part_of_dataset}/embeddings/meta',
                  params={'start_limit': start_limit, 'stop_limit': stop_limit})
        return EmbeddingsMetaResponse.parse_obj(self.send().json())

    def get_many(self, start_limit: int = 0, stop_limit: int = 1000) -> List['FrameEmbeddingModel']:
        """
        :param start_limit: upper limit of items
        :param stop_limit: lower limit of items
        :return: List[ImageEmbeddingModel]
        """
        self._get(f'{MainConfig.main_url}/dataset/{self.dataset_id}/{self.part_of_dataset}/embeddings',
                  params={'start_limit': start_limit, 'stop_limit': stop_limit})
        return [FrameEmbeddingModel.parse_obj(i) for i in self.send().json()]

    def get_by_id(
            self,
            frame_id: str,
            embedding_id: str,
    ) -> 'FrameEmbeddingModel':
        """
        :param embedding_id: id of embedding
        :param frame_id: id of frame
        :return: ImageEmbeddingModel
        """
        self._get(self.route + f'/embedding/{frame_id}/{embedding_id}')
        return FrameEmbeddingModel.parse_obj(self.send().json())

    def upload_many(self, embeddings: List[FrameEmbeddingModel]) -> 'EmbeddingsMetaResponse':
        """
        :param embeddings: List[ImageEmbeddingModel]
        :return: Response, This method does not return anything useful to use, but performs an action
        """
        self._post(
            f'{MainConfig.main_url}/dataset/{self.dataset_id}/{self.part_of_dataset}/embeddings',
            json=[i.dict() if not isinstance(i, dict) else i for i in embeddings]
        )
        return EmbeddingsMetaResponse.parse_obj(self.send().json())

    def delete_all(self, ) -> Response:
        """
        :return: Response, This method does not return anything useful to use, but performs an action
        """
        self._delete(self.route + 'embeddings')
        return self.send()

    def delete_by_id(self, frame_id: str, embedding_id: str = 'all') -> Response:
        """
        :param embedding_id: id of embedding
        :param frame_id: id of frame
        :return: Response, This method does not return anything useful to use, but performs an action
        """
        self._delete(self.route + f'embedding/{frame_id}/{embedding_id}')
        return self.send()
