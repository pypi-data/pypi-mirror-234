from typing import Iterable, Any, Tuple

from pydantic import BaseModel
from requests import Session

from cval_lib.handlers._based_on_json import BasedOnJSON
from cval_lib.models.annotation import (
    DetectionAnnotationCOCO,
    ClassificationLabels,
    LabelsResponse, Label,
)


class AbstractAnnotation(BasedOnJSON):
    tpe = None

    def __init__(self, session: Session, dataset_id: str, ):
        super().__init__(session)
        self.dataset_id = dataset_id

    @staticmethod
    def _gt(training: Any, test: Any, validation: Any) -> Tuple[Tuple[str, Any], ...]:
        return ('training', training), ('test', test), ('validation', validation)

    def _create_ann(self, part_of_dataset: str, annotation: BaseModel()): ...

    def _get_ann(self, part_of_dataset: str, limit=100) -> BaseModel: ...

    def _delete_ann(self, part_of_dataset: str) -> BaseModel():
        return self.__processing__(
            f'/dataset/{self.dataset_id}/{part_of_dataset}/annotation/{self.tpe}',
            self._delete,
            None,
            None,
        )

    def delete(self, training: bool = False, test: bool = False, validation: bool = False):
        return tuple(
            map(lambda x: self._delete_ann(x[0]), filter(lambda x: x[1], self._gt(training, test, validation)))
        )


class Detection(AbstractAnnotation):
    tpe = 'detection'

    def _create_ann(self, part_of_dataset: str, annotation: DetectionAnnotationCOCO):
        return self.__processing__(
            f'/dataset/{self.dataset_id}/{part_of_dataset}/annotation/{self.tpe}',
            self._post,
            None,
            annotation,
        )

    def _get_ann(self, part_of_dataset: str, limit=None) -> BaseModel:
        return self.__processing__(
            f'dataset/{self.dataset_id}/{part_of_dataset}/annotation/{self.tpe}',
            self._get,
            DetectionAnnotationCOCO,
            None,
        )

    def create(
            self,
            training: DetectionAnnotationCOCO = None,
            test: DetectionAnnotationCOCO = None,
            validation: DetectionAnnotationCOCO = None,
    ):
        return tuple(filter(lambda x: x is not None, (self._create_ann(name, obj) if obj else None
                                                      for (name, obj) in self._gt(training, test, validation))))

    def get(self, training: bool = False, test: bool = False, validation: bool = False):
        return tuple(map(lambda x: self._get_ann(x[0]), filter(lambda x: x[1], self._gt(training, test, validation))))


class Classification(AbstractAnnotation):
    tpe = 'classification'

    def __init__(self, session: Session, dataset_id: str, ):
        super().__init__(session, dataset_id)

    def create(
            self,
            training: Iterable[Label] = None,
            validation: Iterable[Label] = None,
            test: Iterable[Label] = None,
    ):
        return self.__processing__(
            f'/dataset/{self.dataset_id}/annotation/{self.tpe}',
            self._post,
            None,
            ClassificationLabels(
                train_labels=training,
                val_labels=validation,
                test_labels=test
            ),
        )

    def _get_ann(self, part_of_dataset: str, limit=100) -> BaseModel:
        return self.__processing__(
            f'/dataset/{self.dataset_id}/{part_of_dataset}/annotation/{self.tpe}',
            self._get,
            LabelsResponse,
            None,
            params={'limit': limit},
        )

    def get(self, training: bool = False, test: bool = False, validation: bool = False):
        return tuple(map(lambda x: self._get_ann(x[0]), filter(lambda x: x[1], self._gt(training, test, validation))))
