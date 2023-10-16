import inspect
from abc import abstractmethod

from FTV.Objects.SystemObjects.TriggerObjects import Trigger
from FTV.Objects.Variables.AbstractDynamicMethod import DynamicMethodObject


class DynamicModuleParent(object):
    type = "DynamicModuleParent"
    # _ACTIVE_METHOD = ""

    def __init__(self, value=None):
        self._setupMethodsLists()
        self._setupEnvironment()

    def _setupMethodsLists(self):
        self._BUILTIN_METHODS = {
            "_setupEnvironment",
            "_loadBuiltinSelf",
            "_loadSelf"
        }

        self._IGNORE_METHODS = {
            "__setattr__",
            "__init__",
            "_setupBuiltinMethods",
            "_setupMethods",
            "_setupBuiltinTriggers",
            "setupTriggers",
            "_setupMethods",
            "addTrigger",
            "removeTrigger",
            "_DynamicModuleParent__initMethodsVariables",
            "_DynamicModuleParent__setupMethod",
            "_getDySwitchAction",  # TODO lahav Temporary!
            "_get",
            "_set",
            "get",
            "set",
            "_setupBuiltinVariables",
            "setupVariables",
        }

    # def __setattr__(self, key, value):
    #     if key in dir(self) and callable(getattr(self, key)):
    #         raise Exception(
    #             "Can't addFeatures the attribute \"{}\" to the object \"{}\", since it is already exists as a method.".format(
    #                 key, self.__class__.__name__))
    #
    #     super().__setattr__(key, value)

    def __setupMethod(self, method_key):
        # print(method_key)
        self.__dynamic_methods__[method_key] = DynamicMethodObject(getattr(self, method_key))

    @abstractmethod
    def _setupEnvironment(self):
        pass

    @abstractmethod
    def _loadBuiltinSelf(self):
        pass

    @abstractmethod
    def _loadSelf(self):
        pass

    def _setupBuiltinMethods(self):
        # self.__dynamic_methods__ = set()
        self.__dynamic_methods__ = {}

        # map(lambda method_key: self.__setupMethod(method_key), getattr(self, "_DynamicModuleParent__BUILTIN_METHODS"))

        # [self.__setupMethod(method_key) for method_key in getattr(self, "_DynamicModuleParent__BUILTIN_METHODS")]

        for method_key in self._BUILTIN_METHODS:
            self.__setupMethod(method_key)

    def _setupMethods(self):
        ignore_methods = self._IGNORE_METHODS
        builtin_methods = self._BUILTIN_METHODS

        methods = inspect.getmembers(self, inspect.ismethod)
        # map(lambda func: self.__setupMethod(func[0]) if func[0] not in ignore_methods | builtin_methods else None, methods)

        # Keep only new methods
        # methods = [method for method in methods if method.__qualname__.split(".")[0] == self.__class__.__name__]

        filtered_methods = list(filter(lambda obj: obj[0] not in ignore_methods | builtin_methods, methods))

        for func in filtered_methods:
            self.__setupMethod(func[0])

    @abstractmethod
    def _setupBuiltinTriggers(self):
        pass

    @abstractmethod
    def setupTriggers(self):
        pass

    def addTrigger(self, dy_object, parent=None, first=False):

        # # TODO lahav This solution is temporary.

        if callable(dy_object):
            if parent is None:
                parent = self
            else:
                pass
                # print()

            modified_dy_object = parent.__get_by_method__(dy_object)
        else:
            modified_dy_object = dy_object

        trigger = Trigger(self).setCondition(modified_dy_object)
        if first:
            modified_dy_object.__triggers__.insert(0, trigger)
        else:
            modified_dy_object.__triggers__.append(trigger)

        return trigger

    def removeTrigger(self, dy_object, parent=None):
        # # TODO lahav This solution is temporary.

        if callable(dy_object):
            if parent is None:
                parent = self
            else:
                pass
                # print()

            modified_dy_object = parent.__get_by_method__(dy_object)
        else:
            modified_dy_object = dy_object

        trigger = Trigger(self).setCondition(modified_dy_object)
        modified_dy_object.__triggers__.clear()

        return trigger

    def overrideTriggers(self, dy_object, parent=None):

        # # TODO lahav This solution is temporary.

        if callable(dy_object):
            if parent is None:
                parent = self
            else:
                pass
                # print()

            modified_dy_object = parent.__get_by_method__(dy_object)
        else:
            modified_dy_object = dy_object

        trigger = Trigger(self).setCondition(modified_dy_object)
        modified_dy_object.__triggers__.clear()
        modified_dy_object.__triggers__.append(trigger)

        return trigger

    def __get_by_method__(self, method):
        # try:
        return self.__dynamic_methods__[method.__name__]
        # except:
        #     return None

    # def _getDySwitchAction(self, action):
    #     return self.__temp_action.activate()
