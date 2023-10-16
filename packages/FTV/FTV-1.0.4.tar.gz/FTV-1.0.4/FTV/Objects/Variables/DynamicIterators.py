from FTV.Managers.Log import Log
from FTV.Objects.SystemObjects.TriggerObjects import Condition
from FTV.Objects.Variables.AbstractDynamicObject import DyListMagicMethods, DyBoolMagicMethods, DyFloatMagicMethods
from FTV.Objects.Variables.DynamicMethods import DyMethod, DyBuiltinMethod
from FTV.Objects.Variables.DynamicModules import DyBuiltinModule
from FTV.Objects.Variables.DynamicObjects import DyInt, DyBool


class DyObjectList(DyListMagicMethods, DyBuiltinModule):
    pass


class DyBoolList(DyBoolMagicMethods, DyObjectList):
    def __init__(self, builtin=False):
        super(DyBoolList, self).__init__(builtin=builtin)

    def _setupMethodsLists(self):
        super(DyBoolList, self)._setupMethodsLists()
        self._BUILTIN_METHODS |= {"_update_len_true", "_update_value"}

    def _setupBuiltinVariables(self):
        super(DyBoolList, self)._setupBuiltinVariables()
        self.__value__: bool  # TODO lahav Please change it to be more generic.
        # self.__len__: int = 0
        self.__iterator__ = []
        self.__len_true__ = DyInt(0, builtin=True)

    def _setupBuiltinTriggers(self):
        super(DyBoolList, self)._setupBuiltinTriggers()
        self.addTrigger(self.__len_true__)\
            .setCondition(DyBoolList.IsEqualToLenOf, self)\
            .setAction(self._update_value, True)

        self.addTrigger(self.__len_true__)\
            .setCondition(DyBoolList.IsNotEqualToLenOf, self)\
            .setAction(self._update_value, False)

    @DyBuiltinMethod()
    def add(self, *dy_bools):
        self.__iterator__ += dy_bools
        self._update_len_true(value=len(list(filter(lambda dy_bool: dy_bool, dy_bools))))

        for dy_bool in dy_bools:
            self.addTrigger(dy_bool).setCondition(DyBool.IsChanged).setAction(self._update_len_true, dy_bool, 1)

    def set(self, value):
        pass  # TODO lahav Please provide an exception
        # Log.p("This object is a dependent variable. Therefore, it cannot be updated directly.", Log.color.RED)

    def getList(self):
        return self.__iterator__

    @DyBuiltinMethod()
    def _update_len_true(self, sign=True, value=1):
        if sign:
            self.__len_true__ += value
        else:
            self.__len_true__ -= value

    @DyBuiltinMethod()
    def _update_value(self, value):
        super(DyBoolList, self).set(value)

    def __condition__(self, old_val, new_val, *args, **kwargs):
        return new_val

    def __action__(self, *args, **kwargs):
        self.set(args[0])

    class IsEqualToLenOf(Condition):
        @staticmethod
        def __condition__(old_val, new_val, *args, **kwargs):
            return new_val == len(args[0])

    class IsNotEqualToLenOf(Condition):
        @staticmethod
        def __condition__(old_val, new_val, *args, **kwargs):
            return new_val != len(args[0])


class DySwitchList(DyBoolList):
    def __init__(self):
        super(DySwitchList, self).__init__(False)

    def setupTriggers(self):
        self.addTrigger(self.__len_true__) \
            .setCondition(DySwitchList.IsEqualToLenOf, self) \
            .setAction(self.deactivateAll)

        self.addTrigger(self.__len_true__) \
            .setCondition(DySwitchList.IsEqualToLenOf, self) \
            .setAction(self._update_value, True)

    @DyMethod()
    def add(self, *dy_bools):
        # super(DySwitchList, self).addFeatures(*dy_bools)
        self.__iterator__ += dy_bools
        # self.__len__ = len(self.__iterator__)
        self._update_len_true(len(list(filter(lambda dy_bool: dy_bool, dy_bools))))

        for dy_bool in dy_bools:
            if isinstance(dy_bool, (DyBool, DyBoolList)):
                # dy_bool._is_child = True
                self.addTrigger(dy_bool).setCondition(DyBool.IsChangedTo, True).setAction(self._update_len_true, 1)
                self.addTrigger(dy_bool).setCondition(DyBool.IsChangedTo, False).setAction(self._update_len_true, -1)
            else:
                Log.p("This object is a DySwitchList iterator. Therefore, it cannot addFeatures child that is not DyBool or DyBoolList.", Log.color.RED)

    def activate(self):
        self.set(True)

    @DyBuiltinMethod()
    def deactivateAll(self):
        for item in self.__iterator__:
            item._set(False)
        # DyObject.set(self, False)
        self._set(False)
        self.__len_true__._set(0)

    @DyBuiltinMethod()
    def _update_value(self, value):
        super(DySwitchList, self)._set_empty(value)


class DyFloatList(DyFloatMagicMethods, DyObjectList):
    def __init__(self, value=None, builtin=False):
        super(DyFloatList, self).__init__(value=value, builtin=builtin)

    def _setupMethodsLists(self):
        super(DyFloatList, self)._setupMethodsLists()
        self._BUILTIN_METHODS |= {"_update_ave_value", "_update_value"}

    def _setupBuiltinVariables(self):
        super(DyFloatList, self)._setupBuiltinVariables()
        self.__value__: float
        self.__iterator__ = []
        # self.__len_true__ = DyInt(0, builtin=True)

    def _setupBuiltinTriggers(self):
        super(DyFloatList, self)._setupBuiltinTriggers()

    @DyBuiltinMethod()
    def add(self, *dy_floats):
        self.__iterator__ += dy_floats
        self._update_value(value=self.getItemsAverage(self.__iterator__))
        # self._update_value(value=len(list(filter(lambda dy_bool: dy_bool, self.__iterator__))))

        for dy_float in dy_floats:
            self.addTrigger(dy_float).setCondition(DyBool.IsChanged).setAction(self._update_ave_value)

    def set(self, value):
        if not self.__iterator__:
            super(DyFloatList, self).set(value.__float__())
        else:
            pass  # TODO lahav Please provide an exception
            # Log.p("This object is a dependent variable. Therefore, it cannot be updated directly.", Log.color.RED)

    def getList(self):
        return self.__iterator__

    @DyBuiltinMethod()
    def _update_ave_value(self):
        # self.__value__ += self._getItemAverageChange(old_val, new_val, self.__iterator__)
        super(DyFloatList, self).set(self.getItemsAverage(self.__iterator__).__float__())

    @DyBuiltinMethod()
    def _update_value(self, value):
        super(DyFloatList, self).set(value.__float__())

    @staticmethod
    def getItemAverage(item, items=None):
        """This method can be overridden according to the required purpose"""
        return item/len(items)

    def getItemsAverage(self, items):
        return sum([self.getItemAverage(item, items) for item in items])

    def _getItemAverageChange(self, old_item, new_item, items):
        return self.getItemAverage(new_item, items) - self.getItemAverage(old_item, items)

    def __action__(self, *args, **kwargs):
        self.set(args[0])


if __name__ == '__main__':
    magic_methods = list(filter(lambda method: method.startswith("__") and method.endswith("__"), dir(list)))
    dy_int_magic_methods = list(filter(lambda method: method not in dir(DyBoolList), magic_methods))

    print("\n".join(dy_int_magic_methods))
