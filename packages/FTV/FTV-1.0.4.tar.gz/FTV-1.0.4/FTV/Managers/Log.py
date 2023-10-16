import socket
import traceback

from FTV.Extra.Examples.BIUAutomation.Tools.Files import Json


class Log:
    """This class is temporary!"""
    ENABLED = True
    BUILTIN_ENABLED = False
    __BLANK_SPACE = 0
    __PORT = 64328
    __HOST = "localhost"
    sock: socket.socket
    FTV_CONSOLE_IS_ATTACHED = False

    @staticmethod
    def p(message="", color=""):
        Log.__print("", message, color)

    @staticmethod
    def i(message="", color=""):
        Log.__print("info", message, color)

    @staticmethod
    def d(message="", color=""):
        Log.__print("debug", message, color)

    @staticmethod
    def e(message="", color=""):
        Log.__print("error", message, color)

    @staticmethod
    def traceback(exctype=None, value=None, tb=None):
        if tb is None:
            repr_message = traceback.format_exc()
        else:
            extracted_tb = traceback.extract_tb(tb)
            repr_message = "Traceback (most recent call last):\n"
            repr_message += "".join(traceback.StackSummary.from_list(extracted_tb).format())
            repr_message += f"{exctype.__name__}: {value}"

        Log.p(repr_message, Log.color.RED)

    @staticmethod
    def input(message="", color=""):
        return Log.__input("", message, color)

    @staticmethod
    def json(data=None, color="", indent=2, ensure_ascii=False):
        Log.__print("", Json.dumps(data, indent=indent, ensure_ascii=ensure_ascii), color)

    @staticmethod
    def __input(mode, message, color):
        _message = str(message).replace("\n", "\n" + "   "*Log.__BLANK_SPACE)
        mode_str = "".join((mode, ": "*int(bool(mode))))
        msg_str = "".join(("   "*Log.__BLANK_SPACE, mode_str, color, _message, "\033[0m"))

        if Log.FTV_CONSOLE_IS_ATTACHED:
            # Print to FTV console
            pass
        else:
            # Print to general console
            return input(msg_str)

    @staticmethod
    def __print(mode, message, color, sep="\n"):
        if Log.ENABLED:
            _message = str(message).replace("\n", "\n" + "   "*Log.__BLANK_SPACE)
            mode_str = "".join((mode, ": "*int(bool(mode))))
            msg_str = "".join(("   "*Log.__BLANK_SPACE, mode_str, color, _message, "\033[0m"))

            if Log.FTV_CONSOLE_IS_ATTACHED:
                # Print to FTV console
                Log.sock.send(msg_str.encode())
            else:
                # Print to general console
                print(msg_str, sep=sep)

    @staticmethod
    def get(message, color=""):
        return Log.__get("", message, color)

    @staticmethod
    def __get(mode, message, color):
        if Log.ENABLED:
            message = message.replace("\n", "\n" + "   "*Log.__BLANK_SPACE)
            mode_str = "".join((mode, ": "*int(bool(mode))))
            msg_str = "".join(("   "*Log.__BLANK_SPACE, mode_str, color, str(message), "\033[0m"))

            if Log.FTV_CONSOLE_IS_ATTACHED:
                # Print to FTV console
                Log.sock.send(msg_str.encode())
            else:
                # Print to general console
                return input(msg_str)

    @classmethod
    def step(cls, step):
        cls.__BLANK_SPACE += step

    @classmethod
    def setup(cls):
        return
        # Setup the socket
        cls.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # cls.sock.settimeout(1000)
        try:
            cls.sock.connect((cls.__HOST, cls.__PORT))
            cls.FTV_CONSOLE_IS_ATTACHED = True
        except (ConnectionRefusedError, TimeoutError):
            cls.FTV_CONSOLE_IS_ATTACHED = False
        except IOError:
            traceback.print_exc()

    class color:
        LIGHT_BLUE = "\033[0;96m"
        BLUE = "\033[0;34m"
        ORANGE = "\033[0;33m"
        PURPLE = "\033[0;35m"
        PINK = "\033[0;95m"
        RED = "\033[0;31m"
        GREEN = "\033[0;32m"


if __name__ == '__main__':
    # for i in list(range(30, 38)) + list(range(90, 98)):
    #     color_code = "\033[0;{}m".format(i)
    #     print("{}color {}{}".format(color_code, i, "\033[0m"))

    # while True:
    Log.setup()
    Log.p("Lahav")  # send message
    Log.p("Lahav")  # send message
    Log.p("Lahav")  # send message
    Log.p("Lahav")  # send message
    Log.p("Lahav")  # send message
