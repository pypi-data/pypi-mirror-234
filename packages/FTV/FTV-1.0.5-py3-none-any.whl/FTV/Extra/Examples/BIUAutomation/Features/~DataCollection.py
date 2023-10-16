from FTV.Extra.Examples.BIUAutomation import Moodle
from FTV.FrameWork.Features import NIFeature
from FTV.Tools.Log import Log
from FTV.Managers.VariableManager import VariableManager
from FTV.Objects.Variables.DynamicMethods import DyMethod, DyBuiltinMethod
from FTV.Objects.Variables.DynamicObjects import DySwitch


class VM(VariableManager):
    def setupVariables(self):
        self.collector = Moodle(
            "206864555",
            "3azZDfLC%ENN9a!",
            "https://lemida.biu.ac.il/"
        )
        self.onLoginCompleted = DySwitch()

    def setupTriggers(self):
        pass


class DataCollection(NIFeature):
    def setupSettings(self):
        pass

    def setupManagers(self):
        self.setVariableManager(VM)

    def setupTriggers(self):
        from FTV.Extra.Examples.BIUAutomation.BIUApp import BIUApp

        self.addTrigger(BIUApp.vm.onStartCollection).setAction(self.login)\
            # .catchAction(self.showLoginErrorMessage)
        self.addTrigger(self.login).setAction(self.vm.onLoginCompleted)
        self.addTrigger(self.vm.onLoginCompleted).setAction(self.getEvents)

        self.addTrigger(BIUApp.vm.collectedEvents).setAction(BIUApp.vm.onCollectedEventsUpdated)
        self.addTrigger(BIUApp.vm.onCollectedEventsUpdated).setAction(self.printCollectedEvents)

    @DyBuiltinMethod()
    def login(self):
        self.vm.collector.login("blocks/login_ldap/")

    @DyMethod()
    def showLoginErrorMessage(self):
        Log.e(f"Could not login to '{self.vm.collector.website_url}'.\n"
              f"Please check the credentials.")

    @DyMethod()
    def getEvents(self):
        from FTV.Extra.Examples.BIUAutomation.BIUApp import BIUApp

        BIUApp.vm.collectedEvents.set(self.vm.collector.getEvents())

    @DyMethod()
    def printCollectedEvents(self):
        from FTV.Extra.Examples.BIUAutomation.BIUApp import BIUApp

        for event in BIUApp.vm.collectedEvents:
            Log.d(f"Collected event: {event['title']}")
