from FTV.Objects.SystemObjects.TriggerObjects import Condition


class DyObjectConditions:
    def __condition__(self, old_val, new_val, *args, **kwargs):
        return True

    class IsChanged(Condition):
        @staticmethod
        def __condition__(old_val, new_val, *args, **kwargs):
            return old_val != new_val

    class IsChangedTo(Condition):
        @staticmethod
        def __condition__(old_val, new_val, *args, **kwargs):
            if new_val == args[0]:
                return old_val != new_val
            return False


class DyNumericConditions(DyObjectConditions):

    class IsIncreased(Condition):
        @staticmethod
        def __condition__(old_val, new_val, *args, **kwargs):
            return old_val < new_val

    class IsDecreased(Condition):
        @staticmethod
        def __condition__(old_val, new_val, *args, **kwargs):
            return old_val > new_val

    class IsEqualTo(Condition):
        @staticmethod
        def __condition__(old_val, new_val, *args, **kwargs):
            return new_val == args[0]

    class IsNotEqualTo(Condition):
        @staticmethod
        def __condition__(old_val, new_val, *args, **kwargs):
            return new_val != args[0]

    class IsGraterEqualTo(Condition):
        @staticmethod
        def __condition__(old_val, new_val, *args, **kwargs):
            return new_val >= args[0]

    class IsLessEqualTo(Condition):
        @staticmethod
        def __condition__(old_val, new_val, *args, **kwargs):
            return new_val <= args[0]

    class IsGraterThan(Condition):
        @staticmethod
        def __condition__(old_val, new_val, *args, **kwargs):
            return new_val > args[0]

    class IsLessThan(Condition):
        @staticmethod
        def __condition__(old_val, new_val, *args, **kwargs):
            return new_val < args[0]


class DyIteratorConditions(DyObjectConditions):

    class IsIncreased(Condition):
        @staticmethod
        def __condition__(old_val, new_val, *args, **kwargs):
            return old_val < new_val

    class IsDecreased(Condition):
        @staticmethod
        def __condition__(old_val, new_val, *args, **kwargs):
            return old_val > new_val

    class IsEqualTo(Condition):
        @staticmethod
        def __condition__(old_val, new_val, *args, **kwargs):
            return new_val == args[0]

    class IsNotEqualTo(Condition):
        @staticmethod
        def __condition__(old_val, new_val, *args, **kwargs):
            return new_val != args[0]


class DyIntConditions(DyNumericConditions):
    pass


class DyBoolConditions(DyObjectConditions):
    def __condition__(self, old_val, new_val, *args, **kwargs):
        return new_val


class DyByteArrayConditions(DyIteratorConditions):
    pass


class DyBytesConditions(DyNumericConditions):
    pass


class DyComplexConditions(DyNumericConditions):
    pass


class DyDictConditions(DyIteratorConditions):
    pass


class DyFloatConditions(DyNumericConditions):
    pass


class DyListConditions(DyIteratorConditions):
    def __condition__(self, old_val, new_val, *args, **kwargs):
        return True

    class IsChanged(Condition):
        @staticmethod
        def __condition__(old_val, new_val, *args, **kwargs):
            return len(old_val) != len(new_val) or next((True for i, j in zip(old_val, new_val) if i != j), False)

    class IsChangedTo(Condition):
        @staticmethod
        def __condition__(old_val, new_val, *args, **kwargs):
            if not DyListConditions.IsChanged.__condition__(new_val, args[0]):
                return DyListConditions.IsChanged.__condition__(old_val, new_val)
            return False

    class IsEmpty(Condition):
        @staticmethod
        def __condition__(old_val, new_val, *args, **kwargs):
            return len(new_val) == 0

    class IsNotEmpty(Condition):
        @staticmethod
        def __condition__(old_val, new_val, *args, **kwargs):
            return len(new_val) != 0


class DySetConditions(DyIteratorConditions):
    pass


class DyStrConditions(DyObjectConditions):
    pass


class DyTupleConditions(DyIteratorConditions):
    pass
