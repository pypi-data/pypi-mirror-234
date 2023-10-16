from threading import current_thread

from FTV.Generators.GenerateMagicMethods.result.MagicMethodsInterfaces import *
from FTV.Objects.Variables.AbstractConditions import (DyIntConditions, DyBoolConditions, DyFloatConditions,
                                                      DyStrConditions, DyByteArrayConditions, DyBytesConditions,
                                                      DyComplexConditions, DyDictConditions, DyListConditions,
                                                      DySetConditions, DyTupleConditions)


class DyInt(DyIntMagicMethods, DyIntConditions, DyObject):
    def __init__(self, value: int=None, builtin=False):
        super().__init__(value.__int__(), builtin)
        self.__value__ = value.__int__()

    def set(self, value):
        super(DyInt, self).set(value.__int__())

    # def __condition__(self, old_val, new_val, *args, **kwargs):
    #     pass


class DyBool(DyBoolMagicMethods, DyBoolConditions, DyObject):
    def __init__(self, value, builtin=False):
        super().__init__(value.__bool__(), builtin)
        self.__value__ = value.__bool__()

    def set(self, value):
        super(DyBool, self).set(value.__bool__())


class DySwitch(DyBoolMagicMethods, DyObject):
    def __init__(self, builtin=False):
        super().__init__(False, builtin)
        self.__value__ = False

    def set(self, value):
        super(DySwitch, self)._set_empty(value.__bool__())

    def activate(self):
        self.set(True)

    def __action__(self, *args, **kwargs):
        self.activate()


class DyByteArray(DyByteArrayMagicMethods, DyByteArrayConditions, DyObject):
    def __init__(self, value: bytearray=None, builtin=False):
        super().__init__(bytearray(value), builtin)
        self.__value__ = bytearray(value)

    def set(self, value):
        super(DyByteArray, self).set(bytearray(value))


class DyBytes(DyBytesMagicMethods, DyBytesConditions, DyObject):
    def __init__(self, value: bytes=None, builtin=False):
        super().__init__(bytes(value), builtin)
        self.__value__ = bytes(value)

    def set(self, value):
        super(DyBytes, self).set(bytearray(value))


class DyComplex(DyComplexMagicMethods, DyComplexConditions, DyObject):
    def __init__(self, value: complex=None, builtin=False):
        super().__init__(complex(value), builtin)
        self.__value__ = complex(value)

    def set(self, value):
        super(DyComplex, self).set(complex(value))


class DyDict(DyDictMagicMethods, DyDictConditions, DyObject):
    def __init__(self, value: dict=None, builtin=False):
        super().__init__(dict(value), builtin)
        self.__value__ = dict(value)

    def set(self, value):
        super(DyDict, self).set(dict(value))


class DyFloat(DyFloatMagicMethods, DyFloatConditions, DyObject):
    def __init__(self, value: float=None, builtin=False):
        super().__init__(value.__float__(), builtin)
        self.__value__ = value.__float__()

    def set(self, value):
        super(DyFloat, self).set(value.__float__())


class DyList(DyListMagicMethods, DyListConditions, DyObject):
    def __init__(self, value=None, builtin=False):
        if value is None:
            value = []
        super().__init__(list(value), builtin)
        self.__value__ = list(value)

    def set(self, value):
        super(DyList, self).set(list(value))

    def _setItem(self, _index, item):
        self.__value__.__setitem__(_index, item)

    def setItem(self, _index, item):
        old_val = self.__value__.copy()
        self.__value__.__setitem__(_index, item)
        self.__log_p__(f"{self.__name__} = {self.__value__}: {current_thread().name}")
        self._prepareAndRunTriggers(self, old_val, self.__value__)

    def getItem(self, _index):
        return self.__value__[_index]

    def _append(self, item):
        self.__value__.append(item)

    def append(self, item):
        old_val = self.__value__.copy()
        self.__value__.append(item)
        self.__log_p__(f"{self.__name__} = {self.__value__}: {current_thread().name}")
        self._prepareAndRunTriggers(self, old_val, self.__value__)

    def _clear(self):
        self.__value__.clear()

    def clear(self):
        old_val = self.__value__.copy()
        self.__value__.clear()
        self.__log_p__(f"{self.__name__} = {self.__value__}: {current_thread().name}")
        self._prepareAndRunTriggers(self, old_val, self.__value__)

    def copy(self):
        return self.__value__.copy()

    def count(self, item):
        return self.__value__.count(item)

    def _extend(self, iterable):
        self.__value__.extend(iterable)

    def extend(self, iterable):
        old_val = self.__value__.copy()
        self.__value__.extend(iterable)
        self.__log_p__(f"{self.__name__} = {self.__value__}: {current_thread().name}")
        self._prepareAndRunTriggers(self, old_val, self.__value__)

    def index(self, item):
        return self.__value__.index(item)

    def _insert(self, _index, item):
        self.__value__.insert(_index, item)

    def insert(self, _index, item):
        old_val = self.__value__.copy()
        self.__value__.insert(_index, item)
        self.__log_p__(f"{self.__name__} = {self.__value__}: {current_thread().name}")
        self._prepareAndRunTriggers(self, old_val, self.__value__)

    def _pop(self, _index):
        return self.__value__.pop(_index)

    def pop(self, _index):
        old_val = self.__value__.copy()
        item = self.__value__.pop(_index)
        self.__log_p__(f"{self.__name__} = {self.__value__}: {current_thread().name}")
        self._prepareAndRunTriggers(self, old_val, self.__value__)
        return item

    def _remove(self, item):
        self.__value__.remove(item)

    def remove(self, item):
        old_val = self.__value__.copy()
        self.__value__.remove(item)
        self.__log_p__(f"{self.__name__} = {self.__value__}: {current_thread().name}")
        self._prepareAndRunTriggers(self, old_val, self.__value__)

    def _reverse(self):
        self.__value__.reverse()

    def reverse(self):
        old_val = self.__value__.copy()
        self.__value__.reverse()
        self.__log_p__(f"{self.__name__} = {self.__value__}: {current_thread().name}")
        self._prepareAndRunTriggers(self, old_val, self.__value__)

    def _sort(self):
        self.__value__.sort()

    def sort(self):
        old_val = self.__value__.copy()
        self.__value__.sort()
        self.__log_p__(f"{self.__name__} = {self.__value__}: {current_thread().name}")
        self._prepareAndRunTriggers(self, old_val, self.__value__)


class DySet(DySetMagicMethods, DySetConditions, DyObject):
    def __init__(self, value: set=None, builtin=False):
        super().__init__(set(value), builtin)
        self.__value__ = set(value)

    def set(self, value):
        super(DySet, self).set(set(value))


class DyStr(DyStrMagicMethods, DyStrConditions, DyObject):
    def __init__(self, value: str=None, builtin=False):
        super().__init__(value.__str__(), builtin)
        self.__value__ = value.__str__()

    def set(self, value):
        super(DyStr, self).set(value.__str__())

    # def format(self, *args, **kwargs):
    #     self.set(str.format(self.__value__, *args, **kwargs))


class DyTuple(DyTupleMagicMethods, DyTupleConditions, DyObject):
    def __init__(self, value: tuple=None, builtin=False):
        super().__init__(tuple(value), builtin)
        self.__value__ = tuple(value)

    def set(self, value):
        super(DyTuple, self).set(tuple(value))


# if __name__ == '__main__':
    # class A:
    #     R = 100
    #     C = 0
    #
    #     def __init__(self):
    #         self.a = 5
    #         # self.a = DyInt(5)
    #         self.loop()
    #
    #     def loop(self):
    #         if self.C < self.R:
    #             self.C += 1
    #             # if isinstance(a, DyInt):
    #             self.a
    #             return self.loop()
    #             # if isinstance(a, int):
    #             #     return self.loop(a)
    #
    # Efficiency.check(A, 10000, "A")

    # magic_methods = list(filter(lambda method: method.startswith("__") and method.endswith("__"), dir(int)))
    # dy_int_magic_methods = list(filter(lambda method: method not in dir(DyInt), magic_methods))
    #
    # print("\n".join(dy_int_magic_methods))
