from collections import deque


class Queue(object):
    def __init__(self):
        self.__list__ = deque()

    def clear(self):
        self.__list__.clear()

    def put_nowait(self, obj):
        self.__list__.append(obj)

    def get_nowait(self):
        return self.__list__.popleft()

    def empty(self):
        return not self.__list__

    @property
    def queue(self):
        return self.__list__

    def __len__(self):
        return self.__list__.__len__()

    def __iter__(self):
        return self.__list__.__iter__()
