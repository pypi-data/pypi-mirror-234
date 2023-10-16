from FTV.FrameWork.Features import NIFeature
from FTV.Tools.Log import Log
from FTV.Managers.VariableManager import VariableManager
from FTV.Objects.Variables.DynamicMethods import DyMethod, DyBuiltinMethod
from FTV.Objects.Variables.DynamicObjects import DySwitch


class VM(VariableManager):
    def setupVariables(self):
        # self.calendar = TickTick(
        #     "lahavs512@gmail.com",
        #     "1l3a1m3l1a3m"
        # )
        # self.collector = InBar(
        #     "206864555",
        #     "3azZDfLC%ENN9a!",
        #     "https://inbar.biu.ac.il/"
        # )
        self.onCollectorLoginCompleted = DySwitch()
        self.onCalendarLoginCompleted = DySwitch()
        self.folder = "Studies/Schedule"

    def setupTriggers(self):
        pass


class ExamSchedule(NIFeature):
    def setupSettings(self):
        self.settings.setEnabled()

    def setupManagers(self):
        self.setVariableManager(VM)

    def setupTriggers(self):
        from FTV.Extra.Examples.BIUAutomation.BIUApp import BIUApp

        # Collector
        self.addTrigger(BIUApp.vm.onStartCollection).setAction(self.collectorLogin)\
            # .catchAction(self.showLoginErrorMessage)
        self.addTrigger(self.collectorLogin).setAction(self.vm.onCollectorLoginCompleted)
        self.addTrigger(self.vm.onCollectorLoginCompleted).setAction(self.getEvents)

        self.addTrigger(BIUApp.vm.collectedEvents).setAction(BIUApp.vm.onCollectedEventsUpdated)
        self.addTrigger(BIUApp.vm.onCollectedEventsUpdated).setAction(self.printCollectedEvents)


        # Calendar
        self.addTrigger(BIUApp.vm.onCollectedEventsUpdated).setAction(self.calendarLogin)\
            # .catchAction(self.showLoginErrorMessage)
        self.addTrigger(self.calendarLogin).setAction(self.vm.onCalendarLoginCompleted)
        self.addTrigger(self.vm.onCalendarLoginCompleted).setAction(self.updateAllEvents)
        self.addTrigger(self.updateAllEvents).setAction(BIUApp.vm.onCalendarEventsUpdated)

    @DyBuiltinMethod()
    def calendarLogin(self):
        self.vm.calendar.login()

    @DyBuiltinMethod()
    def collectorLogin(self):
        self.vm.collector.login("live/Login.aspx", with_index=False)

    @DyMethod()
    def getEvents(self):
        from FTV.Extra.Examples.BIUAutomation.BIUApp import BIUApp

        BIUApp.vm.collectedEvents.set(self.vm.collector.getEvents())

    @DyMethod()
    def printCollectedEvents(self):
        from FTV.Extra.Examples.BIUAutomation.BIUApp import BIUApp

        for event in BIUApp.vm.collectedEvents:
            Log.d(f"Collected event: {event['title']}")

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
