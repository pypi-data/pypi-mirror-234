from pydantic import BaseModel
from requests import Session

from cval_lib.configs.main_config import MainConfig
from cval_lib.handlers._abstract_handler import AbstractHandler
from cval_lib.handlers.result import Result
from cval_lib.models.result import ResultResponse


class BasedOnJSON(AbstractHandler):
    def __init__(
            self,
            session: Session,
    ):
        self.route = f'{MainConfig().main_url}'
        self.result = Result(session)
        super().__init__(session)

    def __processing__(
            self, sub_router: str,
            method, parser: BaseModel() = None,
            json: BaseModel() = None,
            params: dict = None,
    ) -> BaseModel():
        method(url=self.route + sub_router, json=json.dict() if json is not None else {}, params=params)
        if parser is None:
            return self.send().json()
        elif parser.__name__ == 'ResultResponse':
            result = ResultResponse.parse_obj(
                self.send().json()
            )
            self.result.task_id = result.task_id
        else:
            result = parser.parse_obj(
                self.send().json()
            )
        return result
