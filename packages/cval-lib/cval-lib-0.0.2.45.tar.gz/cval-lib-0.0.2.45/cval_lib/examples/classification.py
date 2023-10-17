import time

from cval_lib.models.annotation import Label

if __name__ == '__main__':
    from cval_lib.connection import CVALConnection
    from cval_lib.models.classification import ClassificationTest, ClassificationSampling

    USER_API_KEY = ...
    CVAL = CVALConnection(USER_API_KEY)
    DS_ID = CVAL.dataset().create()
    ANN = CVAL.cls_annotation(dataset_id=DS_ID)
    ANN.create(
        training=[Label(img_external_id='123', img_label=1)],
        test=[Label(img_external_id='123', img_label=1)],
        validation=[Label(img_external_id='123', img_label=1)]
    )
    time.sleep(2)
    print(ANN.get(training=True))

    CLS = CVAL.classification()
    RES = CLS.saas_sampling(DS_ID, config=ClassificationSampling(
        num_samples=1,
        batch_unlabeled=-1,
        model='b0',
        selection_strategy='margin',
    ))
    print(RES)
    time.sleep(60*30)
    print(CVAL.result().get(RES.task_id))
    RES = CLS.saas_test(DS_ID, config=ClassificationTest(
        model='b0',
    ))
    print(RES)
    time.sleep(60*20)
    print(CVAL.result().get(RES.task_id))
