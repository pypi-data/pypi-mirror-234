from FTV.FrameWork.Features import NIFeature, UIFeature, Feature
from FTV.Managers.Log import Log
from FTV.Objects.Variables.DynamicMethods import DyBuiltinMethod
from FTV.Objects.Variables.DynamicObjects import DySwitch


class _AbstractApp:
    type = "App"

    @classmethod
    def startApp(cls):
        cls.vm.START.activate()

    @classmethod
    def stopApp(cls):
        cls.vm.EXIT.activate()


class NIApp(_AbstractApp, NIFeature):
    def __init__(self):
        super(NIApp, self).__init__()
        super(Feature, self).__init__()

    # """This method is deprecated. Please use the method "setupFeatures" in the FeatureManager instead."""
    # # @abstractmethod
    # def setupFeatures(self):
    #     pass
    #
    # """This method is deprecated. Please use the method "setupSettings" in the FeatureManager instead."""
    # # @abstractmethod
    # def setupSettings(self):
    #     pass

    def _setupBuiltinManagers(self):
        super(NIApp, self)._setupBuiltinManagers()
        Log.setup()

    def _setupBuiltinVariables(self):
        super(NIApp, self)._setupBuiltinVariables()
        self.vm.START = DySwitch()
        self.vm.EXIT = DySwitch()

    def _setupBuiltinTriggers(self):
        super(NIApp, self)._setupBuiltinTriggers()
        self.addTrigger(self.vm.POST_BUILTIN_LOAD).setAction(self._resumeSetupEnvironment)

        self.overrideTriggers(self._setupEnvironment).setAction(self.vm.POST_BUILTIN_LOAD).setThread(self.em.Main)
        self.addTrigger(self.vm.POST_SETUP).setAction(self.vm.START)
        self.addTrigger(self.em.STOP_THREADS, parent=self.em).setAction(self.vm.EXIT).setThread(self.em.Main)


class UIApp(_AbstractApp, UIFeature):
    def __init__(self):
        super(UIApp, self).__init__()
        super(Feature, self).__init__()

    def _setupMethodsLists(self):
        super(UIApp, self)._setupMethodsLists()
        self._BUILTIN_METHODS |= {"_setupUIServices"}

    # """This method is deprecated. Please use the method "setupFeatures" in the FeatureManager instead."""
    # # @abstractmethod
    # def setupFeatures(self):
    #     pass
    #
    # """This method is deprecated. Please use the method "setupSettings" in the FeatureManager instead."""
    # # @abstractmethod
    # def setupSettings(self):
    #     pass

    @DyBuiltinMethod()
    def _setupUIServices(self):
        self.uim._startServices()

    def _setupBuiltinVariables(self):
        super(UIApp, self)._setupBuiltinVariables()
        self.vm.START = DySwitch()
        self.vm.EXIT = DySwitch()

    def _setupBuiltinTriggers(self):
        super(UIApp, self)._setupBuiltinTriggers()
        self.addTrigger(self.vm.POST_BUILTIN_LOAD).setAction(self._resumeSetupEnvironment)

        self.overrideTriggers(self._setupEnvironment).setAction(self.vm.POST_BUILTIN_LOAD).setThread(self.em.Main)
        self.addTrigger(self.vm.POST_SETUP).setAction(self._setupUIServices)
        self.addTrigger(self._setupUIServices).setAction(self.vm.START)
        self.addTrigger(self.em.STOP_THREADS, parent=self.em).setAction(self.vm.EXIT).setThread(self.em.Main)
