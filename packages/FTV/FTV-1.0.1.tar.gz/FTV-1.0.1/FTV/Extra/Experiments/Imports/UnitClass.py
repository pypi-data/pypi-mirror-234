class UnitClass(object):
    def __getattribute__(self, item):
        super(UnitClass, self).__getattribute__(item)
