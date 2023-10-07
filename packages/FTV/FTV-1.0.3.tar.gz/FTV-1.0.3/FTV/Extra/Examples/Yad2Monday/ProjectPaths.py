import os
from pathlib import Path

ROOT_DIR = str(Path(os.getcwd())).replace("\\", "/") + "/"
DATA_DIR = ROOT_DIR + "Data/"