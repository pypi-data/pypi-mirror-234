from FTV.Extra.Examples.BIUAutomation import TickTick
from FTV.Tools.Log import Log
from FTV.FrameWork.Features import NIFeature
from FTV.Managers.VariableManager import VariableManager
from FTV.Objects.Variables.DynamicMethods import DyMethod, DyBuiltinMethod
from FTV.Objects.Variables.DynamicObjects import DySwitch


class VM(VariableManager):
    def setupVariables(self):
        self.calendar = TickTick(
            "lahavs512@gmail.com",
            "1l3a1m3l1a3m"
        )
        self.onLoginCompleted = DySwitch()
        self.folder = "Studies/Assignments"

    def setupTriggers(self):
        pass


class DataSharing(NIFeature):
    def setupSettings(self):
        self.settings.setEnabled()

    def setupManagers(self):
        self.setVariableManager(VM)

    def setupTriggers(self):
        from FTV.Extra.Examples.BIUAutomation.BIUApp import BIUApp

        self.addTrigger(BIUApp.vm.onCollectedEventsUpdated).setAction(self.login)\
            # .catchAction(self.showLoginErrorMessage)
        self.addTrigger(self.login).setAction(self.vm.onLoginCompleted)
        self.addTrigger(self.vm.onLoginCompleted).setAction(self.updateAllEvents)
        self.addTrigger(self.updateAllEvents).setAction(BIUApp.vm.onCalendarEventsUpdated)

    @DyBuiltinMethod()
    def login(self):
        self.vm.calendar.login()

    @DyMethod()
    def showLoginErrorMessage(self):
        Log.e(f"Could not login to '{self.vm.collector.website_url}'.\n"
              f"Please check the credentials.")

    @DyMethod()
    def updateAllEvents(self):
        from FTV.Extra.Examples.BIUAutomation.BIUApp import BIUApp

        for event in BIUApp.vm.collectedEvents:
            if self.vm.calendar.isExist(event, self.vm.folder):
                self.update(event)
            else:
                self.create(event)

    @DyBuiltinMethod()
    def create(self, event):
        self.vm.calendar.create(event, self.vm.folder)
        Log.d(f"Created event: {event['title']}")

    @DyBuiltinMethod()
    def update(self, event):
        self.vm.calendar.update(event, self.vm.folder)
        Log.d(f"Updated event: {event['title']}")

    @DyMethod()
    def delete(self, event):
        self.vm.calendar.delete(event, self.vm.folder)
        Log.d(f"Deleted event: {event['title']}")
