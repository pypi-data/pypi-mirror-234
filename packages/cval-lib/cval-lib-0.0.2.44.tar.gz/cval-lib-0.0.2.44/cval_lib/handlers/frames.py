from typing import Iterable

from requests import Session

from cval_lib.configs.main_config import MainConfig
from cval_lib.handlers._abstract_handler import AbstractHandler
from cval_lib.models.frame import FrameModel


class Frames(AbstractHandler):
    def __init__(
            self,
            session: Session,
            dataset_id: str,
            part_of_dataset: str = None,

    ):
        self.route = f'{MainConfig.main_url}/dataset/{dataset_id}/'
        self.part_of_dataset = part_of_dataset
        self.dataset_id = dataset_id
        super().__init__(session)

    @staticmethod
    def _validate(frames: Iterable[FrameModel]):
        return list(map(lambda x: x.dict(), filter(lambda x: x.img_link is not None, frames))) if frames else None

    def read_meta(self, limit: int = 100):
        if self.part_of_dataset is not None:
            return (
                self._get(
                    self.route + f'{self.part_of_dataset}/frames/meta',
                    stream=True,
                    params={'limit': limit},
                ), self.send())[-1]
        else:
            return [
                (self._get(
                    self.route + f'{part_of_dataset}/frames/meta',
                    stream=True,
                    params={'limit': limit},
                ), self.send().json())[-1]
                for part_of_dataset in ('test', 'training', 'validation')
            ]

    def create_fb(self, frames: Iterable[FrameModel]):
        """
        uploading images via blob data
        Based on: FrameModel(img_raw: bytes, img_external_id: str)
        :param frames: Image values in bytes
        """
        self._post(
            self.route + f'{self.part_of_dataset}/blob',
            files=tuple(map(lambda x: ('uploaded_files', x.img_raw), frames)),
            params={'frames_ids': ','.join(list(map(lambda x: x.img_external_id, frames)))},
        )
        return self.send()

    def create_fl(self, train: Iterable[FrameModel] = None, val: Iterable[FrameModel] = None,
                  test: Iterable[FrameModel] = None):
        """
        uploading images via links
        Based on: FrameModel(img_link: str, img_external_id: str)
        :param train: training part of dataset
        :param val: validation part of dataset
        :param test: validation part of dataset
        """
        self._post(
            self.route + 'frames/linked',
            json={
                'train_frames_links': self._validate(train),
                'test_frames_links': self._validate(test),
                'val_frames_links': self._validate(val),
            },
        )
        return self.send()
