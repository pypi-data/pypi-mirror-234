class A(object):
  pass


class B(A):
  pass


b = B()


print(issubclass(b.__class__, A))
