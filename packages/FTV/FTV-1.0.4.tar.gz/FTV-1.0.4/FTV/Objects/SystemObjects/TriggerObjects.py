from abc import abstractmethod


class Condition(object):
    @staticmethod
    @abstractmethod
    def __condition__(old_val, new_val, *args, **kwargs):
        return True


class Trigger:
    __slots__ = ("dy_module_parent",
                 "condition",
                 "condition_args",
                 "condition_kwargs",
                 "exception",
                 "exception_args",
                 "exception_kwargs",
                 "old_val",
                 "new_val",
                 "action",
                 "action_name",
                 "action_args",
                 "action_kwargs",
                 "else_action",
                 "else_action_name",
                 "else_action_args",
                 "else_action_kwargs",
                 "catch_action",
                 "catch_action_name",
                 "catch_action_args",
                 "catch_action_kwargs",
                 "thread",
                 "unique")

    def __init__(self, dy_module_parent):
        self.dy_module_parent = dy_module_parent

        self.condition: function = None
        self.condition_args = []
        self.condition_kwargs = dict()

        self.exception: Exception = None
        self.exception_args = []
        self.exception_kwargs = dict()

        self.old_val = None
        self.new_val = None

        self.action: function = self.__empty_action
        self.action_name = None
        self.action_args = []
        self.action_kwargs = dict()

        self.else_action: function = self.__empty_action
        self.else_action_name = None
        self.else_action_args = []
        self.else_action_kwargs = dict()

        self.catch_action: function = self.__empty_action
        self.catch_action_name = None
        self.catch_action_args = []
        self.catch_action_kwargs = dict()

        self.thread: object = None

        self.unique: bool = False

    def setUnique(self, val=True):
        self.unique = val
        return self

    def isUnique(self):
        return self.unique

    def setCondition(self, condition, *args, **kwargs):
        self.condition = condition.__condition__
        self.condition_args = args
        self.condition_kwargs = kwargs
        return self

    def setException(self, exception, *args, **kwargs):
        self.exception = exception
        self.exception_args = args
        self.exception_kwargs = kwargs
        return self

    def setAction(self, action, *args, **kwargs):
        if callable(action):
            modified_action = self.__getParent(**kwargs).__get_by_method__(action)
            self.action_name = action.__name__
        else:
            modified_action = action

        self.action = modified_action.__action__
        self.action_args = args
        self.action_kwargs = kwargs
        return self

    def elseAction(self, action, *args, **kwargs):
        if callable(action):
            modified_action = self.__getParent(**kwargs).__get_by_method__(action)
            self.else_action_name = action.__name__
        else:
            modified_action = action

        self.else_action = modified_action.__action__
        self.else_action_args = args
        self.else_action_kwargs = kwargs
        return self

    def catchAction(self, action, *args, **kwargs):
        if callable(action):
            modified_action = self.__getParent(**kwargs).__get_by_method__(action)
            self.catch_action_name = action.__name__
        else:
            modified_action = action

        if self.exception is None:
            self.exception = Exception

        self.catch_action = modified_action.__action__
        self.catch_action_args = args
        self.catch_action_kwargs = kwargs
        return self

    def setThread(self, thread):
        self.thread = thread
        return self

    def setValues(self, old_val=None, new_val=None):
        self.old_val = old_val
        self.new_val = new_val

    def runCondition(self):
        return self.__condition__(self.old_val, self.new_val, *self.condition_args, **self.condition_kwargs)

    def runAction(self):
        return self.__action__(*self.action_args, **self.action_kwargs)

    def runElseAction(self):
        return self.__else_action__(*self.else_action_args, **self.else_action_kwargs)

    def runCatchAction(self):
        return self.__catch_action__(*self.catch_action_args, **self.catch_action_kwargs)

    def getException(self):
        return self.exception

    def __getParent(self, **kwargs):
        parent = None
        if "parent" in kwargs:
            parent = kwargs["parent"]
        if parent is None:
            parent = self.dy_module_parent
        return parent

    def __condition__(self, old_val, new_val, *args, **kwargs):
        return self.condition(old_val, new_val, *args, **kwargs)

    def __action__(self, *args, **kwargs):
        return self.action(*args, **kwargs)

    def __else_action__(self, *args, **kwargs):
        return self.else_action(*args, **kwargs)

    def __catch_action__(self, *args, **kwargs):
        return self.catch_action(*args, **kwargs)

    def __empty_action(self, *args, **kwargs):
        pass
