import inspect


class DynamicModuleParent(object):
    __BUILTIN_METHODS = (
        "__setattr__",
        "__init__",
        "addTrigger",
        "addTriggers",
        "_DynamicModuleParent__initMethodsVariables",
        "_DynamicModuleParent__setMethodTriggers"
    )

    def __setattr__(self, key, value):
        if key in dir(self) and callable(getattr(self, key)):
            raise Exception(
                "Can't addFeatures the attribute \"{}\" to the object \"{}\", since it is already exists as a method.".format(
                    key, self.__class__.__name__))
        else:
            super().__setattr__(key, value)

    def __init__(self):
        self._setupMethods()
        self.addTriggers()

    def addTrigger(self, method, trigger):
        method.__triggers__.append(trigger)

    def addTriggers(self):
        pass

    def _setupMethods(self):
        for func in inspect.getmembers(self, inspect.ismethod):
            method_key = func[0]
            if method_key not in getattr(self, "_DynamicModuleParent__BUILTIN_METHODS"):
                self.__setMethodTriggers(method_key, [])

    def __setMethodTriggers(self, method_key, triggers):
        setattr(getattr(self.__class__, method_key), "__triggers__", triggers)


class Feature1(DynamicModuleParent):

    def action(self):
        self.do()

    def do(self):
        print("do()")

    def addTriggers(self):
        self.addTrigger(self.action, "a")
        self.addTrigger(self.action, "b")
        self.addTrigger(self.action, "c")
        self.addTrigger(self.do, "c")


feature = Feature1()

print(feature.action.__triggers__)
print(feature.do.__triggers__)
feature.action()
