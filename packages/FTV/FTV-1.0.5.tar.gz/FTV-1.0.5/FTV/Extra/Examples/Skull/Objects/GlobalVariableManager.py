# class Env:
#     def __init__(self):
#         self.data = mp.Queue()
#
#     def sendUpdate(self, item):
#         self.data.put(item)
#         print(list(self.data._buffer))


class GVC:
    @classmethod
    def setup(cls):
        pass
        # cls.env = Env()
