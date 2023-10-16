class MathPuzzle:
    def __init__(self):
        self.a = []
        self.init_m = []
        self.k = 3

    def setList(self, *a):
        self.a = list(a)
        self.k = len(self.a)
        assert self.k > 1
        self.__updateInitM()

    def __updateInitM(self):
        self.init_m.append((self.a.pop(0) + self.a.pop(0))/2)
        self.init_m += self.a
        self.a.clear()

    def m(self, n):
        if n < 0:
            return self.init_m[-n-1]

        return (self.m(n-1) + self.m(n+1-self.k)) / 2

math = MathPuzzle()
math.setList(1, 3, 5, 7, 9, 11, 13)
print(math.m(20))
