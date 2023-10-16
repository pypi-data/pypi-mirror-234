import time

import pymsgbox

from FTV.Extra.Examples.BIUAutomation import InBar
from FTV.FrameWork.Features import NIFeature
from FTV.Tools.Log import Log
from FTV.Managers.VariableManager import VariableManager
from FTV.Objects.Variables.DynamicMethods import DyMethod
from FTV.Objects.Variables.DynamicObjects import DySwitch, DyInt


class VM(VariableManager):
    def setupVariables(self):
        # self.calendar = TickTick(
        #     "lahavs512@gmail.com",
        #     "1l3a1m3l1a3m"
        # )
        self.course_codes = [
            # "01034",
            "01130",
            "03099",
            # "04010"
            "01078",
        ]

        self.NUM_OF_WORKERS = len(self.course_codes)
        self.collectors = []
        self.worker_count = DyInt(0)
        self.registration_time = 0

        for _ in range(self.NUM_OF_WORKERS):
            self.collector = InBar(
                "206864555",
                "-P0o9I8u7Y6t",
                "https://inbar.biu.ac.il/"
            )
            self.collectors.append(self.collector)

        self.onCollectorLoginCompletedList = [DySwitch() for _ in range(self.NUM_OF_WORKERS)]
        self.folder = "Studies/Schedule"

    def setupTriggers(self):
        pass


class CourseRegistration(NIFeature):
    def setupSettings(self):
        self.settings.setEnabled()

    def setupManagers(self):
        self.setVariableManager(VM)

    def setupTriggers(self):
        from FTV.Extra.Examples.BIUAutomation.BIURegistrationApp import BIURegistrationApp

        # Collector
        for i in range(self.vm.NUM_OF_WORKERS):
            self.addTrigger(BIURegistrationApp.vm.START).setAction(self.collectorLoginAndRegisterCourse, i)\
                .setThread(BIURegistrationApp.em.Workers)

        self.addTrigger(self.vm.worker_count).setCondition(DyInt.IsChangedTo, 0).setAction(self.printRegistrationIsDone)

        # for i, onCollectorLoginCompleted in enumerate(self.vm.onCollectorLoginCompletedList):
        #     self.addTrigger(self.collectorLogin).setAction(onCollectorLoginCompleted)
        #     self.addTrigger(onCollectorLoginCompleted).setAction(self.collectorRegisterCourse, i)

    def countWorkers(self, add):
        self.vm.worker_count += add

    @DyMethod()
    def printRegistrationIsDone(self):
        Log.p(f"Total registration time: {self.vm.registration_time} sec", Log.color.RED)

    @DyMethod()
    def collectorLoginAndRegisterCourse(self, i):
        self.countWorkers(1)

        start_time = time.time()
        self.collectorLogin(i)
        is_succeeded = self.collectorRegisterCourse(i)
        end_time = time.time()

        self.vm.registration_time = round(max(self.vm.registration_time, end_time - start_time))

        self.countWorkers(-1)

        if is_succeeded:
            # Show a messagebox alert
            course_code = self.vm.course_codes[i]
            pymsgbox.alert(f"code: {course_code}",
                           "Registration Success :)")

    @DyMethod()
    def collectorLogin(self, i):
        time.sleep(4*i)
        self.vm.collectors[i].login("live/Login.aspx", with_index=False)

    @DyMethod()
    def collectorRegisterCourse(self, i):
        is_succeeded = False
        try:
            course_code = self.vm.course_codes[i]
            is_succeeded = self.vm.collectors[i].registerCourse(course_code)
        except Exception:
            Log.e(f"An error occurd while trying to register course {course_code}", color=Log.color.RED)

        return is_succeeded

    # @DyMethod()
    # def showLoginErrorMessage(self):
    #     Log.e(f"Could not login to '{self.vm.collector.website_url}'.\n"
    #           f"Please check the credentials.")
