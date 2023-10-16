from FTV.Tools.Log import Log
from FTV.Objects.Variables.DynamicMethods import DyMethod
from FTV.Objects.Variables.DynamicModules import DyModule
from FTV.Objects.Variables.DynamicObjects import DyInt


class VariableManager(DyModule):

    def setupVariables(self):
        self.a = DyInt(1)
        self.b = DyInt(2)

    def setupTriggers(self):
        self.addTrigger(self.POST_INIT).setAction(self.updateA, 5)
        self.addTrigger(self.updateA).setAction(self.updateB, 3)
        self.addTrigger(self.b).setAction(self.printWorks)

    @DyMethod()
    def printWorks(self):
        Log.p("DyBoolList Works!")

    @DyMethod()
    def updateA(self, a):
        self.a += a

    @DyMethod()
    def updateB(self, b):
        self.b += b


vm = VariableManager()
