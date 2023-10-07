class VP:
    def __setattr__(self, key, value):
        super(VP, self).__setattr__(key, value)
        print(key, value)


class VM(VP):
    Name = "lahav"
    Age = 21


class Feature:

    def change_name(self):
        VM.Name = "Shani"

    def change_age(self):
        VM.Name = "Shani"


class FM:
    def __init__(self):
        self.features = []
        self.set_features()
        # self._init_features()

    def set_features(self):
        self.add_features(Feature)

    def add_features(self, *features):
        for feature in features:
            self.features.append(feature())

    def _init_features(self):
        for feature in self.features:
            feature()


class FW:
    TRIGGER_ALERT_1 = False
    fm: FM
    vm: VM

    def __init__(self):
        self.set_feature_manager(FM)
        self.set_variablee_manager(VM)
        self.my_actions()

    def set_feature_manager(self, fm):
        self.fm = fm()

    def set_variablee_manager(self, vm):
        self.vm = vm()

    def my_actions(self):
        VM.Name = "shani"


# FW()


class Child1:
    pass


class Child2:
    pass


class Variables:
    def __setattr__(self, key, value):
        super(Variables, self).__setattr__(key, value)
        print(key, value)


class VM:
    _vars = Variables()

    def __setattr__(self, key, value):
        setattr(self._vars, key, value)

    def create_variables(self):
        self.child_1 = "shahar"



Vm = VM.Main

vm = VM()
vm.child_1 = 5
Vm.child_1 = "lahav"
Vm.child_1 = "shani"
Vm.child_1 = "kfir"
Vm.child_1 = "ofer"
# Parent.Main.child_2 = "LAHAV"

# p_2 = Parent()
# p_2.child_1 = 20

# p_1.Main = 50

# p_2 = Parent()
