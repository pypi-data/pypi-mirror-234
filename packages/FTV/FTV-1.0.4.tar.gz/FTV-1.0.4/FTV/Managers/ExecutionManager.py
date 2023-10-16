import threading

from FTV.Managers.AbstractManager import AbstractManager
from FTV.Objects.SystemObjects.Executions import DyThread, DyThreadList, DyExecution
from FTV.Objects.Variables.DynamicIterators import DyBoolList
from FTV.Objects.Variables.DynamicMethods import DyBuiltinMethod
from FTV.Objects.Variables.DynamicObjects import DySwitch


class ExecutionManager(AbstractManager):
    __short_name__ = "EM"

    def __init__(self, _is_parent_app=False):
        super().__init__(_is_parent_app=_is_parent_app)
        self.init()

    def __setattr__(self, key, value):
        if isinstance(value, DyExecution):
            value(key)
            if not self._isThreadExist(key):
                super(ExecutionManager, self).__setattr__(key, value)
                self._addThread(value)
            else:
                Exception("There is already a thread called \"{}\".".format(key))
        else:
            super(ExecutionManager, self).__setattr__(key, value)

    def init(self):
        pass

    def _setupMethodsLists(self):
        super(ExecutionManager, self)._setupMethodsLists()
        self._BUILTIN_METHODS |= {"_stopAllThreads"}

    @DyBuiltinMethod()
    def _loadBuiltinSelf(self):
        self._setupBuiltinVariables()
        self._setupBuiltinThreads()
        self._setupBuiltinMethods()
        self._setupBuiltinTriggers()

    @DyBuiltinMethod()
    def _loadSelf(self):
        self.setupVariables()
        self.setupThreads()
        self._setupMethods()
        self.setupTriggers()

    def _setupBuiltinVariables(self):
        super(ExecutionManager, self)._setupBuiltinVariables()
        self.STOP_THREADS = DySwitch(builtin=True)

    def _setupBuiltinTriggers(self):
        super(ExecutionManager, self)._setupBuiltinTriggers()
        self.addTrigger(self.areQueuesEmpty)\
            .setCondition(DyBoolList.IsChangedTo, True)\
            .setAction(self.STOP_THREADS)\
            # .setThread(self.getThread("Main"))
        self.addTrigger(self.STOP_THREADS).setAction(self._stopAllThreads)

    def _setupBuiltinThreads(self):
        self.areQueuesEmpty = DyBoolList(builtin=True)

        self.threads = {}

        if self._is_parent_app:
            self.Main = DyThread()

    def setupVariables(self):
        pass

    def setupThreads(self):
        pass

    def _addThread(self, thread: DyThread):
        self.threads[thread.__name__] = thread
        self.areQueuesEmpty.add(self.threads[thread.__name__].isQueueEmpty)

    def _isThreadExist(self, name):
        return name in self.threads

    def getThread(self, name):
        return self.threads[name]

    def getCurrentThread(self):
        return self.threads[threading.currentThread().name]

    def setupSettings(self):
        pass

    @DyBuiltinMethod()
    def _stopAllThreads(self):
        for thread in self.threads.values():
            if isinstance(thread, DyThreadList):
                thread.stop()
            else:
                if not thread.daemon:
                    thread.stop()
