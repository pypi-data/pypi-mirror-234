import os


class Gcode:

    def __init__(self, file_fullname: str):

        self.file_fullname: file_fullname
        self.origin_data = []
        self.data: []
        self.properties = self.Properties()

        self.load(file_fullname)

    @staticmethod
    def get_value_by_command(command_name, value_name):
        pass

    @staticmethod
    def write(fullname, data):
        pass

    def load(self, fullname):
        if "." in fullname:
            if os.path.basename(fullname).split(".")[1] != "gcode":
                raise Exception("Gcode file must be a '*.gcode' type.")
        else:
            raise Exception("Gcode file must be a '*.gcode' type.")

        gcode_file = open(fullname, 'r', encoding='utf-8')
        self.origin_data = gcode_file.readlines()

    def clean(self):

        line_count = 0
        lines_amount = len(self.origin_data)

        data = []

        while lines_amount > line_count:

            gcode_line = self.origin_data[line_count].split("\n")[0].split(";")[0]

            if gcode_line:
                data.append(gcode_line)

            line_count += 1

        self.data = data

    class Properties:
        def __init__(self):
            self.min_layer_height: float  # [mm]
            self.max_layer_height: float  # [mm]

            self.x_axis = self.Axis()
            self.y_axis = self.Axis()
            self.z_axis = self.Axis()

            self.tool_heads = []

            self.weight: float
            self.length: float
            self.coast: float
            self.time: float

        class Axis:
            def __init__(self):
                self.max_acceleration: float  # [mm]
                self.max_velocity: float  # [mm]
                self.min_pos: float  # [mm]
                self.max_pos: float  # [mm]
                self.size: float  # [mm]

        class ToolHead:
            def __init__(self):
                self.max_acceleration: float  # [mm]
                self.max_velocity: float  # [mm]

                self.nozzle_diameter: float  # [mm]
                self.max_temperature: float  # [degrees]

