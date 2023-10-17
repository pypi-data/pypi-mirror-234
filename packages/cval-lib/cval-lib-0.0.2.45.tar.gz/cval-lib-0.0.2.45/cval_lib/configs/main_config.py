from cval_lib.patterns.singleton import Singleton


class MainConfig(metaclass=Singleton):
    main_url = 'http://212.41.26.97:6789/api'
