

class Sensor:
    def __init__(self, name):
        self.name = name

    def getName(self):
        return self.name


class Device:
    def __init__(self):
        self.sensors: list[Sensor] = []

    def addSensor(self, sensor: Sensor):
        sensor_name = sensor.getName()
        if sensor_name not in self.sensors:
            raise Exception(f"There is already a sensor named '{sensor_name}'")
        self.sensors.append(sensor)

    def getSensor(self, sensor_name):
        return next((item for item in self.sensors if item.getName().lower() == sensor_name.lower()), None)

    def isSensorExist(self, sensor_name):
        return self.getSensor(sensor_name) is not None

    def removeSensor(self, sensor_name):
        sensor = self.getSensor(sensor_name)
        if sensor is not None:
            self.sensors.remove(sensor)
        else:
            raise Exception(f"There is not sensor named '{sensor_name}'")

    def getSensorNames(self):
        return [item.getName() for item in self.sensors]

    def getSensors(self):
        return self.sensors
