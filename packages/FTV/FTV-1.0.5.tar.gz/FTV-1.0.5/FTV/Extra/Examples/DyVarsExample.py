from FTV.Tools.Log import Log
from FTV.Objects.Variables.DynamicMethods import DyMethod
from FTV.Objects.Variables.DynamicModules import DyModule
from FTV.Objects.Variables.DynamicObjects import DyFloat, DyStr, DyList, DyBool

if __name__ == '__main__':

    class VM(DyModule):
        def setupVariables(self):
            self.a = DyFloat(5)
            self.b = DyFloat(5)
            # self.com = DyComplex(10)

            self.c = DyStr("lahav {}")
            self.d = DyStr("svorai")

            self.e = DyList([1, 2, 3])
            self.f = DyList([4, 5, 6])

            self.g = DyBool(True)
            self.h = DyBool(False)

        def setupTriggers(self):
            self.addTrigger(self.POST_INIT).setAction(self.action)
            self.addTrigger(self.e).setCondition(DyList.IsChanged).setAction(self.ftvWorks)

        @DyMethod()
        def ftvWorks(self):
            Log.p("FTV works :)")

        @DyMethod()
        def action(self):
            # self.a += self.b
            # self.d += self.c

            # self.b % self.a

            # b += a

            # self.c *= self.a
            # self.c.set(self.d)

            # Log.p("a = {}".format(self.a))
            # Log.p("c = {}".format(self.c))
            # # Log.p("com = {}".format(self.com))
            # Log.p(type(self.a))
            # Log.p(type(self.c))
            # # ab = 5 if
            # Log.p(self.b and self.a)
            #
            # a = 5
            # a **= 7

            # self.a /= 3
            # import math
            # Log.p(math.trunc(self.a))
            #
            # Log.p(self.a)
            # Log.p(type(self.a))
            # Log.p(self.b)
            # Log.p(type(self.b))

            # self.c += self.d

            # Log.p("{}...".format(self.d))
            #
            # Log.p(self.c)
            # Log.p(type(self.c))
            # Log.p(self.d)
            # Log.p(type(self.d))

            self.e += self.f
            self.e.append(10)
            self.e.insert(3, 0)
            self.e.set([0, 0, 0])
            self.e.setItem(1, 2)
            self.e.sort()
            self.e.pop(1)
            self.e.reverse()
            self.e.clear()

            self.f += []

            #
            # Log.p(self.c in [4])
            #
            Log.p(f"self.e: {self.e}")
            Log.p(f"self.f: {self.f}")

            # self.g += self.h
            # Log.p(self.g and self.h)

            # Log.p(self.g)
            # Log.p(type(self.g))
            # Log.p(self.h)
            # Log.p(type(self.h))


    VM()