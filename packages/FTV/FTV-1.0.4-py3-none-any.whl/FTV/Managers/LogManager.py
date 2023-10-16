from FTV.Managers.AbstractManager import AbstractManager
from FTV.Managers.Log import Log


class LogManager(AbstractManager):
    """This class is temporary!"""
    ENABLED = True
    BUILTIN_ENABLED = False
    __BLANK_SPACE = 0

    _DEBUG_MODE = False

    def __init__(self, _is_parent_app=None):
        super().__init__(_is_parent_app=_is_parent_app)
        self.setOptions()

    def init(self):
        pass

    def setOptions(self):
        pass

    @classmethod
    def setDebuggingMode(cls, mode):
        cls._DEBUG_MODE = mode

    @classmethod
    def print(cls, message=None):
        if cls._DEBUG_MODE:
            if message is None:
                message = ""
            print(message)

    def startApp(self):
        self.print()

    def endApp(self):
        self.print()


class logmethod:
    _stage_level = 0

    def __init__(self, func):
        self.func = func
        self.name = self.func.__name__
        self._update_interval()

    def __call__(self, *args, **kwargs):
        self._update_interval()
        LogManager.print(self.interval + "-> " + self.name)

        logmethod._stage_level += 1
        self.func(self, *args, **kwargs)
        logmethod._stage_level -= 1

        self._update_interval()
        LogManager.print(self.interval + "<- " + self.name)

    def _update_interval(self):
        self.interval = "  " * logmethod._stage_level
