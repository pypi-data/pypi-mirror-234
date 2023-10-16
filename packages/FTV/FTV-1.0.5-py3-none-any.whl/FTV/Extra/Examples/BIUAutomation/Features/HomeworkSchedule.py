from FTV.Extra.Examples.BIUAutomation import TickTick
from FTV.Extra.Examples.BIUAutomation import MoodleCalendar
from FTV.FrameWork.Features import NIFeature
from FTV.Tools.Log import Log
from FTV.Managers.VariableManager import VariableManager
from FTV.Objects.SystemObjects.TriggerObjects import Condition
from FTV.Objects.Variables.DynamicMethods import DyMethod, DyBuiltinMethod
from FTV.Objects.Variables.DynamicObjects import DySwitch, DyList


class User:
    def __init__(self):
        self.calendar_user = None
        self.calendar_pass = None
        self.calendar_folder = None
        self.collector_user = None
        self.collector_pass = None
        self.collector_url = None
        self.collector_calendar_url = None

    def setCalendarUser(self, user):
        self.calendar_user = user

    def setCalendarPass(self, _pass):
        self.calendar_pass = _pass

    def setCalendarFolder(self, folder):
        self.calendar_folder = folder

    def setCollectorUser(self, user):
        self.collector_user = user

    def setCollectorPass(self, _pass):
        self.collector_pass = _pass

    def setCollectorURL(self, url):
        self.collector_url = url

    def setCollectorCalendarUrl(self, url):
        self.collector_calendar_url = url

    def getCalendarUser(self):
        return self.calendar_user

    def getCalendarPass(self):
        return self.calendar_pass

    def getCalendarFolder(self):
        return self.calendar_folder

    def getCollectorUser(self):
        return self.collector_user

    def getCollectorPass(self):
        return self.collector_pass

    def getCollectorURL(self):
        return self.collector_url

    def getCollectorCalendarUrl(self):
        return self.collector_calendar_url


class VM(VariableManager):
    def setupVariables(self):
        self.user: User = None
        self.users = DyList(builtin=True)
        self.setupUsers()

        self.onCollectorLoginCompleted = DySwitch()
        self.onCalendarLoginCompleted = DySwitch()

    def setupTriggers(self):
        pass

    def setupUsers(self):
        lahav = User()
        lahav.setCalendarUser("lahavs512@gmail.com")
        lahav.setCalendarPass("1l3a1m3l1a3m")
        lahav.setCalendarFolder("Assignments")
        # lahav.setCollectorUser("svorail@biu.ac.il")
        # lahav.setCollectorPass("-P0o9I8u7Y6t")
        # lahav.setCollectorURL("https://lemida.biu.ac.il/")
        lahav.setCollectorCalendarUrl(
            "https://lemida.biu.ac.il/calendar/export_execute.php?"
            "userid=123430&"
            "authtoken=6a23d0ac3a02afa4dd15d7f5050217f7568c1d9a&"
            "preset_what=all&"
            "preset_time=custom"
        )

        self.users._append(lahav)

        david = User()
        david.setCalendarUser("david@ovadya.org")
        david.setCalendarPass("rWrEFPf8r5i6xiJ")
        david.setCalendarFolder("Studies/Assignments")
        david.setCollectorUser("207320425")  # Please update this to the university email!!!
        david.setCollectorPass("jhDkjnejnSSW13!")
        david.setCollectorURL("https://lemida.biu.ac.il/")

        # self.users._append(david)

    class IsNotEmpty(Condition):
        @staticmethod
        def __condition__(old_val, new_val, *args, **kwargs):
            users = args[0]
            return bool(users)

    class IsEmpty(Condition):
        @staticmethod
        def __condition__(old_val, new_val, *args, **kwargs):
            users = args[0]
            return not bool(users)


class HomeworkSchedule(NIFeature):
    def setupSettings(self):
        self.settings.setEnabled()

    def setupManagers(self):
        self.setVariableManager(VM)

    def setupTriggers(self):
        from FTV.Extra.Examples.BIUAutomation.BIUApp import BIUApp

        # Collector
        self.addTrigger(BIUApp.vm.START).setCondition(VM.IsNotEmpty, self.vm.users).setAction(self.nextUser)
        self.addTrigger(self.nextUser).setAction(self.setupCredentials)
        self.addTrigger(self.setupCredentials).setAction(BIUApp.vm.onStartCollection)
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
        self.addTrigger(BIUApp.vm.onCalendarEventsUpdated).setCondition(VM.IsNotEmpty, self.vm.users).setAction(self.nextUser)

    @DyBuiltinMethod()
    def calendarLogin(self):
        self.vm.calendar.login()

    @DyBuiltinMethod()
    def collectorLogin(self):
        self.vm.collector.login("blocks/login_ldap/")

    @DyMethod()
    def nextUser(self):
        self.vm.user = self.vm.users.pop(0)

    @DyMethod()
    def setupCredentials(self):
        self.vm.calendar = TickTick(
            self.vm.user.getCalendarUser(),
            self.vm.user.getCalendarPass()
        )
        # self.vm.collector = Moodle(
        #     self.vm.user.getCollectorUser(),
        #     self.vm.user.getCollectorPass(),
        #     self.vm.user.getCollectorURL()
        # )
        self.vm.collector = MoodleCalendar(
            self.vm.user.getCollectorCalendarUrl(),
        )
        self.vm.folder = self.vm.user.getCalendarFolder()

    @DyMethod()
    def getEvents(self):
        from FTV.Extra.Examples.BIUAutomation.BIUApp import BIUApp
        # Log.d(f"Calendar user: {self.vm.user.getCalendarUser()}")
        # Log.d(f"Calendar pass: {self.vm.user.getCalendarPass()}")
        # Log.d(f"Calendar folder: {self.vm.user.getCalendarFolder()}")
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
