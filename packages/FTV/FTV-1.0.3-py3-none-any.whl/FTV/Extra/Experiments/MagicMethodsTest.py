class Int(object):
    def __init__(self, value: int=None):
        super(Int, self).__init__()
        self.__value__: int = value
        self.__name__: str = "__name__"

    def set(self, value):
        self.__value__ = value

    def get(self):
        return self.__value__

    def __add__(self, other):
        return int.__add__(self.get(), other + 0)

    def __radd__(self, other):
        return int.__radd__(self.get(), other)


if __name__ == '__main__':
    a = Int(5)
    b = Int(2)

    # a = array([5])
    # b = array([2])

    print(a + a)
