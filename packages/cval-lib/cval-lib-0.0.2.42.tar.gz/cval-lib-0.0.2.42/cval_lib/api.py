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

import asyncio
import logging
import re
from types import NoneType
from typing import Any, List, Tuple

from pydantic import BaseModel

from cval_lib.connection import CVALConnection
from cval_lib.utils.entrypoint import (
    Entrypoint,
    Conflict,
    signature,
)
from cval_lib.utils.logger import Logger


class CVALEntrypoint(Entrypoint, CVALConnection, Logger):
    """
    The entry point can be useful in cases where:
        -- the task being performed is relatively small and does not need profiling;
        -- it is known which parameters are transmitted;
        -- there is no time to understand the library code;
        -- there is a need to study the documentation experimentally.
    """
    __cache__ = None
    _skip_regexps = (
        '',
        '*',
    )

    def __init__(self, user_api_key: str, loglevel=logging.NOTSET, log_docs: bool = True, sync: bool = True):
        super().__init__(user_api_key=user_api_key, sync=sync)
        logging.getLogger()
        self.log_docs = log_docs
        self.loglevel = loglevel

    @staticmethod
    def _chain(_methods: List[Entrypoint], conflicts: Tuple[Tuple[callable, callable, Conflict], ...]):
        for meth, lam, conflict in conflicts:
            _methods = tuple(meth(lam, _methods))
            if not _methods:
                raise conflict
        return _methods

    def find_method(self, request: BaseModel = None, name_regexp='*', docs_regexp='*', **kwargs, ):
        if self.__cache__ is None:
            self.__cache__ = self._get_methods(CVALConnection)
            self.info(f'Cached {self.__cache__.__len__()} methods.')
        _methods = self._chain(
            _methods=self.__cache__,
            conflicts=(
                (
                    filter,
                    lambda x: isinstance(request, x.request_model[1], ) if x.request_model is not NoneType else
                    (True if request is not None else False),
                    Conflict(f'Unknown model. {request.__class__}'),
                ),
                (
                    lambda _, x: reversed(
                        sorted(
                            x,
                            key=lambda y: (set(y.kwargs) & set(kwargs.keys())).__len__() +
                                          (set(y.kwargs_not_defaults) & set(kwargs.keys())).__len__(),
                        )
                    ),
                    None,
                    Conflict(f'No methods found for this **kwargs. {kwargs}'),
                ),
                (
                    filter,
                    lambda x: (
                        re.findall(pattern=name_regexp,
                                   string=x.name, ) if name_regexp not in self._skip_regexps else True),
                    Conflict(f'No methods found for name_regexp. {name_regexp}.')
                ),
                (
                    filter,
                    lambda x: (
                        re.findall(pattern=docs_regexp, string=x.func.__doc__)
                        if docs_regexp not in self._skip_regexps else True),
                    Conflict(f'No methods found for docs_regexp. {docs_regexp}.')
                )
            )
        )
        return _methods

    def execute(
            self,
            request: BaseModel = None,
            name_regexp: str = '*',
            docs_regexp: str = '*',
            **kwargs,
    ) -> Any:
        """
        Args:
            request:
                Is a request model to execute. In most cases it is optional.
                dataset:
                    `cval_lib.models.dataset.DatasetModel`
                        dataset_name
                            the name of dataset
                        dataset_description
                            the description of dataset
                detection:
                    `cval_lib.models.detection.DetectionSamplingOnPremise`
                        num_of_samples
                            absolute number of samples to select
                        bbox_selection_policy
                            Which bounding box to select when there are multiple boxes on an image,
                            according to their confidence. Supports: min, max, mean
                        selection_strategy:
                            Currently supports: margin, least, ratio, entropy, clustering
                        probs_weights:
                            Determines the significance (weight) of the prediction probability for each class.
                            The order in the list corresponds to the order of the classes.
                            It is essential for a multi-class entropy method.
                        frames:
                            prediction for th picture and the bbox
                embedding:
                    `cval_lib.models.embedding.EmbeddingModel`
                result:
                    `cval_lib.models.result.ResultResponse`
                        task_id
                            id of result for polling
                        dataset_id
                            id of dataset
                        time_start
                            starting unix timestamp
                        time_end
                            ending unix timestamp
                        type_of_task
                            type of task: detection, classification
                        action
                            sampling or test
                        weights:
                            weights of result
            name_regexp
                    regular expression for method search by name
            docs_regexp
                    regular expression for method search by docstring
            optional kwargs:
                    name:
                        dataset name
                    description:
                        dataset description
                    dataset_id:
                        id of dataset
                    embedding_id:
                        id of embedding
                    frame_id:
                        id of frame
                    start_limit:
                        upper limit of items
                    stop_limit:
                        lower limit of items

        :raises pydantic.error_wrappers.ValidationError
        if len(dataset_name) > 32 or len(dataset_description) > 256
        :raises ValueError if value not in allowed:
        """
        if kwargs.get('session') is not None:
            del kwargs['session']
        if kwargs.get('sync') is not None:
            del kwargs['sync']
        _methods = self.find_method(request, name_regexp, docs_regexp, **kwargs)
        method = _methods[0]
        self.info(f'Founded method <{method.name}> of {method.base}.')
        if self.log_docs:
            self.info(f'Docstring: {method.func.__doc__}')
        base_class = method.base

        def call():
            with self.session as session:
                return method.func(
                    self=base_class(
                        session=session,
                        **{k: v for k, v in kwargs.items() if k in signature(base_class.__init__)}
                    ),
                    **(
                        {method.request_model[0]: request} if method.request_model is not NoneType else {} |
                        {k: v for k, v in kwargs.items() if k in method.kwargs}
                    ),
                )
        if self.sync:
            return call()

        async def af():
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(None, call)
        return af()

