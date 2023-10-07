from __future__ import annotations

from io import BytesIO
from typing import List

from requests import Session

from cval_lib.configs.main_config import MainConfig
from cval_lib.handlers._abstract_handler import AbstractHandler
from cval_lib.models.weights import WeightsBase


class Weights(AbstractHandler):
    def __init__(
            self,
            session: Session,
            weights_id: str = None,
            version: str = None,
    ):
        super().__init__(session)
        self.route = MainConfig.main_url
        self.weights_id = weights_id
        self.version = version

    def create(self, file):
        self._post(self.url + '/weights/blob', file=file)
        return WeightsBase.parse_obj(self.send().json())

    def get_meta_all(self) -> List['WeightsBase']:
        self._get(self.route+'/weight/meta/all')
        return [WeightsBase.parse_obj(i) for i in self.send().json()]

    def get_meta(self) -> 'WeightsBase':
        self._get(self.route+f'weights/{self.weights_id}/version/{self.version}/meta')
        return WeightsBase.parse_obj(self.send().json())

    def get_blob(self) -> BytesIO:
        self._get(self.route+f'/weights/{self.weights_id}/version/{self.version}/meta')
        return BytesIO(self.send().data)
