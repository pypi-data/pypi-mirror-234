import math

from FTV.Extra.Examples.Algorithms import CalculationApp
from FTV.Tools.Log import Log
from FTV.FrameWork.Features import NIFeature
from FTV.Managers.VariableManager import VariableManager
from FTV.Objects.SystemObjects.TriggerObjects import Condition
from FTV.Objects.Variables.DynamicMethods import DyMethod, DyBuiltinMethod
from FTV.Objects.Variables.DynamicObjects import DyFloat


class VM(VariableManager):
    def setupVariables(self):
        self.progress = CalculationApp.vm.progress
        self.rounded_progress = DyFloat(self.progress.get(), builtin=True)
        # self.isUpdatePBFree = DyBool(True, builtin=True)
        self.progress_step = 0.001

    def setupTriggers(self):
        self.addTrigger(self.progress).setAction(self.updateRoundedPB).setCondition(DyFloat.IsChanged).setUnique()\
            .setThread(CalculationApp.em.getCurrentThread()) \

    @DyBuiltinMethod()
    def updateRoundedPB(self):
        # if self.progress // self.progress_step > 0:
        #     print()
        self.rounded_progress.set(self.progress_step*(self.progress // self.progress_step))

    class IsRoundCompleted(Condition):
        @staticmethod
        def __condition__(old_val, new_val, *args, **kwargs):
            # ans = old_val < args[0]*(new_val // args[0])
            ans = new_val // args[0] - old_val // args[0] >= 1
            return ans


class ProgressBar(NIFeature):
    def setupSettings(self):
        pass

    def setupManagers(self):
        self.setVariableManager(VM)

    def setupTriggers(self):
        # self.addTrigger(self.vm.progress).setAction(self.vm.isUpdatePBFree, False)
        self.addTrigger(self.vm.rounded_progress)\
            .setAction(self.updatePB)\
            .setThread(CalculationApp.em.MainUI)\
            .setCondition(VM.IsChanged)\
            .setUnique()
            # .setCondition(self.vm.isUpdatePBFree)

        # self.addTrigger(self.updatePB).setAction(self.vm.isUpdatePBFree, True)

    @DyMethod()
    def updatePB(self):
        Log.p(f"{math.ceil(self.vm.progress * 100 * 10) / 10}%")
        queue_len = len(CalculationApp.em.MainUI.__active_triggers__)

        if queue_len > 1:
            Log.e(queue_len)
