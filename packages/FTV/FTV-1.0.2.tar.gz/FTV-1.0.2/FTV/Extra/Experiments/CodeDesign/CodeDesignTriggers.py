from FTV.Objects.Variables.DynamicObjects import *


class Module(DyModule):

    def setupVariables(self):
        self.dy_object_or_method = DyBool(False)
        self.b = DyBool(False)
        self.onSwitch = DySwitch()

    def setupTriggers(self):
        self.addTrigger(self.dy_object_or_method)\
            .setCondition(condition=DyObject.IsChanged, *args, **kwargs)\
            .setAction(action=self.dy_object_or_method, *args, **kwargs)\
            .setThread(thread=self.threads.main)

    @DyMethod()
    def printFinish(self):
        Log.p("finish")


if __name__ == '__main__':
    Module()

