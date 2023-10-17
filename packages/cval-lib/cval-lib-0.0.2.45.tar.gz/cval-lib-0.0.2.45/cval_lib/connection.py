
from cval_lib.handlers.dataset import Dataset
from cval_lib.handlers.embedding import Embedding
from cval_lib.handlers.detection import Detection
from cval_lib.handlers.classification import Classification
from cval_lib.handlers.result import Result
from cval_lib.handlers.frames import Frames

from cval_lib.handlers.annotation import (
    Detection as DetectionAnnotation,
    Classification as ClassificationAnnotation,
)
from cval_lib.utils.base_conn import BaseConn


class CVALConnection(BaseConn):
    def dataset(self) -> Dataset:
        """
        actions with dataset: : create, get, delete, update by ID or all (with some limits)
        :return: Dataset
        """
        return Dataset(session=self.session, )

    def embedding(self, dataset_id: str, part_of_dataset: str) -> Embedding:
        """
        actions with embedding: create, get, delete, update by ID or all (with some limits)
        :param dataset_id: id of dataset
        :param part_of_dataset: type of dataset (training, test, validation)
        :return: Embedding
        """
        return Embedding(self.session, dataset_id=dataset_id, part_of_dataset=part_of_dataset, )

    def detection(self) -> Detection:
        """
        This method can be used to call a detection sampling or test
        :return: Detection
        """
        return Detection(self.session, )

    def result(self) -> Result:
        """
        This method can be used for polling
        :return: Result
        """
        return Result(self.session, )

    def frames(self, dataset_id: str, part_of_dataset: str = None) -> Frames:
        """
        This method can be used for raw frames data uploading and get metadata
        :return: Frames
        """
        return Frames(self.session, dataset_id=dataset_id, part_of_dataset=part_of_dataset)

    def det_annotation(self, dataset_id: str, ) -> DetectionAnnotation:
        """
        This method can be used for annotation uploading and get for detection tasks
        :return: DetectionAnnotation
        """
        return DetectionAnnotation(self.session, dataset_id=dataset_id, )

    def cls_annotation(self, dataset_id: str) -> ClassificationAnnotation:
        """
        This method can be used for annotation uploading and get for classification tasks
        :return: DetectionAnnotation
        """
        return ClassificationAnnotation(self.session, dataset_id)

    def classification(self) -> Classification:
        return Classification(self.session)

