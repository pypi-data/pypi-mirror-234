from FTV.Managers.AbstractManager import AbstractManager
from FTV.Objects.Variables.DynamicMethods import DyBuiltinMethod


class UIManager(AbstractManager):
    __short_name__ = "UIM"

    def __init__(self, _is_parent_app=None):
        super().__init__(_is_parent_app)
        self.init()

    def _setupMethodsLists(self):
        super(UIManager, self)._setupMethodsLists()
        self._BUILTIN_METHODS |= {"_startServices"}

    def init(self):
        pass

    @DyBuiltinMethod()
    def _startServices(self):
        pass  # TODO lahav Please implement the setup UI mechanism.
