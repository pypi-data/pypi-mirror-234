from FTV.Extra.Experiments import Efficiency
from FTV.Tools.Log import Log
from FTV.Objects.Variables.DynamicMethods import DyMethod
from FTV.Objects.Variables.DynamicModules import DyModule
from FTV.Objects.Variables.DynamicObjects import DySwitch, DyBool


class DynamicModule(DyModule):
    @staticmethod
    def print(message):
        Log.p(message)

    @DyMethod()
    def ftvWorks(self):
        self.print("FTV Works!")

    @DyMethod()
    def firstMethod(self):
        self.first.activate()

    @DyMethod()
    def secondMethod(self):
        self.second.activate()

    @DyMethod()
    def thirdMethod(self):
        self.third.activate()

    def setupVariables(self):
        self.first = DySwitch()
        self.second = DySwitch()
        self.third = DySwitch()

    def setupTriggers(self):
        self.addTrigger(self.POST_LOAD).setAction(self.firstMethod)
        self.addTrigger(self.first).setAction(self.secondMethod)
        self.addTrigger(self.second).setAction(self.thirdMethod)
        self.addTrigger(self.third).setAction(self.ftvWorks)


class SimpleDyModule(DyModule):

    def __init__(self):
        super(SimpleDyModule, self).__init__()
        self.first = DySwitch()
        self.second = DySwitch()
        self.third = DySwitch()

        self.firstMethod()
        if self.first.get():
            self.secondMethod()
            if self.second.get():
                self.thirdMethod()
                if self.third.get():
                    self.ftvWorks()

    @staticmethod
    def print(message):
        Log.p(message)

    # @DyMethod()
    def ftvWorks(self):
        self.print("FTV Works!")

    # @DyMethod()
    def firstMethod(self):
        # self.print("firstMethod")
        self.first.activate()

    # @DyMethod()
    def secondMethod(self):
        # self.print("secondMethod")
        self.second.activate()

    # @DyMethod()
    def thirdMethod(self):
        # self.print("thirdMethod")
        self.third.activate()


class SimpleModule(DyModule):

    def __init__(self):
        # super(SimpleModule, self).__init__()
        self.first = DyBool(False)
        self.second = DyBool(False)
        self.third = DyBool(False)

        self.firstMethod()
        if self.first.get():
            self.secondMethod()
            if self.second.get():
                self.thirdMethod()
                if self.third.get():
                    self.ftvWorks()

    @staticmethod
    def print(message):
        Log.p(message)

    def ftvWorks(self):
        self.print("FTV Works!")

    def firstMethod(self):
        # self.print("firstMethod")
        self.first.set(True)

    def secondMethod(self):
        # self.print("secondMethod")
        self.second.set(True)

    def thirdMethod(self):
        # self.print("thirdMethod")
        self.third.set(True)

    # def __setattr__(self, key, value):
    #     return object.__setattr__(self, key, value)


if __name__ == '__main__':
    DyModule()

    repetitions = 1200

    Efficiency.check(DynamicModule, repetitions, "DynamicModule")
    Efficiency.check(SimpleDyModule, repetitions, "SimpleDyModule")
    Efficiency.check(SimpleModule, repetitions, "SimpleModule")

    # list_a = []
    # list_b = []
    # list_c = []
    #
    # decay_factor = []
    #
    # cycles = 1
    #
    # for i in range(cycles):
    #     list_a.append(Efficiency.check(DyModule, 1200, "DyModule"))
    #     list_b.append(Efficiency.check(SimpleDyModule, 1200, "SimpleDyModule"))
    #     list_c.append(Efficiency.check(SimpleModule, 1200, "SimpleModule"))
    #
    #     if list_c[-1] != 0:
    #         decay_factor.append(list_a[-1]/list_c[-1])
    #
    # A = sum(list_a)/len(list_a)
    # B = sum(list_b)/len(list_b)
    # C = sum(list_c)/len(list_c)
    #
    # decayFactor = None
    #
    # if len(decay_factor) != 0:
    #     decayFactor = sum(decay_factor)/len(decay_factor)
    #
    # Efficiency.printResult(A, "DyModule")
    # Efficiency.printResult(B, "SimpleDyModule")
    # Efficiency.printResult(C, "SimpleModule")
    #
    # print()
    # print("Decay Factor: " + str(round(decayFactor)))
    # print("Decay Cycles: " + str(len(decay_factor)))
