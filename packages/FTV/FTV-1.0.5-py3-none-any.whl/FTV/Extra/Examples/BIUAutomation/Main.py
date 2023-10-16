import os
import sys
from pathlib import Path

# # Specify the directory containing your content roots
# content_roots_directory = str(Path.cwd().parent.parent).replace("\\", "/")
#
# # Get a list of subdirectories in the content roots directory
# subdirectories = [os.path.join(content_roots_directory, d) for d in os.listdir(content_roots_directory) if os.path.isdir(os.path.join(content_roots_directory, d))]
#
# # Add the content roots to sys.path
# for subdirectory in subdirectories:
#     if subdirectory not in sys.path:
#         sys.path.append(subdirectory)


ROOT_DIR = str(Path(os.getcwd()).parent.parent).replace("\\", "/") + "/"
sys.path.append(rf"{ROOT_DIR}")
# print(ROOT_DIR)
# exit()

from FTV.Extra.Examples.BIUAutomation.BIURegistrationApp import BIURegistrationApp

# BIUApp()
BIURegistrationApp()
