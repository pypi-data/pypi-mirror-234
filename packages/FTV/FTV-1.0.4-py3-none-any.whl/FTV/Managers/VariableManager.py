from abc import abstractmethod

from FTV.Managers.AbstractManager import AbstractManager


class VariableManager(AbstractManager):
    __short_name__ = "VM"

    def __init__(self, _is_parent_app=None):
        super().__init__(_is_parent_app=_is_parent_app)
        self.init()

    def init(self):
        pass

    @abstractmethod
    def setupVariables(self):
        pass

    @abstractmethod
    def setupTriggers(self):
        pass
