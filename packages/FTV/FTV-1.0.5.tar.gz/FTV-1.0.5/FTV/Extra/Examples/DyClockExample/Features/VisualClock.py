from FTV.Extra.Examples.DyClockExample.ClockApp import ClockApp
from FTV.Tools.Log import Log
from FTV.FrameWork.Features import NIFeature
from FTV.Objects.Variables.DynamicMethods import DyMethod
from FTV.Objects.Variables.DynamicObjects import DyInt


class VisualClock(NIFeature):
    def setupSettings(self):
        self.settings.setEnabled()

    def setupManagers(self):
        pass

    def setupTriggers(self):
        self.addTrigger(ClockApp.vm.seconds).setCondition(DyInt.IsChanged).setAction(self.updateSecondsRadius)\
            .setThread(ClockApp.em.MainUI)
        self.addTrigger(ClockApp.vm.minutes).setCondition(DyInt.IsChanged).setAction(self.updateMinutesRadius)\
            .setThread(ClockApp.em.MainUI)
        self.addTrigger(ClockApp.vm.hours).setCondition(DyInt.IsChanged).setAction(self.updateHoursRadius)\
            .setThread(ClockApp.em.MainUI)

    @DyMethod()
    def updateSecondsRadius(self):
        Log.p("FTV Works!!!")

    @DyMethod()
    def updateMinutesRadius(self):
        Log.p("FTV Works!!!")

    @DyMethod()
    def updateHoursRadius(self):
        Log.p("FTV Works!!!")
