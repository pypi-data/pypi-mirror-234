
if __name__ == '__main__':
    import time

    from cval_lib.connection import CVALConnection
    from cval_lib.models.annotation import Label

    USER_API_KEY = ...
    CVAL = CVALConnection(USER_API_KEY)
    DS_ID = CVAL.dataset().create()
    ANN = CVAL.cls_annotation(dataset_id=DS_ID)
    ANN.create(training=[Label(img_external_id='123', img_label=1)])
    time.sleep(2)
    ANN.get(training=True)
