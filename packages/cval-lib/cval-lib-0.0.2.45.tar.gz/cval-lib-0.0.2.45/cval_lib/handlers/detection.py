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

from cval_lib.handlers._based_on_json import BasedOnJSON

from cval_lib.models.detection import (
    DetectionSamplingOnPremise,
    DetectionSampling,
    DetectionTest,
)
from cval_lib.models.result import ResultResponse


class Detection(BasedOnJSON):
    def on_premise_sampling(self, config: DetectionSamplingOnPremise) -> ResultResponse:
        """
        Start Active Learning selection for a specific model predictions.
        Assumes synchronous interaction if the number of predictions does not exceed 10000, otherwise asynchronous.
        Upon executing this method, you will receive either a null _value or a list of images as the result.
        """
        return self.__processing__('/on-premise/sampling/detection', self._post, ResultResponse, config)

    def saas_sampling(self, dataset_id: str, config: DetectionSampling) -> ResultResponse:
        """
        Start Active Learning selection for a specific dataset ID.
        """
        return self.__processing__(f'/dataset/{dataset_id}/sampling/detection', self._post, ResultResponse, config)

    def saas_test(self, dataset_id: str, config: DetectionTest) -> ResultResponse:
        """
        Start model test for a specific dataset config ID.
        """
        return self.__processing__(f'/dataset/{dataset_id}/test/detection', self._post, ResultResponse, config, )
