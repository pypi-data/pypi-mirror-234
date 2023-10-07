

class Trigger:
    funcs = {}

    def __setattr__(self, key, value):
        if key != "__value__":
            if key in self.funcs.keys():
                print("event")
        super().__setattr__(key, value)

    @classmethod
    def add_func(cls, var_name, func):
        cls.funcs[var_name] = func


class TrIntIncreased(Trigger):
    def condition(self, old_var, new_var):
        return new_var > old_var


class TV:
    funcs = {}

    def __setattr__(self, key, value):
        if key in self.funcs.keys():
            print("event")
        super().__setattr__(key, value)

    @classmethod
    def add_func(cls, var_name, func):
        cls.funcs[var_name] = func

    @classmethod
    def add_trigger(cls, trigger: Trigger, func):
        cls.funcs[trigger] = func


class Int(int, TV):
    def __init__(self, value=None):
        super().__init__()
        self.__value__ = value

    def __repr__(self):
        return self.__value__


class VM:
    a = Int(0)

    def get_name(self):
        d = {v: k for k, v in globals().items()}
        return d[self]


class Feature:
    def __init__(self):
        VM.a.add_trigger(TrIntIncreased(), self.s_feature_2)

    def s_feature_1(self):
        VM.a += 1
        print("VM.a = ", VM.a)
        # print('C_two a=', self.trigger.obj)

    def s_feature_2(self):
        VM.a += 1
        print("VM.a = ", VM.a)
        # print('C_two a=', self.trigger.obj)


class Empty:
    child = 0


vm = VM()
feature = Feature()

# feature.s_feature_1()
