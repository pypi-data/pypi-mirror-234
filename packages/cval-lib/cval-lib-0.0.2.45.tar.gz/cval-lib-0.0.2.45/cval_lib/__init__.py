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

import os
from .utils import lib_tools, install_dynamically

if os.getenv('CVAL_CHECK_VERSION') == 'True':
    lib_tools.LibraryChecker('cval-lib')()

if os.getenv('CVAL_AUTO_UPDATE') == 'True':
    install_dynamically.install_libs(
        f"cval-lib=={lib_tools.LibraryChecker('cval-lib').latest_version}"
    )

if os.getenv('CVAL_INSTALL_TOOLS_DEPS') == 'True':
    install_dynamically.install_libs(
        'torchvision',
        'sklearn',
        'albumentations',
    )





from . import (
    models,
    handlers,
    examples,
    connection,
    api,
    tools,
)

from .models import (
    annotation,
    classification,
    dataset,
    detection,
    embedding,
    frame,
    result,
    weights,
)



CVALConnection, API = connection.CVALConnection, api.CVALEntrypoint
CVALEntrypoint = API


__all__ = [
    'models',
    'handlers',
    'examples',
    'tools',
    'annotation',
    'classification',
    'dataset',
    'detection',
    'embedding',
    'frame',
    'result',
    'weights',
    'connection',
    'api',
    'CVALConnection',
    'API',
    'CVALEntrypoint',
]

VERSION = '0.0.2.45'

