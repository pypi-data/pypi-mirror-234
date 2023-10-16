from FTV.Tools.Log import Log
from FTV.Objects.Variables.DynamicIterators import DyBoolList
from FTV.Objects.Variables.DynamicMethods import DyMethod
from FTV.Objects.Variables.DynamicModules import DyModule
from FTV.Objects.Variables.DynamicObjects import DyBool


class VariableManager(DyModule):

    def setupVariables(self):
        self.a = DyBool(False)
        self.b = DyBool(False)
        self.c = DyBool(False)
        self.list_1 = DyBoolList()

    def setupTriggers(self):
        self.list_1.add(self.a, self.b, self.c)

        self.addTrigger(self.POST_INIT).setAction(self.updateABC, True, True, True)
        self.addTrigger(self.list_1).setAction(self.printWorks)

    @DyMethod()
    def printWorks(self):
        Log.p("DyBoolList Works!")

    @DyMethod()
    def updateABC(self, a, b, c):
        self.a.set(a)
        self.b.set(b)
        self.c.set(c)

        Log.p(f"{self.list_1}")


vm = VariableManager()
