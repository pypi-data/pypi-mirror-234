import time

from FTV.Extra.Examples.DyClockExample.ClockApp import ClockApp
from FTV.Tools.Log import Log
from FTV.FrameWork.Features import NIFeature
from FTV.Managers.VariableManager import VariableManager
from FTV.Objects.Variables.DynamicMethods import DyMethod
from FTV.Objects.Variables.DynamicObjects import DyInt, DyObject


class VM(VariableManager):
    def setupVariables(self):
        self.tenth_seconds_mode = 10
        self.seconds_mode = 60
        self.minutes_mode = 60
        self.hours_mode = 24

        self.tenth_seconds = ClockApp.vm.tenth_seconds
        self.seconds = ClockApp.vm.seconds
        self.minutes = ClockApp.vm.minutes
        self.hours = ClockApp.vm.hours

    def setupTriggers(self):
        self.addTrigger(self.tenth_seconds)\
            .setCondition(DyInt.IsGraterEqualTo, self.tenth_seconds_mode)\
            .setAction(self.updateUnit, self.tenth_seconds, self.seconds, self.tenth_seconds_mode)

        self.addTrigger(self.seconds)\
            .setCondition(DyInt.IsGraterEqualTo, self.seconds_mode)\
            .setAction(self.updateUnit, self.seconds, self.minutes, self.seconds_mode)

        self.addTrigger(self.minutes)\
            .setCondition(DyInt.IsGraterEqualTo, self.minutes_mode)\
            .setAction(self.updateUnit, self.minutes, self.hours, self.minutes_mode)

        self.addTrigger(self.hours)\
            .setCondition(DyInt.IsGraterEqualTo, self.hours_mode)\
            .setAction(self.modUnit, self.hours, self.hours, self.hours_mode)

    @DyMethod()
    def updateUnit(self, var_1: DyInt, var_2: DyInt, mod: int):
        self.addUnit(var_2, var_1, mod)
        self.modUnit(var_1, var_1, mod)

    # @DyMethod()
    def modUnit(self, var: DyInt, val: DyInt, mod: int):
        var.set(val.get() % mod)

    # @DyMethod()
    def addUnit(self, var: DyInt, val: DyInt, mod: int):
        var += val.get() // mod


class IntegratedClock(NIFeature):
    def setupSettings(self):
        pass

    def setupManagers(self):
        self.setVariableManager(VM)

    def setupTriggers(self):
        self.addTrigger(ClockApp.vm.START).setAction(self.startClock)

    def getTimeStamp(self):
        return f"{self.vm.hours}:{self.vm.minutes}:{self.vm.seconds}:{self.vm.tenth_seconds}"

    @DyMethod()
    def updateDyObject(self, obj: DyObject, new_obj: DyObject):
        obj.set(new_obj.get())

    @DyMethod()
    def startClock(self):
        while self.vm.minutes < 3:
            self.tick()

    @DyMethod()
    def tick(self):
        self.vm.seconds += 1
        Log.p(self.getTimeStamp())
        time.sleep(1)
