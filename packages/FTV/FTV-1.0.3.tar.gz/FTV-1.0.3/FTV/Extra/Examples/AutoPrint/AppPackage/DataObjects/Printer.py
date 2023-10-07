

class Printer:
    def __init__(self):
        self.id: int

        self.weight: float  # [$]
        self.coast: float  # [$]
        self.firmware: str  # [$]
        self.supported_files = []
        self.supported_materials = []

        self.min_layer_height: float
        self.max_layer_height: float

        self.x_axis = self.Axis()
        self.y_axis = self.Axis()
        self.z_axis = self.Axis()

        self.tool_heads = [self.ToolHead()]

        self.prints = {}
        self.prints_sorted = []

    def send(self, command):
        pass

    def get_temperature(self):
        pass

    def is_connected(self):
        pass

    def add_print(self, _print, id_number):
        self.prints[id_number] = _print

    def remove_print(self, id_number):
        del self.prints[id_number]

    class Axis:
        def __init__(self):
            self.max_acceleration: float  # [mm]
            self.max_velocity: float  # [mm]
            self.min_pos: float  # [mm]
            self.max_pos: float  # [mm]
            self.size: float  # [mm]

            self.position: float  # [mm]
            self.steps_per_mm: float  # [steps/mm]

    class ToolHead:
        def __init__(self):
            self.max_acceleration: float  # [mm]
            self.max_velocity: float  # [mm]

            self.nozzle_diameter: float  # [mm]
            self.temperature: float  # [degrees]
            self.max_temperature: float  # [degrees]

    class Connection:
        def __init__(self):
            self.is_connected: bool
            self.commands = []
            self.receive: str
