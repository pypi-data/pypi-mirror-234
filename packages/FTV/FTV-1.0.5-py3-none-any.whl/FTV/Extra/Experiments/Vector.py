from math import atan, pi, sqrt, pow, sin, cos
from time import time


class Link:
    def __init__(self, feature, trigger, method):
        self.feature = feature
        self.trigger = trigger()
        self.method = method

    @staticmethod
    def get_var_by_id(id):
        return [x for x in globals().values() if id(x) == id]


class TM:
    links = {}
    preventLoop = False

    def __init__(self):
        pass

    @classmethod
    def add_trigger(cls, variable, trigger, method):
        cls.links[id(variable)] = Link(cls, trigger, method)

    @classmethod
    def rename_key(cls, old_id, new_id):
        if old_id == new_id:
            return
        link = cls.links[old_id]
        del cls.links[old_id]
        cls.links[new_id] = link


class LM:
    _debugging_mode = False

    def __init__(self):
        self.set_options()

    def set_options(self):
        self.set_debugging_mode(True)

    @classmethod
    def set_debugging_mode(cls, mode):
        cls._debugging_mode = mode

    @classmethod
    def print(cls, message):
        if cls._debugging_mode:
            print(message)


class VP:
    _forbidden = ("_hold", "_current_key", "_current_value")

    def __init__(self):
        self._hold = False
        self._current_key = None
        self._current_value = None

    def __setattr__(self, key, value):
        if key in self._forbidden:
            super().__setattr__(key, value)
            return
        if self._hold:
            self._current_key = key
            self._current_value = value
            super().__setattr__(key, value)
            return
        if key in dir(self):
            old_var = getattr(self, key)
            old_var_id = id(old_var)
            super().__setattr__(key, value)
            new_var = getattr(self, key)
            new_var_id = id(new_var)
            if old_var_id in TM.links:
                TM.rename_key(old_var_id, new_var_id)
                link = TM.links[new_var_id]
                link.trigger.set_args(old_var, new_var)
                if link.trigger():
                    # print("Change: " + str(key) + " = " + str(value))
                    link.method()

        super().__setattr__(key, value)

    def add_trigger(self, variable, trigger, method):
        TM.add_trigger(variable, trigger, method)

    def set_triggers(self):
        pass

    def print(self, message):
        LM.print(message)

    def hold(self):
        self._hold = True

    def release(self):
        self._hold = False
        self.__setattr__(self._current_key, self._current_value)


class Trigger:
    def __call__(self, *args, **kwargs):
        return self.condition()

    def set_args(self, old_var, new_var):
        self.old_var = old_var
        self.new_var = new_var

    def condition(self):
        return False


class FloatChanged(Trigger):
    def condition(self):
        return self.new_var != self.old_var


class MultipleFloatsChanged(FloatChanged):
    def condition(self):
        return self.new_var != self.old_var


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.update_r()
        self.update_theta()

    def move_x_steps(self, x):
        self.x += x

    def move_y_steps(self, y):
        self.y += y

    def update_theta(self):
        self.theta = atan(self.y / self.x) * 180 / pi

    def update_r(self):
        self.r = sqrt(pow(self.x, 2) + pow(self.y, 2))

    def update_r_and_theta(self):
        self.update_theta()
        self.update_r()

    def update_x(self):
        self.x = self.r*cos(self.theta * pi / 180)

    def update_y(self):
        self.y = self.r*sin(self.theta * pi / 180)

    def update_x_and_y(self):
        self.update_x()
        self.update_y()


class CustomVector(Vector, VP):
    def __init__(self, x, y):
        VP.__init__(self)
        Vector.__init__(self, x, y)

    def update_r_and_theta(self):
        self.hold()
        super(CustomVector, self).update_r_and_theta()
        self.print("\ttheta = " + str(self.theta))
        self.print("\tr = " + str(self.r))
        self.release()

    def update_x_and_y(self):
        self.hold()
        super(CustomVector, self).update_x_and_y()
        self.print("\tx = " + str(self.x))
        self.print("\ty = " + str(self.y))
        self.release()


class VM(VP):
    vector = CustomVector(3, 4)

    def set_triggers(self):
        self.add_trigger(self.vector.x, FloatChanged, self.vector.update_r_and_theta)
        self.add_trigger(self.vector.y, FloatChanged, self.vector.update_r_and_theta)
        # self.addTrigger(self.vector.r, FloatChanged, self.vector.update_x_and_y)
        # self.addTrigger(self.vector.theta, FloatChanged, self.vector.update_x_and_y)


class FW:
    tm = None
    vm = None
    lm = None

    def __init__(self):
        self.set_managers()
        self.vm.set_triggers()

    def set_managers(self):
        pass

    def set_trigger_manager(self, tm):
        self.tm = tm()

    def set_variable_manager(self, vm):
        self.vm = vm()

    def set_log_manager(self, lm):
        self.lm = lm()


class App(FW):
    def __init__(self):
        super().__init__()

        start = time()
        self.my_actions()
        end = time()

        total_time = (end - start)
        time_per_action = total_time / 1000 / 8
        print("Total time: " + str(total_time))
        print("Time per action: " + str(time_per_action))

    def set_managers(self):
        self.set_trigger_manager(TM)
        self.set_variable_manager(VM)
        self.set_log_manager(LM)

    def my_actions(self):
        for k in range(1, 1 + 1):
            self.vm.vector.x = k
            self.vm.vector.y = k


App()
