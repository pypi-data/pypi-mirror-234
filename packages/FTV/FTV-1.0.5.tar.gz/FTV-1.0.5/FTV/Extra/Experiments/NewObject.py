class A(object):
    def __new__(cls, *args, **kwargs):
        print("lahav")
        return super(A, cls).__new__(cls)


a = A()
b = A()
a = A()
