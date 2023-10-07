from FTV.Extra.Experiments.Imports import UnitClass


class A(UnitClass):
    def __init__(self):
        print("init A")

    def __call__(self, *args, **kwargs):
        super(A, self).__call__(*args, **kwargs)
        self.__init__()

