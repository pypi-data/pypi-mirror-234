import serial.tools.list_ports


class Arduino:
    @staticmethod
    def scanArduinoPorts():
        ports = list(serial.tools.list_ports.comports())
        arduino_ports = []

        for port in ports:
            if not port.description.startswith("Arduino"):
                if port.manufacturer is not None:
                    if port.manufacturer.startswith("Arduino") and port.device.endswith(port.description):
                        port.description = "Arduino Uno"
                    else:
                        continue
                else:
                    continue

            if port.device:
                arduino_ports.append(port.device)

        return [item.device for item in arduino_ports]
