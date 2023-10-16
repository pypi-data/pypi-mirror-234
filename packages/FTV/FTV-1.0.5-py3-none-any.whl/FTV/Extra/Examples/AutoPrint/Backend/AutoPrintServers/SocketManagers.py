import datetime
import socket
import time
from _thread import start_new_thread
from threading import Thread


class ConnectivityManager(object):
    ARGS_SEPARATOR = "%arg%"

    def __init__(self, host="", port=9999):
        self.socket: socket.socket = None

        self.host = host
        self.port = port

        self.setupSocket()

    def setupSocket(self):
        pass

    def _createSocket(self):
        try:
            self.socket = socket.socket()
            print("Socket has been created.")

        except socket.error as msg:
            print("Socket creation error: " + str(msg))

    def generateLogLine(self, source, message):
        _message = message.replace(self.ARGS_SEPARATOR, ", ")
        timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y %H-%M-%S')
        return f"{timestamp}: {source}: {_message}"

    def sendMessage(self, message: str, ignore_response=False):
        self.socket.send(message.encode("utf-8"))

    @classmethod
    def _packMessage(cls, cmd: str, *args) -> str:
        args_string = cls.ARGS_SEPARATOR.join(list(args))
        return f"{cmd}:{args_string}"

    @classmethod
    def _unpackMessage(cls, message: str) -> (str, dict):
        if ":" in message:
            (cmd, args_string) = message.split(":", 1)
            if cls.ARGS_SEPARATOR in args_string:
                args = tuple(args_string.split(cls.ARGS_SEPARATOR))
            else:
                if args_string == "":
                    args = {}
                else:
                    args = {args_string}
        else:
            cmd = message
            args = {}

        cmd = cmd.replace("\\", "/")

        return cmd, args

    @classmethod
    def _unpackCommand(cls, command: str) -> (str, str):
        if "/" in command:
            _cls, func = command.split("/")
        else:
            _cls = None
            func = command

        return _cls, func

class ClientConnectivityManager(ConnectivityManager):
    def __init__(self, host="", port=9999):
        super(ClientConnectivityManager, self).__init__(host=host, port=port)

    def setupSocket(self):
        self._createSocket()
        self._connectSocket()
        # Thread(target=self.listenToServer).start()

    def sendMessage(self, message: str, ignore_response=False):
        print(self.generateLogLine("Client", message))
        self.socket.send(message.encode("utf-8"))
        try:
            response = str(self.socket.recv(2048), "utf-8")
            print(self.generateLogLine("Server", response))
            self.onResponse(response)
            return response

        except ConnectionResetError:
            print("Error connection issue")

    def _connectSocket(self):
        self.socket.connect((self.host, self.port))

    def onResponse(self, response):
        pass

class ServerConnectivityManager(ConnectivityManager):

    def __init__(self, host="", port=9999):
        self.connections = {}
        super(ServerConnectivityManager, self).__init__(host=host, port=port)

    def listenToConnections(self):
        while True:
            self._acceptConnection()

    def listenToClient(self, conn_full_address):
        connection = self.connections[conn_full_address]
        while True:
            try:
                data = connection.recv(2048)
                if not data:
                    break

            except ConnectionResetError:
                break

            message = str(data.decode("utf-8"))
            print(self.generateLogLine(f"Client {conn_full_address}", message))
            self.onMessageReceived(message)

        self._closeConnection(conn_full_address)

    def setupSocket(self):
        self._createSocket()
        self._bindSocket()
        self.socket.setblocking(True)
        Thread(target=self.listenToConnections).start()

    def onMessageReceived(self, message):
        pass

    def _bindSocket(self):
        try:
            self.socket.bind((self.host, self.port))
            self.socket.listen(2)
            print("Socket has been bonded.")

        except socket.error as msg:
            print("Socket Binding error: " + str(msg) + "\n" + "Retrying...")

    def _acceptConnection(self):
        try:
            conn, address = self.socket.accept()
            full_address = ":".join([str(item) for item in address])
            self.connections[full_address] = conn
            print(f"Connection has been established: \"{full_address}\"")

            start_new_thread(self.listenToClient, (full_address,))

        except socket.error as msg:
            print("Socket acceptance error: " + str(msg))

    def _closeConnection(self, conn_full_address):
        print(self.generateLogLine(f"Client \"{conn_full_address}\"", "is disconnected."))
        self.connections[conn_full_address].close()
        del self.connections[conn_full_address]
