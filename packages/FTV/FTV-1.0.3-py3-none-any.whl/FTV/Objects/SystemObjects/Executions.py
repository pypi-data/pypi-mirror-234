import time
from threading import Thread as BaseThread

from FTV.Objects.SystemObjects.DataObject import Queue
from FTV.Objects.Variables.DynamicIterators import DyBoolList
from FTV.Objects.Variables.DynamicModules import DyBuiltinModule
from FTV.Objects.Variables.DynamicObjects import DyBool


class DyExecution(DyBuiltinModule):
    def runActiveTrigger(self, trigger):
        trigger.runAction()

    def runElseActiveTrigger(self, trigger):
        trigger.runElseAction()

    def runCondition(self, trigger):
        return trigger.runCondition()


class DyProcess(DyExecution):
    pass


class DyProcessList(DyExecution):
    pass


class DyThread(DyExecution):
    def __init__(self, daemon=False):
        self.daemon = daemon

    def __call__(self, name=None, daemon=False):
        # Log.p(f"DyThread.__init__({name})")
        self.name = name
        self.daemon = daemon
        super(DyExecution, self).__init__()

    def setupVariables(self):
        self.isQueueEmpty = DyBool(True, builtin=True)
        self.__active_triggers__ = Queue()
        self.thread = BaseThread(target=self.thread_loop, daemon=self.daemon)

        if self.name is not None:
            self.thread.setName(self.name)

        self.is_new = True

    def setupTriggers(self):
        pass

    def thread_loop(self):
        self.is_new = False
        while True:
            if not self.__active_triggers__.empty():
                self.isQueueEmpty.set(False)
                trigger = self.__active_triggers__.get_nowait()

                if trigger is None:
                    break

                if trigger.exception is not None:
                    try:
                        if self.runCondition(trigger):
                            self.runActiveTrigger(trigger)
                        else:
                            self.runElseActiveTrigger(trigger)
                    except trigger.exception as e:
                        trigger.runCatchAction()
                else:
                    if self.runCondition(trigger):
                        self.runActiveTrigger(trigger)
                    else:
                        self.runElseActiveTrigger(trigger)
            else:
                self.isQueueEmpty.set(True)

    def addActiveTrigger(self, trigger):
        self.__active_triggers__.put_nowait(trigger)

        if not self.isAlive():
            self.start()

    def isTriggerInQueue(self, trigger):
        return id(trigger) in [id(obj) for obj in self.__active_triggers__]

    def start(self):
        # Log.p(f"startThread: {self.name}")
        self.thread.start()

    def stop(self):
        # Log.p(f"stopThread: {self.name}")
        self.__active_triggers__.put_nowait(None)

    def sleep(self, secs):
        time.sleep(secs)

    def join(self):
        self.thread.join()

    def isAlive(self):
        return self.thread.is_alive()

    def _setName(self, name):
        self.name = name
        self.__name__ = name


class DyThreadList(DyExecution):
    def __call__(self, name=None, **kwargs):
        # Log.p(f"DyThreadList.__init__({name})")
        self.name = name
        super(DyBuiltinModule, self).__init__()

    def setupVariables(self):
        # Create the dict of dyThreads and other relevant variables.
        self.dyThreads = {}
        self.__available_thread_ids = [0]  # TODO lahav The efficiency of this mechanism can be improved by using stack.

        self.isQueueEmpty = DyBoolList(builtin=True)
        self.isQueueEmpty._set(True)

    def addActiveTrigger(self, trigger):
        # Create a new DyThread and add it to the dict and then start it.

        # Update the the available thread ids
        thread_id = self.__available_thread_ids.pop(0)
        if not self.__available_thread_ids:
            self.__available_thread_ids.append(thread_id + 1)

        dyThread = self.dyThreads[thread_id] = DyThread()
        dyThread(name=f"{self.name} #{thread_id}")
        dyThread.addActiveTrigger(trigger)
        self.isQueueEmpty.add(dyThread.isQueueEmpty)

    def stop(self):
        for dy_thread in self.dyThreads.values():
            dy_thread.stop()
