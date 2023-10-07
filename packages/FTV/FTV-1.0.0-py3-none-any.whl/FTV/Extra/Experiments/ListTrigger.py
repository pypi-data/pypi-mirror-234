class VM:
    list = []

    def __init__(self):
        self.list = [5]

    def __setattr__(self, key, value):
        super().__setattr__(key, value)
        print("Change")


vm = VM()
# print(vm.list)
