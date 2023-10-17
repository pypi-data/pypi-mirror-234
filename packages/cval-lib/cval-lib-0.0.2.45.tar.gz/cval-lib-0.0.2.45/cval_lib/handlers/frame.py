
from requests import Session

from cval_lib.configs.main_config import MainConfig
from cval_lib.handlers._abstract_handler import AbstractHandler


class Frame(AbstractHandler):
    def __init__(
            self,
            session: Session,
            part_of_dataset: str,
            frame_id: str,
            dataset_id: str = None,
    ):
        self.route = f'{MainConfig.main_url}/dataset/{dataset_id}/{part_of_dataset}/frame/{frame_id}'
        super().__init__(session)

    def read(self):
        self._get(self.route, stream=True)
        return self.send()

    def create(self, file):
        self._post(self.route, file=file)
        return self.send()

    def update(self, file):
        self._put(self.route, file=file)
        return self.send()

    def delete(self):
        self._delete(self.route)
        return self.send()

    def hash(self):
        self._get(self.route + '/hash')
        return self.send().data
