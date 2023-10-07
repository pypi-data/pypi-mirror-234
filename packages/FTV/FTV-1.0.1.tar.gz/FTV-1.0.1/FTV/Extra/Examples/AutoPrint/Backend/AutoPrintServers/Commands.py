class Command(object):
    commands = set()

    def __init_subclass__(cls, **kwargs):
        cls.commands |= set(f"{cls.__name__}/{item}" for item in dir(cls)
                            if isinstance(getattr(cls, item), str) and not cls.isMagicMethod(item))

    @classmethod
    def getClassName(cls):
        return cls.__name__

    @staticmethod
    def isMagicMethod(method_name: str):
        return method_name.startswith("__") and method_name.endswith("__")

class AutoPrintServerCommands:
    commands = set()

    @classmethod
    def isCommandExist(cls, cmd):
        return cmd in Command.commands

    class Server(Command):
        login = "login"
        logout = "logout"
        register = "register"

    class Station(Command):
        version = "version"
        id = "id"
        name = "name"
        selectController = "selectController"
        getControllers = "getControllers"
        getOnlineControllers = "getOnlineControllers"
        addController = "addFeatures"
        removeController = "remove"

    class Controller(Command):
        version = "version"


    class Printer(Command):
        name = "name"
        getTemperature = "getTemperature"
        setTemperature = "setTemperature"
        home = "home"
        setHome = "setHome"
        move = "move"

    class Bed(Command):
        version = "version"
        move = "move"
        moveUntilBreak = "moveUntilBreak"
        release = "release"
        home = "home"


class AutoPrintServerCommandsInterface:
    class Server(object):

        @staticmethod
        def login(username, password):
            pass

        @staticmethod
        def register(username, password):
            pass

    class Printer(object):

        def move(self, x=0, y=0, z=0):
            pass

        def home(self, x=0, y=0, z=0):
            pass

        def setHome(self, x=None, y=None, z=None):
            pass

        def getTemperature(self):
            pass

        def setTemperature(self, temp_deg):
            pass
