class DatabaseError(Exception):
    pass

class DeviceChildError(DatabaseError):
    def __init__(self, child_id, workshop_name=None):
        self.workshop_name = workshop_name
        self.printer_id = child_id

# UserError

class UsernameExist(DeviceChildError):

    def __init__(self, username):
        self.username = username

    def __str__(self):
        return f"The username, \"{self.username}\", is already exist."

class UsernameNotExist(DeviceChildError):

    def __init__(self, username):
        self.username = username

    def __str__(self):
        return f"The username, \"{self.username}\", is not exist."

class WrongPassword(DeviceChildError):

    def __init__(self, username):
        self.username = username

    def __str__(self):
        return f"The password for the username, \"{self.username}\", is wrong."

# DeviceError

class DeviceExist(DeviceChildError):

    def __init__(self, username, workshop_name):
        self.username = username
        self.workshop_name = workshop_name

    def __str__(self):
        return f"The workshop, \"{self.workshop_name}\", is already exist in the username, \"{self.username}\"."

class DeviceNotExist(DeviceChildError):

    def __init__(self, username, workshop_name):
        self.username = username
        self.workshop_name = workshop_name

    def __str__(self):
        return f"The workshop, \"{self.workshop_name}\", is not exist in the username, \"{self.username}\"."

# StationError

class StationExist(DeviceChildError):
    def __init__(self, username, workshop_name, station_name):
        self.username = username
        self.workshop_name = workshop_name
        self.station_name = station_name

    def __str__(self):
        return f"The station, \"{self.station_name}\", is already exist in the workshop, \"{self.workshop_name}\", of the username, \"{self.username}\"."

class StationNotExist(DeviceChildError):
    def __init__(self, username, workshop_name, station_name):
        self.username = username
        self.workshop_name = workshop_name
        self.station_name = station_name

    def __str__(self):
        return f"The station, \"{self.station_name}\", is not exist in the workshop, \"{self.workshop_name}\", of the username, \"{self.username}\"."

class StationRegistered(DeviceChildError):
    def __init__(self, station_id):
        self.station_id = station_id

    def __str__(self):
        return f"The station id, \"{self.station_id}\", is already registered."

class StationNotRegistered(DeviceChildError):
    def __init__(self, station_id):
        self.station_id = station_id

    def __str__(self):
        return f"The station id, \"{self.station_id}\", is not registered."

# ControllerError

class ControllerRegistered(DeviceChildError):
    def __init__(self, controller_id):
        self.controller_id = controller_id

    def __str__(self):
        return f"The controller id, \"{self.controller_id}\", is already registered."

class ControllerNotRegistered(DeviceChildError):
    def __init__(self, controller_id):
        self.controller_id = controller_id

    def __str__(self):
        return f"The controller id, \"{self.controller_id}\", is not registered."

# FilamentChangerError

class FilamentChangerRegistered(DeviceChildError):
    def __init__(self, filament_changer_id):
        self.filament_changer_id = filament_changer_id

    def __str__(self):
        return f"The filament changer id, \"{self.filament_changer_id}\", is already registered."

class FilamentChangerNotRegistered(DeviceChildError):
    def __init__(self, filament_changer_id):
        self.filament_changer_id = filament_changer_id

    def __str__(self):
        return f"The filament changer id, \"{self.filament_changer_id}\", is not registered."

# PrinterError

class PrinterRegistered(DeviceChildError):
    def __init__(self, workshop_name, printer_id):
        self.workshop_name = workshop_name
        self.printer_id = printer_id

    def __str__(self):
        return f"The printer id, \"{self.printer_id}\", is already registered in the workshop, \"{self.workshop_name}\"."

class PrinterNotRegistered(DeviceChildError):
    def __init__(self, workshop_name, printer_id):
        self.workshop_name = workshop_name
        self.printer_id = printer_id

    def __str__(self):
        return f"The printer id, \"{self.printer_id}\", is not registered in the workshop, \"{self.workshop_name}\"."
