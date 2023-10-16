import os
import sys
from pathlib import Path

ROOT_DIR = str(Path(os.getcwd()).parent.parent).replace("\\", "/") + "/"
sys.path.append(rf"{ROOT_DIR}")
# print(ROOT_DIR)
# exit()

from FTV.Extra.Examples.Yad2Monday.Yad2App import Yad2App

Yad2App()
