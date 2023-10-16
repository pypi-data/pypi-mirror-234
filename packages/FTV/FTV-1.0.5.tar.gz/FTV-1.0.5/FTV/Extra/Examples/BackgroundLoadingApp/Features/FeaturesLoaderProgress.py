from FTV.Extra.Examples.BackgroundLoadingApp import App
from FTV.Tools.Log import Log
from FTV.FrameWork.Features import NIFeature
from FTV.Managers.VariableManager import VariableManager
from FTV.Objects.Variables.DynamicMethods import DyMethod


class VM(VariableManager):
    def setupVariables(self):
        self.progress = App.fm.features[1].fm.loading_progress  # TODO lahav Please access this variable properly.

    def setupTriggers(self):
        pass


class FeaturesLoaderProgress(NIFeature):
    def setupSettings(self):
        self.settings.setEnabled()

    def setupManagers(self):
        self.setVariableManager(VM)

    def setupTriggers(self):
        self.addTrigger(self.vm.progress, first=True).setAction(self.printProgress)\
            .setThread(App.em.MainUI)

    @DyMethod()
    def printProgress(self):
        Log.p(f"{round(self.vm.progress * 100, 1)}%")
