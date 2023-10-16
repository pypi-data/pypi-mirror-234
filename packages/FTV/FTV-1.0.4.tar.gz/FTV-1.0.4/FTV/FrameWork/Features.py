import abc
# global variableManager
# global featureManager
import importlib

from FTV.Managers.Log import Log
from FTV.Objects.Variables.AbstractDynamicModule import DynamicModuleParent
from FTV.Objects.Variables.DynamicMethods import DyBuiltinMethod
from FTV.Objects.Variables.DynamicObjects import DyBool, DySwitch


class Feature(DynamicModuleParent):
    type = "Feature"

    _builtin_managers = {
        "lm": "LogManager",
        "em": "ExecutionManager",
        "vm": "VariableManager",
        "fm": "FeatureManager",
    }

    lm = None
    em = None
    vm = None
    fm = None

    # def __new__(cls, *args, **kwargs):
    #     cls.settings = cls._Settings()
    #     cls._fm_setupSettings()

    def __init__(self):
        self.__name__ = self.__class__.__name__
        self._managers = {}

        self.settings = self._Settings()
        self._fm_setupSettings()

    def _setupMethodsLists(self):
        super(Feature, self)._setupMethodsLists()
        self._BUILTIN_METHODS |= {"_loadChildren"}
        self._BUILTIN_METHODS |= {"_startSetupEnvironment"}
        self._BUILTIN_METHODS |= {"_resumeSetupEnvironment"}

    @DyBuiltinMethod()
    def _setupEnvironment(self):
        self._loadBuiltinSelf()

    @DyBuiltinMethod()
    def _loadBuiltinSelf(self):
        self._setupBuiltinManagers()
        self._setupBuiltinVariables()
        self._setupBuiltinMethods()
        self._setupBuiltinTriggers()

    @DyBuiltinMethod()
    def _loadSelf(self):
        self._resumeSetupManagers()
        self._setupMethods()
        self.setupTriggers()
        self.vm.IS_SELF_LOADED.set(True)

    @abc.abstractmethod
    def setupSettings(self):
        pass

    def _setupBuiltinManagers(self):
        from FTV.Managers.LogManager import LogManager
        from FTV.Managers.ExecutionManager import ExecutionManager
        from FTV.Managers.VariableManager import VariableManager
        from FTV.Managers.FeatureManager import FeatureManager

        self.__lm_class = LogManager
        self.__vm_class = VariableManager
        self.__em_class = ExecutionManager
        self.__fm_class = FeatureManager

        self.setupManagers()
        from FTV.FrameWork.Apps import _AbstractApp
        is_parent_app = issubclass(self.__class__, _AbstractApp)

        self.__class__.lm = self.__lm_class(_is_parent_app=is_parent_app)
        self.__class__.vm = self.__vm_class(_is_parent_app=is_parent_app)
        self.__class__.em = self.__em_class(_is_parent_app=is_parent_app)
        self.__class__.fm = self.__fm_class(_is_parent_app=is_parent_app)

    @classmethod
    def _resumeSetupManagers(cls):
        cls.lm._resumeSetupEnvironment()
        cls.em._resumeSetupEnvironment()
        cls.vm._resumeSetupEnvironment()
        cls.fm._resumeSetupEnvironment()

    @DyBuiltinMethod()
    def _startSetupEnvironment(self):
        super(Feature, self).__init__()

    @DyBuiltinMethod()
    def _resumeSetupEnvironment(self):
        self.vm.PRE_LOAD.activate()

    def _setupBuiltinVariables(self):
        self.vm.POST_BUILTIN_LOAD = DySwitch(builtin=True)
        self.vm.PRE_LOAD = DySwitch(builtin=True)
        self.vm.IS_SELF_LOADED = DyBool(True, builtin=True)
        self.vm.POST_LOAD = DySwitch(builtin=True)
        self.vm.PRE_LOAD_FEATURES = DySwitch(builtin=True)
        self.vm.IS_CHILDREN_LOADED = DyBool(False, builtin=True)
        self.vm.POST_LOAD_FEATURES = DySwitch(builtin=True)
        self.vm.POST_SETUP = DySwitch(builtin=True)

    def _setupBuiltinTriggers(self):
        self.addTrigger(self._setupEnvironment).setAction(self.vm.POST_BUILTIN_LOAD)

        self.addTrigger(self.vm.PRE_LOAD).setAction(self._loadSelf)
        self.addTrigger(self._loadSelf).setAction(self.vm.POST_LOAD)
        self.addTrigger(self.vm.POST_LOAD).setAction(self.vm.PRE_LOAD_FEATURES)
        self.addTrigger(self.vm.PRE_LOAD_FEATURES).setAction(self._loadChildren)
        self.addTrigger(self._loadChildren).setAction(self.vm.POST_LOAD_FEATURES)
        self.addTrigger(self._resumeSetupEnvironment).setAction(self.vm.POST_SETUP)

    def _fm_setupFeatures(self):
        self.fm.setupFeatures()
        # self.setupFeatures()

    def _fm_setupSettings(self):
        # self.fm.setupSettings()
        self.setupSettings()

    @DyBuiltinMethod()
    def _loadChildren(self):
        self._fm_setupFeatures()
        self.fm._resumeSetupFeatures()
        self.vm.IS_CHILDREN_LOADED.set(True)

    # @classmethod
    @abc.abstractmethod
    def setupManagers(self):
        pass

    def _getBaseAbstractManagerClass(self, cls_name):
        # manager_class = __import__(f"FTV.Managers.{cls_name}")
        manager_class = importlib.import_module(f"FTV.Managers.{cls_name}")
        manager_class = getattr(manager_class, cls_name)
        return manager_class

    def _setAbstractManager(self, manager_parameter, Manager):
        manager_parameter = Manager
        # manager = Manager()
        # methods_list = [method for method in dir(manager) if callable(getattr(manager, method))
        #                 and not (method.startswith("__") and method.endswith("__"))]
        #
        # abstract_manager.__dict__.update(manager.__dict__)
        # for method in methods_list:
        #     setattr(abstract_manager, method, getattr(manager, method))

    # @classmethod
    def setVariableManager(self, Manager):
        self.__vm_class = Manager

    # @classmethod
    def setExecutionManager(self, Manager):
        self.__em_class = Manager

    # @classmethod
    def setLogManager(self, Manager):
        self.__lm_class = Manager

    # @classmethod
    def setFeatureManager(self, Manager):
        self.__fm_class = Manager

    # @classmethod
    def setUIManager(self, Manager):
        self.__uim_class = Manager

    def setupTriggers(self):
        pass

    # """This method is deprecated. Please use the method "setupFeatures" in the FeatureManager instead."""
    # def setupFeatures(self):
    #     pass

    # """This method is deprecated. Please use the method "addFeatures" in the FeatureManager instead."""
    # def addFeatures(self, *features):
    #     self.fm.addFeatures(*features)

    # """This method is deprecated. Please use the method "addFeature" in the FeatureManager instead."""
    # def addFeature(self, feature):
    #     self.fm.addFeatures(feature)

    class _Settings:
        ui_platform = None

        def __init__(self):
            self.enabled = True

        def setEnabled(self, enabled=True):
            self.enabled = enabled

        def setDisabled(self, disabled=True):
            self.enabled = not disabled


# TODO lahav Add a proper mechanism for the loaded features tree.
class NIFeature(Feature):
    pass
    # type = "NIFeature"

    # """This method is deprecated. Please use the method "setupSettings" in the FeatureManager instead."""
    # # @abc.abstractmethod
    # def setupSettings(self):
    #     pass

    # """This method is deprecated. Please use the method "setupManagers" in the FeatureManager instead."""
    # # @classmethod
    # # @abc.abstractmethod
    # def setupManagers(self):
    #     pass


class UIFeature(NIFeature):
    # type = "UIFeature"

    def _setupMethodsLists(self):
        super(UIFeature, self)._setupMethodsLists()
        self._BUILTIN_METHODS |= {"_loadUISelf"}

    def _setupBuiltinManagers(self):
        from FTV.Managers.UIManager import UIManager
        self.__uim_class = UIManager
        super(UIFeature, self)._setupBuiltinManagers()

        from FTV.FrameWork.Apps import NIApp
        is_parent_app = issubclass(self.__class__, NIApp)

        self.__class__.uim = self.__uim_class(_is_parent_app=is_parent_app)

    def _setupBuiltinVariables(self):
        super(UIFeature, self)._setupBuiltinVariables()
        self.vm.PRE_UI_LOAD = DySwitch(builtin=True)
        self.vm.IS_SELF_UI_LOADED = DyBool(False, builtin=True)
        self.vm.POST_UI_LOAD = DySwitch(builtin=True)

    def _setupBuiltinTriggers(self):
        super(UIFeature, self)._setupBuiltinTriggers()
        self.overrideTriggers(self.vm.POST_LOAD).setAction(self.vm.PRE_UI_LOAD)
        self.addTrigger(self.vm.PRE_UI_LOAD).setAction(self._loadUISelf)

        self.addTrigger(self._loadUISelf).setAction(self.vm.POST_UI_LOAD)
        self.addTrigger(self.vm.POST_UI_LOAD).setAction(self.vm.PRE_LOAD_FEATURES)

    @DyBuiltinMethod()
    def _loadUISelf(self):
        self.uim.setupVariables()
        self.uim.setupTriggers()
        self.setupUITriggers()
        self.uim.IS_SELF_UI_LOADED = DyBool(False)

    # """This method is deprecated. Please use the method "setupManagers" in the FeatureManager instead."""
    # @classmethod
    # # @abc.abstractmethod
    # def setupManagers(cls):
    #     pass

    # """This method is deprecated. Please use the method "setupSettings" in the FeatureManager instead."""
    # # @abc.abstractmethod
    # def setupSettings(self):
    #     pass

    def setupUITriggers(self):
        pass

    def addUITrigger(self):
        pass
