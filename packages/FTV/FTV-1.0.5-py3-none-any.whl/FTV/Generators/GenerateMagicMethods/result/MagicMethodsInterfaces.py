from threading import current_thread

from FTV.Tools.Log import Log
from FTV.Objects.SystemObjects.DataObject import Queue
from FTV.Objects.Variables.AbstractConditions import DyObjectConditions


class DynamicObjectInterface(object):
    # __slots__ = ("__triggers__", "__active_triggers__")

    def __init__(self):
        self.__triggers__ = []
        self.__active_triggers__ = Queue()

    @staticmethod
    def _distributeTriggers(dy_object, old_val=None, new_val=None):
        dy_object.__active_triggers__.clear()

        for trigger in dy_object.__triggers__:
            trigger.setValues(old_val, new_val)
            if trigger.thread is None:
                dy_object.__active_triggers__.put_nowait(trigger)
            else:
                if not trigger.isUnique():
                    trigger.thread.addActiveTrigger(trigger)
                else:
                    if not trigger.thread.isTriggerInQueue(trigger):
                        trigger.thread.addActiveTrigger(trigger)

    @staticmethod
    def _runActiveTriggers(dy_object, old_val=None, new_val=None):
        while not dy_object.__active_triggers__.empty():
            trigger = dy_object.__active_triggers__.get_nowait()
            if trigger.exception is not None:
                try:
                    if trigger.runCondition():
                        trigger.runAction()
                    else:
                        trigger.runElseAction()
                except trigger.exception as e:
                    trigger.runCatchAction()
            else:
                if trigger.runCondition():
                    trigger.runAction()
                else:
                    trigger.runElseAction()

    def _prepareAndRunTriggers(self, dy_object, old_val=None, new_val=None):
        self._distributeTriggers(dy_object, old_val, new_val)
        self._runActiveTriggers(dy_object)

    # @abstractmethod
    def __action__(self, *args, **kwargs) -> object:
        pass


class DyObjectMagicMethods:

    def __eq__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            return object.__eq__(self.get(), args[0].get(), **kwargs)
        else:
            return object.__eq__(self.get(), *args, **kwargs)

    def __format__(self, *args, **kwargs):
        return object.__format__(self.get(), *args, **kwargs)

    def __ge__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            return object.__ge__(self.get(), args[0].get(), **kwargs)
        else:
            return object.__ge__(self.get(), *args, **kwargs)

    def __gt__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            return object.__gt__(self.get(), args[0].get(), **kwargs)
        else:
            return object.__gt__(self.get(), *args, **kwargs)

    def __le__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            return object.__le__(self.get(), args[0].get(), **kwargs)
        else:
            return object.__le__(self.get(), *args, **kwargs)

    def __lt__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            return object.__lt__(self.get(), args[0].get(), **kwargs)
        else:
            return object.__lt__(self.get(), *args, **kwargs)

    def __ne__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            return object.__ne__(self.get(), args[0].get(), **kwargs)
        else:
            return object.__ne__(self.get(), *args, **kwargs)

    def __repr__(self, *args, **kwargs):
        return object.__repr__(self.get(), *args, **kwargs)

    def __str__(self, *args, **kwargs):
        return object.__str__(self.get(), *args, **kwargs)


class DyIntMagicMethods(DyObjectMagicMethods):

    def __abs__(self, *args, **kwargs):
        return int.__abs__(self.get(), *args, **kwargs)

    def __add__(self, *args, **kwargs):
        return int.__add__(self.get(), args[0].__int__(), **kwargs)

    def __and__(self, *args, **kwargs):
        return int.__and__(self.get(), args[0].__int__(), **kwargs)

    def __bool__(self, *args, **kwargs):
        return int.__bool__(self.get(), *args, **kwargs)

    def __ceil__(self, *args, **kwargs):
        return int.__ceil__(self.get(), *args, **kwargs)

    def __divmod__(self, *args, **kwargs):
        return int.__divmod__(self.get(), args[0].__int__(), **kwargs)

    def __eq__(self, *args, **kwargs):
        return int.__eq__(self.get(), args[0].__int__(), **kwargs)

    def __float__(self, *args, **kwargs):
        return int.__float__(self.get(), *args, **kwargs)

    def __floordiv__(self, *args, **kwargs):
        return int.__floordiv__(self.get(), args[0].__int__(), **kwargs)

    def __floor__(self, *args, **kwargs):
        return int.__floor__(self.get(), *args, **kwargs)

    def __format__(self, *args, **kwargs):
        return int.__format__(self.get(), *args, **kwargs)

    def __ge__(self, *args, **kwargs):
        return int.__ge__(self.get(), args[0].__int__(), **kwargs)

    def __gt__(self, *args, **kwargs):
        return int.__gt__(self.get(), args[0].__int__(), **kwargs)

    def __index__(self, *args, **kwargs):
        return int.__index__(self.get(), *args, **kwargs)

    def __int__(self, *args, **kwargs):
        return int.__int__(self.get(), *args, **kwargs)

    def __invert__(self, *args, **kwargs):
        return int.__invert__(self.get(), *args, **kwargs)

    def __le__(self, *args, **kwargs):
        return int.__le__(self.get(), args[0].__int__(), **kwargs)

    def __lshift__(self, *args, **kwargs):
        return int.__lshift__(self.get(), args[0].__int__(), **kwargs)

    def __lt__(self, *args, **kwargs):
        return int.__lt__(self.get(), args[0].__int__(), **kwargs)

    def __mod__(self, *args, **kwargs):
        return int.__mod__(self.get(), args[0].__int__(), **kwargs)

    def __mul__(self, *args, **kwargs):
        return int.__mul__(self.get(), args[0].__int__(), **kwargs)

    def __neg__(self, *args, **kwargs):
        return int.__neg__(self.get(), *args, **kwargs)

    def __ne__(self, *args, **kwargs):
        return int.__ne__(self.get(), args[0].__int__(), **kwargs)

    def __or__(self, *args, **kwargs):
        return int.__or__(self.get(), args[0].__int__(), **kwargs)

    def __pos__(self, *args, **kwargs):
        return int.__pos__(self.get(), *args, **kwargs)

    def __pow__(self, *args, **kwargs):
        return int.__pow__(self.get(), args[0].__int__(), **kwargs)

    def __radd__(self, *args, **kwargs):
        return args[0].__int__()

    def __rand__(self, *args, **kwargs):
        return args[0].__int__()

    def __rdivmod__(self, *args, **kwargs):
        return args[0].__int__()

    def __repr__(self, *args, **kwargs):
        return int.__repr__(self.get(), *args, **kwargs)

    def __rfloordiv__(self, *args, **kwargs):
        return args[0].__int__()

    def __rlshift__(self, *args, **kwargs):
        return args[0].__int__()

    def __rmod__(self, *args, **kwargs):
        return args[0].__int__()

    def __rmul__(self, *args, **kwargs):
        return args[0].__int__()

    def __ror__(self, *args, **kwargs):
        return args[0].__int__()

    def __round__(self, *args, **kwargs):
        return int.__round__(self.get(), *args, **kwargs)

    def __rpow__(self, *args, **kwargs):
        return args[0].__int__()

    def __rrshift__(self, *args, **kwargs):
        return args[0].__int__()

    def __rshift__(self, *args, **kwargs):
        return int.__rshift__(self.get(), args[0].__int__(), **kwargs)

    def __rsub__(self, *args, **kwargs):
        return args[0].__int__()

    def __rtruediv__(self, *args, **kwargs):
        return args[0].__int__()

    def __rxor__(self, *args, **kwargs):
        return args[0].__int__()

    def __str__(self, *args, **kwargs):
        return int.__str__(self.get(), *args, **kwargs)

    def __sub__(self, *args, **kwargs):
        return int.__sub__(self.get(), args[0].__int__(), **kwargs)

    def __truediv__(self, *args, **kwargs):
        return int.__truediv__(self.get(), args[0].__int__(), **kwargs)

    def __trunc__(self, *args, **kwargs):
        return int.__trunc__(self.get(), *args, **kwargs)

    def __xor__(self, *args, **kwargs):
        return int.__xor__(self.get(), args[0].__int__(), **kwargs)

    def __iadd__(self, *args, **kwargs):
        self.set(int.__add__(self.get(), args[0].__int__(), **kwargs))
        return self

    def __iand__(self, *args, **kwargs):
        self.set(int.__and__(self.get(), args[0].__int__(), **kwargs))
        return self

    def __ifloordiv__(self, *args, **kwargs):
        self.set(int.__floordiv__(self.get(), args[0].__int__(), **kwargs))
        return self

    def __ilshift__(self, *args, **kwargs):
        self.set(int.__lshift__(self.get(), args[0].__int__(), **kwargs))
        return self

    def __imod__(self, *args, **kwargs):
        self.set(int.__mod__(self.get(), args[0].__int__(), **kwargs))
        return self

    def __imul__(self, *args, **kwargs):
        self.set(int.__mul__(self.get(), args[0].__int__(), **kwargs))
        return self

    def __ior__(self, *args, **kwargs):
        self.set(int.__or__(self.get(), args[0].__int__(), **kwargs))
        return self

    def __ipow__(self, *args, **kwargs):
        self.set(int.__pow__(self.get(), args[0].__int__(), **kwargs))
        return self

    def __irshift__(self, *args, **kwargs):
        self.set(int.__rshift__(self.get(), args[0].__int__(), **kwargs))
        return self

    def __isub__(self, *args, **kwargs):
        self.set(int.__sub__(self.get(), args[0].__int__(), **kwargs))
        return self

    def __itruediv__(self, *args, **kwargs):
        self.set(int.__truediv__(self.get(), args[0].__int__(), **kwargs))
        return self

    def __ixor__(self, *args, **kwargs):
        self.set(int.__xor__(self.get(), args[0].__int__(), **kwargs))
        return self


class DyBoolMagicMethods(DyIntMagicMethods):

    def __and__(self, *args, **kwargs):
        return bool.__and__(self.get(), args[0].__bool__(), **kwargs)

    def __or__(self, *args, **kwargs):
        return bool.__or__(self.get(), args[0].__bool__(), **kwargs)

    def __rand__(self, *args, **kwargs):
        return args[0].__bool__()

    def __repr__(self, *args, **kwargs):
        return bool.__repr__(self.get(), *args, **kwargs)

    def __ror__(self, *args, **kwargs):
        return args[0].__bool__()

    def __rxor__(self, *args, **kwargs):
        return args[0].__bool__()

    def __str__(self, *args, **kwargs):
        return bool.__str__(self.get(), *args, **kwargs)

    def __xor__(self, *args, **kwargs):
        return bool.__xor__(self.get(), args[0].__bool__(), **kwargs)

    def __iand__(self, *args, **kwargs):
        self.set(bool.__and__(self.get(), args[0].__bool__(), **kwargs))
        return self

    def __ior__(self, *args, **kwargs):
        self.set(bool.__or__(self.get(), args[0].__bool__(), **kwargs))
        return self

    def __ixor__(self, *args, **kwargs):
        self.set(bool.__xor__(self.get(), args[0].__bool__(), **kwargs))
        return self


class DyByteArrayMagicMethods(DyObjectMagicMethods):

    def __add__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            return bytearray.__add__(self.get(), args[0].get(), **kwargs)
        else:
            return bytearray.__add__(self.get(), *args, **kwargs)

    def __contains__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            return bytearray.__contains__(self.get(), args[0].get(), **kwargs)
        else:
            return bytearray.__contains__(self.get(), *args, **kwargs)

    def __eq__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            return bytearray.__eq__(self.get(), args[0].get(), **kwargs)
        else:
            return bytearray.__eq__(self.get(), *args, **kwargs)

    def __ge__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            return bytearray.__ge__(self.get(), args[0].get(), **kwargs)
        else:
            return bytearray.__ge__(self.get(), *args, **kwargs)

    def __gt__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            return bytearray.__gt__(self.get(), args[0].get(), **kwargs)
        else:
            return bytearray.__gt__(self.get(), *args, **kwargs)

    def __iadd__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            self.set(bytearray.__add__(self.get(), args[0].get(), **kwargs))
        else:
            self.set(bytearray.__add__(self.get(), *args, **kwargs))
        return self

    def __imul__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            self.set(bytearray.__mul__(self.get(), args[0].get(), **kwargs))
        else:
            self.set(bytearray.__mul__(self.get(), *args, **kwargs))
        return self

    def __iter__(self, *args, **kwargs):
        return bytearray.__iter__(self.get(), *args, **kwargs)

    def __len__(self, *args, **kwargs):
        return bytearray.__len__(self.get(), *args, **kwargs)

    def __le__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            return bytearray.__le__(self.get(), args[0].get(), **kwargs)
        else:
            return bytearray.__le__(self.get(), *args, **kwargs)

    def __lt__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            return bytearray.__lt__(self.get(), args[0].get(), **kwargs)
        else:
            return bytearray.__lt__(self.get(), *args, **kwargs)

    def __mod__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            return bytearray.__mod__(self.get(), args[0].get(), **kwargs)
        else:
            return bytearray.__mod__(self.get(), *args, **kwargs)

    def __mul__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            return bytearray.__mul__(self.get(), args[0].get(), **kwargs)
        else:
            return bytearray.__mul__(self.get(), *args, **kwargs)

    def __ne__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            return bytearray.__ne__(self.get(), args[0].get(), **kwargs)
        else:
            return bytearray.__ne__(self.get(), *args, **kwargs)

    def __repr__(self, *args, **kwargs):
        return bytearray.__repr__(self.get(), *args, **kwargs)

    def __rmod__(self, *args, **kwargs):
        return int(*args, **kwargs)

    def __rmul__(self, *args, **kwargs):
        return int(*args, **kwargs)

    def __str__(self, *args, **kwargs):
        return bytearray.__str__(self.get(), *args, **kwargs)

    def __imod__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            self.set(bytearray.__mod__(self.get(), args[0].get(), **kwargs))
        else:
            self.set(bytearray.__mod__(self.get(), *args, **kwargs))
        return self

    def __radd__(self, *args, **kwargs):
        return int(*args, **kwargs)


class DyBytesMagicMethods(DyObjectMagicMethods):

    def __add__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            return bytes.__add__(self.get(), args[0].get(), **kwargs)
        else:
            return bytes.__add__(self.get(), *args, **kwargs)

    def __contains__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            return bytes.__contains__(self.get(), args[0].get(), **kwargs)
        else:
            return bytes.__contains__(self.get(), *args, **kwargs)

    def __eq__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            return bytes.__eq__(self.get(), args[0].get(), **kwargs)
        else:
            return bytes.__eq__(self.get(), *args, **kwargs)

    def __ge__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            return bytes.__ge__(self.get(), args[0].get(), **kwargs)
        else:
            return bytes.__ge__(self.get(), *args, **kwargs)

    def __gt__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            return bytes.__gt__(self.get(), args[0].get(), **kwargs)
        else:
            return bytes.__gt__(self.get(), *args, **kwargs)

    def __iter__(self, *args, **kwargs):
        return bytes.__iter__(self.get(), *args, **kwargs)

    def __len__(self, *args, **kwargs):
        return bytes.__len__(self.get(), *args, **kwargs)

    def __le__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            return bytes.__le__(self.get(), args[0].get(), **kwargs)
        else:
            return bytes.__le__(self.get(), *args, **kwargs)

    def __lt__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            return bytes.__lt__(self.get(), args[0].get(), **kwargs)
        else:
            return bytes.__lt__(self.get(), *args, **kwargs)

    def __mod__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            return bytes.__mod__(self.get(), args[0].get(), **kwargs)
        else:
            return bytes.__mod__(self.get(), *args, **kwargs)

    def __mul__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            return bytes.__mul__(self.get(), args[0].get(), **kwargs)
        else:
            return bytes.__mul__(self.get(), *args, **kwargs)

    def __ne__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            return bytes.__ne__(self.get(), args[0].get(), **kwargs)
        else:
            return bytes.__ne__(self.get(), *args, **kwargs)

    def __repr__(self, *args, **kwargs):
        return bytes.__repr__(self.get(), *args, **kwargs)

    def __rmod__(self, *args, **kwargs):
        return int(*args, **kwargs)

    def __rmul__(self, *args, **kwargs):
        return int(*args, **kwargs)

    def __str__(self, *args, **kwargs):
        return bytes.__str__(self.get(), *args, **kwargs)

    def __iadd__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            self.set(bytes.__add__(self.get(), args[0].get(), **kwargs))
        else:
            self.set(bytes.__add__(self.get(), *args, **kwargs))
        return self

    def __imod__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            self.set(bytes.__mod__(self.get(), args[0].get(), **kwargs))
        else:
            self.set(bytes.__mod__(self.get(), *args, **kwargs))
        return self

    def __imul__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            self.set(bytes.__mul__(self.get(), args[0].get(), **kwargs))
        else:
            self.set(bytes.__mul__(self.get(), *args, **kwargs))
        return self

    def __radd__(self, *args, **kwargs):
        return int(*args, **kwargs)


class DyComplexMagicMethods(DyObjectMagicMethods):

    def __abs__(self, *args, **kwargs):
        return complex.__abs__(self.get(), *args, **kwargs)

    def __add__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            return complex.__add__(self.get(), args[0].get(), **kwargs)
        else:
            return complex.__add__(self.get(), *args, **kwargs)

    def __bool__(self, *args, **kwargs):
        return complex.__bool__(self.get(), *args, **kwargs)

    def __divmod__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            return complex.__divmod__(self.get(), args[0].get(), **kwargs)
        else:
            return complex.__divmod__(self.get(), *args, **kwargs)

    def __eq__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            return complex.__eq__(self.get(), args[0].get(), **kwargs)
        else:
            return complex.__eq__(self.get(), *args, **kwargs)

    def __float__(self, *args, **kwargs):
        return complex.__float__(self.get(), *args, **kwargs)

    def __floordiv__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            return complex.__floordiv__(self.get(), args[0].get(), **kwargs)
        else:
            return complex.__floordiv__(self.get(), *args, **kwargs)

    def __format__(self, *args, **kwargs):
        return complex.__format__(self.get(), *args, **kwargs)

    def __ge__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            return complex.__ge__(self.get(), args[0].get(), **kwargs)
        else:
            return complex.__ge__(self.get(), *args, **kwargs)

    def __gt__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            return complex.__gt__(self.get(), args[0].get(), **kwargs)
        else:
            return complex.__gt__(self.get(), *args, **kwargs)

    def __int__(self, *args, **kwargs):
        return complex.__int__(self.get(), *args, **kwargs)

    def __le__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            return complex.__le__(self.get(), args[0].get(), **kwargs)
        else:
            return complex.__le__(self.get(), *args, **kwargs)

    def __lt__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            return complex.__lt__(self.get(), args[0].get(), **kwargs)
        else:
            return complex.__lt__(self.get(), *args, **kwargs)

    def __mod__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            return complex.__mod__(self.get(), args[0].get(), **kwargs)
        else:
            return complex.__mod__(self.get(), *args, **kwargs)

    def __mul__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            return complex.__mul__(self.get(), args[0].get(), **kwargs)
        else:
            return complex.__mul__(self.get(), *args, **kwargs)

    def __neg__(self, *args, **kwargs):
        return complex.__neg__(self.get(), *args, **kwargs)

    def __ne__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            return complex.__ne__(self.get(), args[0].get(), **kwargs)
        else:
            return complex.__ne__(self.get(), *args, **kwargs)

    def __pos__(self, *args, **kwargs):
        return complex.__pos__(self.get(), *args, **kwargs)

    def __pow__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            return complex.__pow__(self.get(), args[0].get(), **kwargs)
        else:
            return complex.__pow__(self.get(), *args, **kwargs)

    def __radd__(self, *args, **kwargs):
        return int(*args, **kwargs)

    def __rdivmod__(self, *args, **kwargs):
        return int(*args, **kwargs)

    def __repr__(self, *args, **kwargs):
        return complex.__repr__(self.get(), *args, **kwargs)

    def __rfloordiv__(self, *args, **kwargs):
        return int(*args, **kwargs)

    def __rmod__(self, *args, **kwargs):
        return int(*args, **kwargs)

    def __rmul__(self, *args, **kwargs):
        return int(*args, **kwargs)

    def __rpow__(self, *args, **kwargs):
        return int(*args, **kwargs)

    def __rsub__(self, *args, **kwargs):
        return int(*args, **kwargs)

    def __rtruediv__(self, *args, **kwargs):
        return int(*args, **kwargs)

    def __str__(self, *args, **kwargs):
        return complex.__str__(self.get(), *args, **kwargs)

    def __sub__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            return complex.__sub__(self.get(), args[0].get(), **kwargs)
        else:
            return complex.__sub__(self.get(), *args, **kwargs)

    def __truediv__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            return complex.__truediv__(self.get(), args[0].get(), **kwargs)
        else:
            return complex.__truediv__(self.get(), *args, **kwargs)

    def __iadd__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            self.set(complex.__add__(self.get(), args[0].get(), **kwargs))
        else:
            self.set(complex.__add__(self.get(), *args, **kwargs))
        return self

    def __ifloordiv__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            self.set(complex.__floordiv__(self.get(), args[0].get(), **kwargs))
        else:
            self.set(complex.__floordiv__(self.get(), *args, **kwargs))
        return self

    def __imod__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            self.set(complex.__mod__(self.get(), args[0].get(), **kwargs))
        else:
            self.set(complex.__mod__(self.get(), *args, **kwargs))
        return self

    def __imul__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            self.set(complex.__mul__(self.get(), args[0].get(), **kwargs))
        else:
            self.set(complex.__mul__(self.get(), *args, **kwargs))
        return self

    def __ipow__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            self.set(complex.__pow__(self.get(), args[0].get(), **kwargs))
        else:
            self.set(complex.__pow__(self.get(), *args, **kwargs))
        return self

    def __isub__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            self.set(complex.__sub__(self.get(), args[0].get(), **kwargs))
        else:
            self.set(complex.__sub__(self.get(), *args, **kwargs))
        return self

    def __itruediv__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            self.set(complex.__truediv__(self.get(), args[0].get(), **kwargs))
        else:
            self.set(complex.__truediv__(self.get(), *args, **kwargs))
        return self


class DyDictMagicMethods(DyObjectMagicMethods):

    def __contains__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            return dict.__contains__(self.get(), args[0].get(), **kwargs)
        else:
            return dict.__contains__(self.get(), *args, **kwargs)

    def __eq__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            return dict.__eq__(self.get(), args[0].get(), **kwargs)
        else:
            return dict.__eq__(self.get(), *args, **kwargs)

    def __ge__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            return dict.__ge__(self.get(), args[0].get(), **kwargs)
        else:
            return dict.__ge__(self.get(), *args, **kwargs)

    def __gt__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            return dict.__gt__(self.get(), args[0].get(), **kwargs)
        else:
            return dict.__gt__(self.get(), *args, **kwargs)

    def __iter__(self, *args, **kwargs):
        return dict.__iter__(self.get(), *args, **kwargs)

    def __len__(self, *args, **kwargs):
        return dict.__len__(self.get(), *args, **kwargs)

    def __le__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            return dict.__le__(self.get(), args[0].get(), **kwargs)
        else:
            return dict.__le__(self.get(), *args, **kwargs)

    def __lt__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            return dict.__lt__(self.get(), args[0].get(), **kwargs)
        else:
            return dict.__lt__(self.get(), *args, **kwargs)

    def __ne__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            return dict.__ne__(self.get(), args[0].get(), **kwargs)
        else:
            return dict.__ne__(self.get(), *args, **kwargs)

    def __repr__(self, *args, **kwargs):
        return dict.__repr__(self.get(), *args, **kwargs)


class DyFloatMagicMethods(DyObjectMagicMethods):

    def __abs__(self, *args, **kwargs):
        return float.__abs__(self.get(), *args, **kwargs)

    def __add__(self, *args, **kwargs):
        return float.__add__(self.get(), args[0].__float__(), **kwargs)

    def __bool__(self, *args, **kwargs):
        return float.__bool__(self.get(), *args, **kwargs)

    def __divmod__(self, *args, **kwargs):
        return float.__divmod__(self.get(), args[0].__float__(), **kwargs)

    def __eq__(self, *args, **kwargs):
        return float.__eq__(self.get(), args[0].__float__(), **kwargs)

    def __float__(self, *args, **kwargs):
        return float.__float__(self.get(), *args, **kwargs)

    def __floordiv__(self, *args, **kwargs):
        return float.__floordiv__(self.get(), args[0].__float__(), **kwargs)

    def __format__(self, *args, **kwargs):
        return float.__format__(self.get(), *args, **kwargs)

    def __ge__(self, *args, **kwargs):
        return float.__ge__(self.get(), args[0].__float__(), **kwargs)

    def __gt__(self, *args, **kwargs):
        return float.__gt__(self.get(), args[0].__float__(), **kwargs)

    def __int__(self, *args, **kwargs):
        return float.__int__(self.get(), *args, **kwargs)

    def __le__(self, *args, **kwargs):
        return float.__le__(self.get(), args[0].__float__(), **kwargs)

    def __lt__(self, *args, **kwargs):
        return float.__lt__(self.get(), args[0].__float__(), **kwargs)

    def __mod__(self, *args, **kwargs):
        return float.__mod__(self.get(), args[0].__float__(), **kwargs)

    def __mul__(self, *args, **kwargs):
        return float.__mul__(self.get(), args[0].__float__(), **kwargs)

    def __neg__(self, *args, **kwargs):
        return float.__neg__(self.get(), *args, **kwargs)

    def __ne__(self, *args, **kwargs):
        return float.__ne__(self.get(), args[0].__float__(), **kwargs)

    def __pos__(self, *args, **kwargs):
        return float.__pos__(self.get(), *args, **kwargs)

    def __pow__(self, *args, **kwargs):
        return float.__pow__(self.get(), args[0].__float__(), **kwargs)

    def __radd__(self, *args, **kwargs):
        return args[0].__float__()

    def __rdivmod__(self, *args, **kwargs):
        return args[0].__float__()

    def __repr__(self, *args, **kwargs):
        return float.__repr__(self.get(), *args, **kwargs)

    def __rfloordiv__(self, *args, **kwargs):
        return args[0].__float__()

    def __rmod__(self, *args, **kwargs):
        return args[0].__float__()

    def __rmul__(self, *args, **kwargs):
        return args[0].__float__()

    def __round__(self, *args, **kwargs):
        return float.__round__(self.get(), *args, **kwargs)

    def __rpow__(self, *args, **kwargs):
        return args[0].__float__()

    def __rsub__(self, *args, **kwargs):
        return args[0].__float__()

    def __rtruediv__(self, *args, **kwargs):
        return args[0].__float__()

    def __str__(self, *args, **kwargs):
        return float.__str__(self.get(), *args, **kwargs)

    def __sub__(self, *args, **kwargs):
        return float.__sub__(self.get(), args[0].__float__(), **kwargs)

    def __truediv__(self, *args, **kwargs):
        return float.__truediv__(float(self.get()), args[0].__float__(), **kwargs)

    def __trunc__(self, *args, **kwargs):
        return float.__trunc__(self.get(), *args, **kwargs)

    def __iadd__(self, *args, **kwargs):
        self.set(float.__add__(self.get(), args[0].__float__(), **kwargs))
        return self

    def __ifloordiv__(self, *args, **kwargs):
        self.set(float.__floordiv__(self.get(), args[0].__float__(), **kwargs))
        return self

    def __imod__(self, *args, **kwargs):
        self.set(float.__mod__(self.get(), args[0].__float__(), **kwargs))
        return self

    def __imul__(self, *args, **kwargs):
        self.set(float.__mul__(self.get(), args[0].__float__(), **kwargs))
        return self

    def __ipow__(self, *args, **kwargs):
        self.set(float.__pow__(self.get(), args[0].__float__(), **kwargs))
        return self

    def __isub__(self, *args, **kwargs):
        self.set(float.__sub__(self.get(), args[0].__float__(), **kwargs))
        return self

    def __itruediv__(self, *args, **kwargs):
        self.set(float.__truediv__(self.get(), args[0].__float__(), **kwargs))
        return self


class DyListMagicMethods(DyObjectMagicMethods):

    def __add__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            return list.__add__(self.get(), args[0].get(), **kwargs)
        else:
            return list.__add__(self.get(), *args, **kwargs)

    def __contains__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            return list.__contains__(self.get(), args[0].get(), **kwargs)
        else:
            return list.__contains__(self.get(), *args, **kwargs)

    def __eq__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            return list.__eq__(self.get(), args[0].get(), **kwargs)
        else:
            return list.__eq__(self.get(), *args, **kwargs)

    def __ge__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            return list.__ge__(self.get(), args[0].get(), **kwargs)
        else:
            return list.__ge__(self.get(), *args, **kwargs)

    def __gt__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            return list.__gt__(self.get(), args[0].get(), **kwargs)
        else:
            return list.__gt__(self.get(), *args, **kwargs)

    def __iadd__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            self.set(list.__add__(self.get(), args[0].get(), **kwargs))
        else:
            self.set(list.__add__(self.get(), *args, **kwargs))
        return self

    def __imul__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            self.set(list.__mul__(self.get(), args[0].get(), **kwargs))
        else:
            self.set(list.__mul__(self.get(), *args, **kwargs))
        return self

    def __iter__(self, *args, **kwargs):
        return list.__iter__(self.get(), *args, **kwargs)

    def __len__(self, *args, **kwargs):
        return list.__len__(self.get(), *args, **kwargs)

    def __le__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            return list.__le__(self.get(), args[0].get(), **kwargs)
        else:
            return list.__le__(self.get(), *args, **kwargs)

    def __lt__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            return list.__lt__(self.get(), args[0].get(), **kwargs)
        else:
            return list.__lt__(self.get(), *args, **kwargs)

    def __mul__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            return list.__mul__(self.get(), args[0].get(), **kwargs)
        else:
            return list.__mul__(self.get(), *args, **kwargs)

    def __ne__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            return list.__ne__(self.get(), args[0].get(), **kwargs)
        else:
            return list.__ne__(self.get(), *args, **kwargs)

    def __repr__(self, *args, **kwargs):
        return list.__repr__(self.get(), *args, **kwargs)

    def __reversed__(self, *args, **kwargs):
        return list.__reversed__(self.get(), *args, **kwargs)

    def __rmul__(self, *args, **kwargs):
        return int(*args, **kwargs)

    def __radd__(self, *args, **kwargs):
        return int(*args, **kwargs)


class DySetMagicMethods(DyObjectMagicMethods):

    def __and__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            return set.__and__(self.get(), args[0].get(), **kwargs)
        else:
            return set.__and__(self.get(), *args, **kwargs)

    def __contains__(self, y):
        if isinstance(y, DyObject):
            return set.__contains__(self.get(), y.get())
        else:
            return set.__contains__(self.get(), y)

    def __eq__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            return set.__eq__(self.get(), args[0].get(), **kwargs)
        else:
            return set.__eq__(self.get(), *args, **kwargs)

    def __ge__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            return set.__ge__(self.get(), args[0].get(), **kwargs)
        else:
            return set.__ge__(self.get(), *args, **kwargs)

    def __gt__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            return set.__gt__(self.get(), args[0].get(), **kwargs)
        else:
            return set.__gt__(self.get(), *args, **kwargs)

    def __iand__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            self.set(set.__and__(self.get(), args[0].get(), **kwargs))
        else:
            self.set(set.__and__(self.get(), *args, **kwargs))
        return self

    def __ior__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            self.set(set.__or__(self.get(), args[0].get(), **kwargs))
        else:
            self.set(set.__or__(self.get(), *args, **kwargs))
        return self

    def __isub__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            self.set(set.__sub__(self.get(), args[0].get(), **kwargs))
        else:
            self.set(set.__sub__(self.get(), *args, **kwargs))
        return self

    def __iter__(self, *args, **kwargs):
        return set.__iter__(self.get(), *args, **kwargs)

    def __ixor__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            self.set(set.__xor__(self.get(), args[0].get(), **kwargs))
        else:
            self.set(set.__xor__(self.get(), *args, **kwargs))
        return self

    def __len__(self, *args, **kwargs):
        return set.__len__(self.get(), *args, **kwargs)

    def __le__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            return set.__le__(self.get(), args[0].get(), **kwargs)
        else:
            return set.__le__(self.get(), *args, **kwargs)

    def __lt__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            return set.__lt__(self.get(), args[0].get(), **kwargs)
        else:
            return set.__lt__(self.get(), *args, **kwargs)

    def __ne__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            return set.__ne__(self.get(), args[0].get(), **kwargs)
        else:
            return set.__ne__(self.get(), *args, **kwargs)

    def __or__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            return set.__or__(self.get(), args[0].get(), **kwargs)
        else:
            return set.__or__(self.get(), *args, **kwargs)

    def __rand__(self, *args, **kwargs):
        return int(*args, **kwargs)

    def __repr__(self, *args, **kwargs):
        return set.__repr__(self.get(), *args, **kwargs)

    def __ror__(self, *args, **kwargs):
        return int(*args, **kwargs)

    def __rsub__(self, *args, **kwargs):
        return int(*args, **kwargs)

    def __rxor__(self, *args, **kwargs):
        return int(*args, **kwargs)

    def __sub__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            return set.__sub__(self.get(), args[0].get(), **kwargs)
        else:
            return set.__sub__(self.get(), *args, **kwargs)

    def __xor__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            return set.__xor__(self.get(), args[0].get(), **kwargs)
        else:
            return set.__xor__(self.get(), *args, **kwargs)


class DyStrMagicMethods(DyObjectMagicMethods):

    def __add__(self, *args, **kwargs):
        return str.__add__(self.get(), args[0].__str__(), **kwargs)

    def __contains__(self, *args, **kwargs):
        return str.__contains__(self.get(), args[0].__str__(), **kwargs)

    def __eq__(self, *args, **kwargs):
        return str.__eq__(self.get(), args[0].__str__(), **kwargs)

    def __format__(self, *args, **kwargs):
        return str.__format__(self.get(), *args, **kwargs)

    def __ge__(self, *args, **kwargs):
        return str.__ge__(self.get(), args[0].__str__(), **kwargs)

    def __gt__(self, *args, **kwargs):
        return str.__gt__(self.get(), args[0].__str__(), **kwargs)

    def __iter__(self, *args, **kwargs):
        return str.__iter__(self.get(), *args, **kwargs)

    def __len__(self, *args, **kwargs):
        return str.__len__(self.get(), *args, **kwargs)

    def __le__(self, *args, **kwargs):
        return str.__le__(self.get(), args[0].__str__(), **kwargs)

    def __lt__(self, *args, **kwargs):
        return str.__lt__(self.get(), args[0].__str__(), **kwargs)

    def __mod__(self, *args, **kwargs):
        return str.__mod__(self.get(), args[0].__str__(), **kwargs)

    def __mul__(self, *args, **kwargs):
        return str.__mul__(self.get(), args[0].__str__(), **kwargs)

    def __ne__(self, *args, **kwargs):
        return str.__ne__(self.get(), args[0].__str__(), **kwargs)

    def __repr__(self, *args, **kwargs):
        return str.__repr__(self.get(), *args, **kwargs)

    def __rmod__(self, *args, **kwargs):
        return args[0].__str__()

    def __rmul__(self, *args, **kwargs):
        return args[0].__str__()

    def __str__(self, *args, **kwargs):
        return str.__str__(self.get(), *args, **kwargs)

    def __iadd__(self, *args, **kwargs):
        self.set(str.__add__(self.get(), args[0].__str__(), **kwargs))
        return self

    def __imod__(self, *args, **kwargs):
        self.set(str.__mod__(self.get(), args[0].__str__(), **kwargs))
        return self

    def __imul__(self, *args, **kwargs):
        self.set(str.__mul__(self.get(), args[0].__str__(), **kwargs))
        return self

    def __radd__(self, *args, **kwargs):
        return args[0].__str__()


class DyTupleMagicMethods(DyObjectMagicMethods):

    def __add__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            return tuple.__add__(self.get(), args[0].get(), **kwargs)
        else:
            return tuple.__add__(self.get(), *args, **kwargs)

    def __contains__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            return tuple.__contains__(self.get(), args[0].get(), **kwargs)
        else:
            return tuple.__contains__(self.get(), *args, **kwargs)

    def __eq__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            return tuple.__eq__(self.get(), args[0].get(), **kwargs)
        else:
            return tuple.__eq__(self.get(), *args, **kwargs)

    def __ge__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            return tuple.__ge__(self.get(), args[0].get(), **kwargs)
        else:
            return tuple.__ge__(self.get(), *args, **kwargs)

    def __gt__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            return tuple.__gt__(self.get(), args[0].get(), **kwargs)
        else:
            return tuple.__gt__(self.get(), *args, **kwargs)

    def __iter__(self, *args, **kwargs):
        return tuple.__iter__(self.get(), *args, **kwargs)

    def __len__(self, *args, **kwargs):
        return tuple.__len__(self.get(), *args, **kwargs)

    def __le__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            return tuple.__le__(self.get(), args[0].get(), **kwargs)
        else:
            return tuple.__le__(self.get(), *args, **kwargs)

    def __lt__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            return tuple.__lt__(self.get(), args[0].get(), **kwargs)
        else:
            return tuple.__lt__(self.get(), *args, **kwargs)

    def __mul__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            return tuple.__mul__(self.get(), args[0].get(), **kwargs)
        else:
            return tuple.__mul__(self.get(), *args, **kwargs)

    def __ne__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            return tuple.__ne__(self.get(), args[0].get(), **kwargs)
        else:
            return tuple.__ne__(self.get(), *args, **kwargs)

    def __repr__(self, *args, **kwargs):
        return tuple.__repr__(self.get(), *args, **kwargs)

    def __rmul__(self, *args, **kwargs):
        return int(*args, **kwargs)

    def __iadd__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            self.set(tuple.__add__(self.get(), args[0].get(), **kwargs))
        else:
            self.set(tuple.__add__(self.get(), *args, **kwargs))
        return self

    def __imul__(self, *args, **kwargs):
        if isinstance(args[0], DyObject):
            self.set(tuple.__mul__(self.get(), args[0].get(), **kwargs))
        else:
            self.set(tuple.__mul__(self.get(), *args, **kwargs))
        return self

    def __radd__(self, *args, **kwargs):
        return int(*args, **kwargs)


class DyObject(DyObjectMagicMethods, DyObjectConditions, DynamicObjectInterface):

    type = "DynamicObject"

    def __init__(self, value=None, builtin=False):
        super(DyObject, self).__init__()
        self.__value__: object = value
        self.__name__: str = "__name__"
        self._is_builtin: bool = builtin

    def _set_empty(self, value):
        old_val = self._get()
        self.__log_p__(f"{self.__name__} = {value}: {current_thread().name}")
        self._prepareAndRunTriggers(self, old_val, value)

    def _set(self, value):
        self.__value__ = value

    def set(self, value):
        old_val = self._get()
        self._set(value)
        self.__log_p__(f"{self.__name__} = {value}: {current_thread().name}")
        self._prepareAndRunTriggers(self, old_val, value)

    def _get(self):
        return self.__value__

    def get(self):
        return self._get()

    def setBuiltin(self, ans):
        self._is_builtin = ans

    # def __repr__(self):
    #     return self.get()

    @staticmethod
    def __get_other__(other):
        if isinstance(other, DyObject):
            return other.get()
        return other

    def __log_p__(self, message):
        if not (self._is_builtin and not Log.BUILTIN_ENABLED):
            Log.p(message, Log.color.BLUE)

    def __action__(self, *args, **kwargs):
        return self.set(args[0])
