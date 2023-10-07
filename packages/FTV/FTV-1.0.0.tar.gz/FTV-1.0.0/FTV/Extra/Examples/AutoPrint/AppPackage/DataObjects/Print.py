from AppPackage.DataObjects.Gcode import Gcode


class Print:
    def __init__(self, gcode_file_fullname, id_number: int):
        self.id = id_number

        self.gcode = Gcode(gcode_file_fullname)
