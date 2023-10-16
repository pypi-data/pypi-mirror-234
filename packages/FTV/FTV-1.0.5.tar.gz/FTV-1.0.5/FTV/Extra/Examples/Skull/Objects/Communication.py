import time
from datetime import datetime

import serial.tools.list_ports
# TODO architecture construct this class
from setuptools._vendor.ordered_set import OrderedSet

from StaticData import config
from Tools.ArduinoTools import Arduino


def _print(source, text):
    time_stamp = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    print(f"\033[0;34m{time_stamp}\033[0m \033[0;32m{source}:\033[0m {text}")


class Serial(serial.Serial):
    def __init__(self, port=None, baudrate=9600, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE,
                 stopbits=serial.STOPBITS_ONE, timeout=None, xonxoff=False, rtscts=False, write_timeout=None,
                 dsrdtr=False, inter_byte_timeout=None, exclusive=None, **kwargs):
        super(Serial, self).__init__(port, baudrate, bytesize, parity, stopbits, timeout, xonxoff, rtscts,
                                     write_timeout, dsrdtr, inter_byte_timeout, exclusive, **kwargs)
        self.buffer_size: int = 1024
        self.port_name = port

    def getPortName(self):
        return self.port_name

    def setBufferSize(self, buffer_size):
        self.buffer_size = buffer_size

    def open(self):
        if not self.is_open:
            super().open()

    def write(self, cmd: str):
        super(Serial, self).write(cmd.encode())

    def print(self, text):
        """Print messages from the device."""
        _print("Device", text)

    def isArduino(self, expected_baudrate):
        if self.baudrate == expected_baudrate:
            return True
        else:
            return False


# TODO architecture refactor this class
class VirtualSerial(Serial):
    def __init__(self, port=None, baudrate=9600, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
                 timeout=None, xonxoff=False, rtscts=False, write_timeout=None, dsrdtr=False, inter_byte_timeout=None,
                 exclusive=None, **kwargs):
        super().__init__(port, baudrate, bytesize, parity, stopbits, timeout, xonxoff, rtscts, write_timeout, dsrdtr,
                         inter_byte_timeout, exclusive, **kwargs)

        self.output = None
        self._in_waiting = True
        self.is_open = False

        self.sensors = ()

    def open(self):
        self.is_open = True

    def close(self):
        self.is_open = False

    def write(self, cmd):
        self.in_waiting = True
        self.output = self.performCommand(cmd.encode("utf-8"))
        return len(cmd)

    def _generateOutput(self, id, mac, power, dtr, mv):
        data = f"MAC:{mac}@power:{power}@dtr:{dtr}@mV:{mv}"
        output = f"from: id:{id}@data:{data}"
        return output

    def performCommand(self, cmd):
        output = ""
        cmd = cmd.decode("utf-8")

        if cmd == "8":
            outputs = []

            self.sensors = config.getVirSensorsData()

            for sensor_name, sensor_data in self.sensors.items():
                _id = 5

                outputs.append(self._generateOutput(
                    _id,
                    sensor_data["mac"],
                    sensor_data["power"],
                    sensor_data["dtr"],
                    sensor_data["mV"],
                ))

            output = "\n".join(outputs)

        elif cmd == "getBattery":
            output = "80"

        return output.encode()

    def readline(self, __size=None) -> bytes:
        self.in_waiting = False
        return self.output

    @property
    def in_waiting(self):
        self._in_waiting = True

    @in_waiting.setter
    def in_waiting(self, value):
        self._in_waiting = value

    @in_waiting.getter
    def in_waiting(self):
        return self._in_waiting

    def print(self, text):
        """Print messages from the device."""
        _print("VirDevice", text)


# TODO architecture refactor this class
class Port:
    def __init__(self, port_name):
        """ Prepare serial port object

            :returns:
                serial port object
        """
        self.port_name = port_name
        self.output = None  # Reserve for console output element in UI.
        self._setup()

    def _setup(self):
        if not self.isVirtual(self.port_name):
            self.serial = Serial(self.port_name, timeout=1, write_timeout=1)
        else:
            self.serial = VirtualSerial(self.port_name, timeout=1, write_timeout=1)

        self.serial.setBufferSize(10000000)

    def connect(self):
        self.serial.open()

    def sendCommand(self, cmd: str):
        start_time = time.time()
        # self.print(f"cmd: {cmd}")
        self.serial.write(cmd)
        ser_data = ""

        # TODO architecture Check if this line is really necessary for the real serial connection.
        # time.sleep(BUFFERING_S)

        while self.serial.inWaiting():
            try:
                ser_data += self.serial.readline().decode('utf-8')
            except UnicodeDecodeError:
                # TODO architecture Check if you can prevent the crashes.
                # Skip gibberish if ESP crashes.
                pass

        response = ser_data.strip()
        response_time = time.time() - start_time

        response_repr = response.replace('\n', ' '*2)
        # self.print(f"res: \033[0;33m{response_repr}\033[0m | time: {response_time}")

        return response

    def getSensorData(self):
        return self.sendCommand("8")

    def print(self, text):
        _print(self.serial.getPortName(), text)

    def isAlive(self):
        port_names = Arduino.scanArduinoPorts()

        if config.isVirtualConnected():
            port_names.append("VIR0")

        return self.port_name in port_names

    @staticmethod
    def isVirtual(port):
        return port.startswith("VIR")

    def getPortName(self):
        return self.port_name

    def __repr__(self):
        return self.port_name


class SerialManager:
    def __init__(self, baudrate=9600):
        self.baudrate = baudrate
        self.available_port_names = OrderedSet()
        self.used_ports = OrderedSet()

    def scanPorts(self):
        """ Lists serial port names

            :raises EnvironmentError:
                On unsupported or unknown platforms
            :returns:
                A list of the serial ports available on the system
        """

        port_names = []

        port_names += Arduino.scanArduinoPorts()

        if config.isVirtualConnected():
            port_names.append("VIR0")
        else:
            if "VIR0" in self.used_ports:
                self.used_ports.remove("VIR0")

        self.available_port_names = self.available_port_names | set(port_names)
        self.available_port_names -= self.used_ports

    def isPortAvailable(self):
        return bool(self.available_port_names)

    def isPortInUse(self, port_name):
        return port_name in self.used_ports

    def getAvailablePort(self):
        if self.isPortAvailable():
            port_name = self.available_port_names[0]
            self.used_ports.add(port_name)
            self.available_port_names.remove(port_name)
            return Port(port_name)
