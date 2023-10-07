

class Filament:

    def __init__(self):
        self.id: int

        self.total_length: float  # [mm]
        self.used_length: float  # [mm]
        self.diameter: float  # [mm]
        self.density: float  # [mm/g^3]
        self.material: str  # [material]
        self.total_weight: float  # [g]
        self.coast: float  # [$]
        self.color: str  # [color]

        self.weight: float  # [g]
        self.length: float  # [mm]
        self.coast_per_gram: float  # [$/g]
