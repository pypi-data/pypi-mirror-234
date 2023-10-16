import asyncio

from FTV.Objects.Variables.DynamicMethods import DyBuiltinMethod
from FTV.Objects.Variables.DynamicModules import DyBuiltinModule


class AbstractManager(DyBuiltinModule):
    def __init__(self, _is_parent_app=None):
        # Log.p(f"init{self.__class__.__short_name__}: {self.__class__.__name__}")
        self._is_parent_app = _is_parent_app
        super(AbstractManager, self).__init__()

    def init(self):
        pass

    def _setupMethodsLists(self):
        super(AbstractManager, self)._setupMethodsLists()
        self._BUILTIN_METHODS |= {"_resumeSetupEnvironment"}

    def setupSettings(self):
        pass

    def _setupBuiltinTriggers(self):
        self.addTrigger(self._setupEnvironment).setAction(self.POST_BUILTIN_INIT)
        self.addTrigger(self.PRE_INIT).setAction(self._loadSelf)
        self.addTrigger(self._resumeSetupEnvironment)\
            .setCondition(self.IsNotSetupMode, self)\
            .setAction(self.POST_INIT)

    @DyBuiltinMethod()
    def _resumeSetupEnvironment(self):
        asyncio.set_event_loop(asyncio.new_event_loop())

        self.PRE_INIT.activate()
