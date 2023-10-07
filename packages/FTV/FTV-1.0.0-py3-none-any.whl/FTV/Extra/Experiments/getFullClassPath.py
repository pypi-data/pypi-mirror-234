class A:
    class B:
        class C:
            def me(self):
                print(str(repr(self)).split(" ", 1)[0][1:])


x = A.B.C()
x.me()
