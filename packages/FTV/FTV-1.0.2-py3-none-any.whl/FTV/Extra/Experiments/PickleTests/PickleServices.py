import os

# import pickle
import dill as pickle

from FTV.Extra.Experiments import DynamicModule


class ModulesManager(object):
    def __init__(self, default_directory):
        self.directory: str = default_directory

    def load(self, file_name):
        pass

    def save(self, module, file_name):
        self.module = module(setup_mode=True)
        # self.module = module()
        full_path = self.directory + file_name
        file = open(full_path, 'wb')
        pickle.dump(self.module, file)
        file.close()

    def setDirectory(self, directory):
        self.directory = directory


if __name__ == '__main__':
    directory = os.getcwd().replace("\\", "/") + "/"
    mm = ModulesManager(directory)
    mm.save(DynamicModule, "DynamicModule.ftv")
