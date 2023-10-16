class Test:
    def __init__(self):
        self.method2(self.method1)

    def method2(self, methodToRun):
        result = methodToRun()
        return result

    def method1(self):
        print('hello world')


test = Test()
