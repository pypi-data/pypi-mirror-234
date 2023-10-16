if __name__ == '__main__':
    from cval_lib.connection import CVALConnection
    from cval_lib.models.frame import FrameModel

    USER_API_KEY = '2a90cd6b4cb6d1ad1d7e51f43298d105c199e32fc5e33272897b1e5880ac2bce'
    CVAL = CVALConnection(USER_API_KEY)
    DS_ID = CVAL.dataset().create()
    RES = CVAL.frames(DS_ID, ).create_fl(
        train=[
            FrameModel(
                img_external_id='1',
                img_link='https://happypik.ru/wp-content/uploads/2019/09/njashnye-kotiki8.jpg',
            ),
        ],
        test=[
            FrameModel(
                img_external_id='1',
                img_link='https://happypik.ru/wp-content/uploads/2019/09/njashnye-kotiki8.jpg',
            ),
        ],
        val=[
            FrameModel(
                img_external_id='1',
                img_link='https://happypik.ru/wp-content/uploads/2019/09/njashnye-kotiki8.jpg',
            ),
        ],
    )
    print(RES)
