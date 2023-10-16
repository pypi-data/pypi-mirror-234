from _thread import start_new_thread

from FTV.Extra.Experiments import AutoPrintServerCommands
from FTV.Extra.Experiments import ServerConnectivityManager


Commands = AutoPrintServerCommands


class UserConnectivityManager(ServerConnectivityManager):
    pass


class ServerConnectivityManager(ServerConnectivityManager):
    pass


class AutoPrintServer(object):

    def __init__(self):
        self.dataBase = {}

        self.loadDataBase()
        self.userConnManager = UserConnectivityManager(host="", port=9999)
        self.userConnManager.onMessageReceived = self.onUserMessageReceived

        self.connStationManager = ServerConnectivityManager(host="", port=8888)
        self.connStationManager.onMessageReceived = self.onStationMessageReceived

    def loadDataBase(self):
        self.dataBase = {
            "lahav": {
                "password": "",
                "logged_in": False,
                "stations": {
                    "Apartment": {
                        "Controllers": [
                            "Lusy",
                            "Lucas"
                        ]
                    },
                    "Hamama": {
                        "Controllers": [
                            "Z18",
                            "Prusa"
                        ]
                    }
                }
            },
            "daniel": {
                "password": "",
                "logged_in": False,
                "stations": {
                    "Home": {
                        "Controllers": [
                            "Mendy"
                        ]
                    }
                }
            }
        }

    def __sendMessageToUser(self, conn_full_address, message: str):
        self.userConnManager.connections[conn_full_address].send(message.encode("utf-8"))

    def sendCommandToUser(self, cmd, data):
        self.__sendMessageToUser(list(self.userConnManager.connections.keys())[0], f"{cmd}:{data}")  # TODO lahav This solution is temporary.

    def __sendMessageToStation(self, conn_full_address, message: str):
        self.connStationManager.connections[conn_full_address].send(message.encode("utf-8"))

    def sendCommandToStation(self, cmd, data):
        self.__sendMessageToUser(list(self.connStationManager.connections.keys())[0], f"{cmd}:{data}")  # TODO lahav This solution is temporary.

    def onUserMessageReceived(self, message):
        start_new_thread(self.checkAndRunCommand, (message,))

    def onStationMessageReceived(self, message):
        start_new_thread(self.checkAndRunCommand, (message,))

    def checkAndRunCommand(self, message):
        cmd, args = self.userConnManager._unpackMessage(message)
        cls, func = self.userConnManager._unpackCommand(cmd)

        if Commands.isCommandExist(cmd):
            response = None
            if hasattr(self, func):
                try:
                    response = self.__getattribute__(func).__call__(*args)
                except TypeError as e:
                    response = str(e)

                if cls == "Server":
                    pass

                elif cls == "Station":
                    pass

                elif cls in ["Printer", "Bed"]:
                    pass

            # print(f"{cls}.{func}({str(*args)})")

            if response is None:
                response = f"The following command has not been implemented yet: \"{cmd}\""
        else:
            response = f"The following command is not exist: \"{cmd}\""

        self.__sendMessageToUser(
            list(self.userConnManager.connections.keys())[0], response
        )  # TODO lahav This solution is temporary.

    ## Server commands

    def login(self, username, password=None):
        # time.sleep(5)
        if username in self.dataBase:
            if self.dataBase[username]["logged_in"]:
                response = "Server/login: You are already logged in"
            else:
                if self.dataBase[username]["password"] == password:
                    response = "Server/login: Ok"
                    self.dataBase[username]["logged_in"] = True
                    # self.userConnManager.connections
                else:
                    response = "Server/login: Wrong password"
        else:
            response = "Server/login: Username is not exist"

        return response

    def logout(self, username):
        if username in self.dataBase:
            self.dataBase[username]["logged_in"] = False
            response = "Server/logout: Ok"
        else:
            response = "Server/logout: Username is not exist"

        return response

    def register(self, username, password=None):
        if username not in self.dataBase:
            self.dataBase[username] = {
                "password": password,
                "logged_in": True,
                "stations": []
            }
            response = "Server/register: Ok"
        else:
            response = "Server/register: Username is already exist"

        return response

    ## Station commands

    def version(self):
        pass


if __name__ == '__main__':
    AutoPrintServer()
