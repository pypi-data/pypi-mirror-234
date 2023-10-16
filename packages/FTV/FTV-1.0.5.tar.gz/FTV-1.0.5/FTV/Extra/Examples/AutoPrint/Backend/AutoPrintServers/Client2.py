import socket
from queue import Queue
from threading import Thread

import wrapt

from FTV.Extra.Experiments import AutoPrintServerCommands
from FTV.Extra.Experiments import ClientConnectivityManager


Commands = AutoPrintServerCommands

# Get the host of the current machine
# Use it only if you run the client on the same machine as the server
HOST = socket.gethostbyname(socket.gethostname())


class ClientCommand:
    def __init__(self, cmd_class):
        self.cmd_class = cmd_class

    @wrapt.decorator
    def __call__(self, wrapped, instance, args, kwargs):
        return instance.__class__.sendCommand(f"{self.cmd_class.__name__}/{wrapped.__name__}", *args, **kwargs)


class AutoPrintDesktopClient(object):
    connManager = ClientConnectivityManager(host=HOST, port=9999)
    messages = Queue()
    responses = Queue()

    def __init__(self):
        self.connManager.onResponse = self.onResponse
        self.setupClient()

    def setupClient(self):
        # pass
        Thread(target=self.sendMessages).start()
        # Thread(target=self.listenToUser).start()

    def onResponse(self, response):
        self.responses.put_nowait(response)

    @classmethod
    def __sendMessage(cls, message: str, ignore_response=False):
        return cls.connManager.sendMessage(message, ignore_response=ignore_response)

    @classmethod
    def sendMessage(cls, message: str, ignore_response=False):
        # return cls.connManager.sendMessage(message, ignore_response=ignore_response)
        cls.__addMessage(message)

    def sendMessages(self):
        while True:
            if not self.messages.empty():
                msg = self.messages.get_nowait()
                cmd, args = self.connManager._unpackMessage(msg)
                # print(f"loop: {msg}")
                if Commands.isCommandExist(cmd):
                    self.__sendCommand(cmd, *args)
                else:
                    print(f"The following command is not exist: \"{cmd}\"")

    # def listenToUser(self):
    #     while True:
    #         msg = str(input("Send: "))
    #         # self.sendMessage(msg)
    #         self.__addMessage(msg)

    @classmethod
    def __addMessage(cls, message):
        cls.messages.put(message)

    def __addResponse(self, response):
        self.responses.put(response)

    @classmethod
    def sendCommand(cls, cmd: str, *args, ignore_response=False):
        cls.__addMessage(cls.connManager._packMessage(cmd, *args))

    @classmethod
    def __sendCommand(cls, cmd: str, *args, ignore_response=False):
        return cls.__sendMessage(cls.connManager._packMessage(cmd, *args), ignore_response=ignore_response)

    @ClientCommand(Commands.Server)
    def login(self, username, password):
        pass

    @ClientCommand(Commands.Server)
    def logout(self, username):
        pass

    @staticmethod
    def register(username, password):
        AutoPrintDesktopClient.sendCommand(Commands.Server.register, username, password)

    # class Station(object):
    #
    #     @staticmethod
    #     def version():


    class Printer(object):

        @staticmethod
        def move(x=0, y=0, z=0):
            AutoPrintDesktopClient.sendCommand(Commands.Printer.move, x, y, z)

        @staticmethod
        def home(x=0, y=0, z=0):
            AutoPrintDesktopClient.sendCommand(Commands.Printer.home, x, y, z)

        @staticmethod
        def setHome(x=None, y=None, z=None):
            AutoPrintDesktopClient.sendCommand(Commands.Printer.setHome, x, y, z)

        @staticmethod
        def getTemperature():
            AutoPrintDesktopClient.sendCommand(Commands.Printer.getTemperature)

        @staticmethod
        def setTemperature(temp_deg):
            AutoPrintDesktopClient.sendCommand(Commands.Printer.setTemperature, temp_deg)


if __name__ == '__main__':
    ap = AutoPrintDesktopClient()
    # time.sleep(3)
    ap.login("daniel", "")
    ap.login("lahav", "")

    msg = None
    exit_commands = ("exit", "quit", "stop")
    while msg not in exit_commands:
        msg = input("Send: ")
        if msg not in exit_commands:
            ap.sendMessage(msg)
