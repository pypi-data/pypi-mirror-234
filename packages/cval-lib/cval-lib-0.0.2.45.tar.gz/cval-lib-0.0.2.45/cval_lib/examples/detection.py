import json
import time

import requests

from cval_lib.models.annotation import DetectionAnnotationCOCO

if __name__ == '__main__':
    from cval_lib.connection import CVALConnection
    from cval_lib.models.detection import DetectionTest, DetectionSampling

    USER_API_KEY = ...
    CVAL = CVALConnection(USER_API_KEY)
    DS_ID = CVAL.dataset().create()

    ANN = CVAL.det_annotation(dataset_id=DS_ID).create(
        training=DetectionAnnotationCOCO.parse_obj(
            json.loads(
                requests.get(
                    'https://raw.githubusercontent.com/fangorntreabeard/coco-person/main/train.json'
                             ).text
            )
        ),
        test=DetectionAnnotationCOCO.parse_obj(
            json.loads(
                requests.get(
                    'https://raw.githubusercontent.com/fangorntreabeard/coco-person/main/test.json'
                             ).text
            )
        ),
        validation=DetectionAnnotationCOCO.parse_obj(
            json.loads(
                requests.get(
                    'https://raw.githubusercontent.com/fangorntreabeard/coco-person/main/val.json'
                ).text
            )
        ),
    )

    RES = CVAL.detection().saas_sampling(dataset_id=DS_ID, config=DetectionSampling(...))
    time.sleep(60*120)
    print(CVAL.result().get(RES.task_id))
    RES = CVAL.detection().saas_test(dataset_id=DS_ID, config=DetectionTest(...))
