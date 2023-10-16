from FTV.Tools.Log import Log
from FTV.Objects.Variables.DynamicIterators import DySwitchList, DyBoolList
from FTV.Objects.Variables.DynamicMethods import DyMethod
from FTV.Objects.Variables.DynamicModules import DyModule
from FTV.Objects.Variables.DynamicObjects import DyBool


class VariableManager(DyModule):

    def setupVariables(self):
        self.a_master = DyBool(False)
        self.master = DyBoolList()

        self.a = DyBool(False)
        self.b = DyBool(False)
        self.c = DyBool(False)
        self.list = DySwitchList()

    def setupTriggers(self):
        self.master.add(self.a_master)
        self.list.add(self.a, self.b, self.c, self.master)

        self.addTrigger(self.POST_INIT).setAction(self.updateABC, True, True, True)
        self.addTrigger(self.updateABC).setAction(self.updateABC2, True, True, True)
        self.addTrigger(self.list).setAction(self.printWorks)

    @DyMethod()
    def printWorks(self):
        Log.p("DyBoolList Works!")
        for item in self.list:
            Log.p(item.__name__)
        Log.p(len(self.list))
        # self.list.set(False)
        Log.p(self.list)

    @DyMethod()
    def updateABC(self, a, b, c):
        self.a.set(a)
        self.b.set(b)
        self.c.set(c)
        self.a_master.set(True)
        # Log.p(self.master)

    @DyMethod()
    def updateABC2(self, a, b, c):
        # Log.p(self.list)
        self.a.set(a)
        self.b.set(b)
        self.c.set(c)
        self.a_master.set(True)


vm = VariableManager()
