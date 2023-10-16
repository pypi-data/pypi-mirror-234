import sys

ROOT_DIR = sys.argv[0].replace("\\", "/").rsplit("/", 1)[0] + "/"
LIBRARIES_DIR = ROOT_DIR + "ExternalTools/"
CHROME_DRIVER = LIBRARIES_DIR + "chromedriver.exe"