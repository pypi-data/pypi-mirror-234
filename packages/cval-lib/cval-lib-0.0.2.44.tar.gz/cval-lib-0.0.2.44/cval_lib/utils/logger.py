import logging


from cval_lib.patterns.singleton import Singleton


class Color:
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    RESET = "\033[0m"

    def __init__(self, color: str = None, loglevel: int = logging.INFO):
        logging.getLogger()
        logging.basicConfig(level=loglevel, format='%(asctime)s | %(message)s')
        self.loglevel = loglevel
        self.color: str = color.upper()

    def log(self, text: str) -> None:
        colored_text = f"{self.__getattribute__(self.color)}{text}{self.RESET}"
        logging.log(self.loglevel, colored_text)


class Logger(Color, metaclass=Singleton):
    def info(self, text):
        self.color = 'BLUE'
        self.log('CVAL-LIB:\t' + text)

    def warn(self, text):
        self.color = 'RED'
        self.loglevel = logging.WARN
        self.log('CVAL-LIB:\t' + text, )
