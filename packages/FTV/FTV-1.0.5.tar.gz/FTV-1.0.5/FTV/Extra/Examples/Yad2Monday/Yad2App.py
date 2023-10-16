from FTV.Extra.Examples.Yad2Monday.Features import MondayUploader, HouseCollection
from FTV.FrameWork.Apps import NIApp
from FTV.Managers.ExecutionManager import ExecutionManager
from FTV.Managers.FeatureManager import FeatureManager
from FTV.Tools.Log import Log
from FTV.Managers.VariableManager import VariableManager
from FTV.Objects.SystemObjects.Executions import DyThread
from FTV.Objects.Variables.DynamicMethods import DyBuiltinMethod
from FTV.Objects.Variables.DynamicObjects import DySwitch, DyList


class VM(VariableManager):
    def setupVariables(self):
        self.houses = DyList()

        self.onReadyToCollect = DySwitch()
        self.onCollectionCompleted = DySwitch()
        self.onReadyToUploadToMonday = DySwitch()
        self.onUploadToMondayCompleted = DySwitch()

    def setupTriggers(self):
        pass


class EM(ExecutionManager):
    def setupThreads(self):
        self.MainUI = DyThread()
        # self.Workers = DyThreadList()


class FM(FeatureManager):
    def setupFeatures(self):
        self.addFeature(HouseCollection)
        self.addFeature(MondayUploader)
        pass


class Yad2App(NIApp):
    def setupSettings(self):
        pass

    def setupManagers(self):
        self.setExecutionManager(EM)
        self.setFeatureManager(FM)
        self.setVariableManager(VM)

    def setupTriggers(self):
        self.addTrigger(self.vm.START).setAction(self.vm.onReadyToCollect)
        self.addTrigger(self.vm.onCollectionCompleted).setAction(self.vm.onReadyToUploadToMonday)
        self.addTrigger(self.vm.onUploadToMondayCompleted).setAction(self.printUploadFinished)

    @DyBuiltinMethod()
    def printUploadFinished(self):
        Log.p("Upload finished :)")
