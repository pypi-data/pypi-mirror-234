import time

from FTV.FrameWork.Features import NIFeature
from FTV.Managers.VariableManager import VariableManager
from FTV.Objects.SystemObjects.TriggerObjects import Condition
from FTV.Objects.Variables.AbstractDynamicObject import DyObject
from FTV.Objects.Variables.DynamicMethods import DyMethod, DyBuiltinMethod
from FTV.Objects.Variables.DynamicObjects import DyInt


class VM(VariableManager):
    def setupVariables(self):
        self.isStopped = False
        self.seconds = DyInt(-1, builtin=False)
        self.period = 3  # seconds

    def setupTriggers(self):
        self.addTrigger(self.seconds).setCondition(DyInt.IsChangedTo, self.period).setAction(self.setDyObject, self.seconds, 0)

    @DyBuiltinMethod()
    def setDyObject(self, object: DyObject, value):
        object.set(value)

    class PeriodCompleted(Condition):
        @staticmethod
        def __condition__(old_val, new_val, *args, **kwargs):
            return new_val % args[0] == 0


class Timer(NIFeature):
    def setupSettings(self):
        pass

    def setupManagers(self):
        self.setVariableManager(VM)

    def setupTriggers(self):
        from FTV.Extra.Examples.BIUAutomation.BIUApp import BIUApp

        self.overrideTriggers(BIUApp.vm.START).setAction(self.startClock)
        # self.addTrigger(self.vm.seconds).setCondition(self.vm.PeriodCompleted, self.vm.period).setAction(BIUApp.vm.onStartCollection)
        self.addTrigger(self.vm.seconds).setCondition(DyInt.IsEqualTo, 0).setAction(BIUApp.vm.onStartCollection)

    def stop(self):
        self.vm.isStopped = True

    @DyMethod()
    def updateDyObject(self, obj: DyObject, new_obj: DyObject):
        obj.set(new_obj.get())

    @DyMethod()
    def startClock(self):
        while not self.vm.isStopped:
            self.tick()

    @DyBuiltinMethod()
    def tick(self):
        self.vm.seconds += 1
        time.sleep(1)
