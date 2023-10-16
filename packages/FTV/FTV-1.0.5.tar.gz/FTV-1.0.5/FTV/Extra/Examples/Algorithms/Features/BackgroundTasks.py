import time

from FTV.Extra.Examples.Algorithms import CalculationApp
from FTV.Tools.Log import Log
from FTV.FrameWork.Features import NIFeature
from FTV.Managers.VariableManager import VariableManager
from FTV.Objects.Variables.DynamicMethods import DyMethod


class VM(VariableManager):
    def setupVariables(self):
        self.progress = CalculationApp.vm.progress
        self.file_path = "/Extra/Examples/Algorithms/Data/log.txt"

    def setupTriggers(self):
        pass


class BackgroundTasks(NIFeature):
    def setupSettings(self):
        pass

    def setupManagers(self):
        self.setVariableManager(VM)

    def setupTriggers(self):
        self.addTrigger(CalculationApp.vm.START).setAction(self.backgroundTask)\
            .setThread(CalculationApp.em.Algorithms)

    @DyMethod()
    def backgroundTask(self):
        N = 20
        maximum = 2*17711 - 1
        # for k in range(N/2):
        #     maximum += math.factorial(N+1-k)/math.factorial(2*k)/math.factorial()

        self.del_progress = 1/maximum
        self.results = set()

        self.file = open(self.vm.file_path, 'w+')

        res = self.calculateFib(N)
        Log.p(res)

        self.file.close()

    def calculateFib(self, n):

        # Log.d(self.vm.progress + self.del_progress)
        # print(self.vm.progress + self.del_progress)
        self.printToFile(self.vm.progress + self.del_progress)
        self.vm.progress += self.del_progress

        # if self.vm.progress > 0.01:
        #     pass
            # Event().wait(0.1)
            # CalculationApp.em.getCurrentThread().sleep(0.1)

        if n == -1:
            return 1
        elif n == 0:
            return 0

        res = self.calculateFib(n - 1) + self.calculateFib(n - 2)
        if res not in self.results:
            time.sleep(0.01)

        self.results.add(res)
        return res

    def printToFile(self, message):
        self.file.write(str(message) + "\n")
