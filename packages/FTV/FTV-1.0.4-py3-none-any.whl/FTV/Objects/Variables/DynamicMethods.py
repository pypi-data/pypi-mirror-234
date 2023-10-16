from threading import current_thread

import wrapt

from FTV.Managers.Log import Log
from FTV.Objects.Variables.AbstractDynamicObject import DynamicObjectInterface


# class DyProxy(wrapt.ObjectProxy):
#     def __init__(self, object_to_wrap, *args):
#         super().__init__(object_to_wrap)
#         self._args = args
#
#     @property
#     def args(self):
#         return self._args
#
#     def __reduce_ex__(self, protocol):
#         return type(self), (self.__wrapped__, self.args)


class DyMethod(DynamicObjectInterface):
    def __init__(self):
        super(DyMethod, self).__init__()
    #
    # def __copy__(self):
    #     pass
    #
    # def __deepcopy__(self, memo):
    #     pass
    #
    # def __reduce__(self):
    #     pass

    # __slots__ = ()

    # def __init__(self):
    #     super(DyMethod, self).__init__()

    @wrapt.decorator
    def __call__(self, wrapped, instance, args, kwargs):
        if "parent" in kwargs:
            del kwargs["parent"]
        
        # self.__log_p__(f"-> {wrapped.__name__}")
        self.__log_p__(f"-> {instance.__class__.__name__}.{wrapped.__name__}: {current_thread().name}")
        self.__log_step__(1)
        # instance._ACTIVE_METHOD = wrapped.__name__
        ans = wrapped(*args, **kwargs)
        # instance._ACTIVE_METHOD = ""
        self.__log_step__(-1)
        # self.__log_p__(f"<- {wrapped.__name__}")
        self.__log_p__(f"<- {instance.__class__.__name__}.{wrapped.__name__}")
        self._prepareAndRunTriggers(instance.__get_by_method__(wrapped))
        return ans

    @staticmethod
    def __log_p__(message):
        Log.p(message, Log.color.ORANGE)

    @staticmethod
    def __log_step__(step):
        Log.step(step)


class DyBuiltinMethod(DyMethod):

    @staticmethod
    def __log_p__(message):
        if Log.BUILTIN_ENABLED:
            DyMethod.__log_p__(message)

    @staticmethod
    def __log_step__(step):
        if Log.BUILTIN_ENABLED:
            DyMethod.__log_step__(step)


@wrapt.decorator
def dyMethod(wrapped, instance, args, kwargs):
    # DyMethod.__log_p__("->"" {}".format(wrapped.__name__))
    # DyMethod.__log_step__(1)
    # # instance._ACTIVE_METHOD = wrapped.__name__
    ans = wrapped(*args, **kwargs)
    # # instance._ACTIVE_METHOD = ""
    # DyMethod.__log_step__(-1)
    # DyMethod.__log_p__("<-"" {}".format(wrapped.__name__))
    DynamicObjectInterface._prepareAndRunTriggers(instance, instance.__get_by_method__(wrapped))
    return ans
