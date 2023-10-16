import time

from FTV.Tools.Log import Log
from FTV.FrameWork.Apps import UIApp
from FTV.Managers.ExecutionManager import ExecutionManager
from FTV.Managers.FeatureManager import FeatureManager
from FTV.Objects.SystemObjects.Executions import DyThread, DyThreadList
from FTV.Objects.Variables.DynamicMethods import DyMethod


class EM(ExecutionManager):
    def setupThreads(self):
        self.MainUI = DyThread()
        self.MainApplication = DyThread()
        self.Tests = DyThreadList()


class FM(FeatureManager):
    def setupFeatures(self):
        from FTV.Extra.Examples.BackgroundLoadingApp.Features import FeaturesLoader
        from FTV.Extra.Examples.BackgroundLoadingApp.Features.FeaturesLoaderProgress import \
            FeaturesLoaderProgress

        self.addFeature(FeaturesLoaderProgress)
        self.addFeature(FeaturesLoader)


class App(UIApp):
    def setupSettings(self):
        pass

    def setupManagers(self):
        self.setExecutionManager(EM)
        self.setFeatureManager(FM)

    def setupTriggers(self):
        self.addTrigger(self.vm.START).setAction(self.startAppOperations).setThread(self.em.MainApplication)
        self.addTrigger(self.vm.START).setAction(self.startAppOperations).setThread(self.em.MainUI)

    @DyMethod()
    def startAppOperations(self):
        Log.p("Application is running!")
        # time.sleep(1)

    @DyMethod()
    def startTest(self, test):
        Log.p(f"Running \"{test}\"")
        time.sleep(int(test[-1]))


if __name__ == '__main__':
    app = App()
