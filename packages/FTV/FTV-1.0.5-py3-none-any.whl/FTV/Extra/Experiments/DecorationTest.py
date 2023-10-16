import wrapt


class Wrapper(wrapt.ObjectProxy):
    def __init__(self, wrapped):
        super(Wrapper, self).__init__(wrapped)
        wrapped.__triggers__ = []
        print(wrapped)

    @wrapt.decorator
    def __call__(self, *args, **kwargs):
        print("->")
        ans = self.__wrapped__(self, *args, **kwargs)
        print("<-")
        return ans

@wrapt.decorator
def pass_through(wrapped, instance, args, kwargs):
    print("->")
    ans = wrapped(*args, **kwargs)
    print("<-")
    return ans


class Deco(object):
    def __init__(self):
        # setattr(self.function, "__triggers__", [])
        self.function.__triggers__.append(1)
        self.function()

    @Wrapper
    def function(self):
        print("function()")
        print(self.function.__triggers__)

class Deco2(Deco):
    def __init__(self):
        self.deco = Deco()
        print("---------------")
        super(Deco2, self).__init__()
        # print(self.function.__triggers__)


# Deco()
# print("---------------")
Deco2()