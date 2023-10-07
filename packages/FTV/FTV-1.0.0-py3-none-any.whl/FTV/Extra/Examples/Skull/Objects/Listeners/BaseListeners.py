import wrapt


def getSenderClasses(parent_class):
    if Sender in parent_class.__bases__:
        return [parent_class]

    classes = [item for item in parent_class.__bases__]

    res = []
    for cls in classes:
        sub_classes = [item for item in cls.__bases__]
        if Sender in sub_classes:
            res.append(cls)

    return res


def getReceiverClasses(parent_class):
    classes = [item for item in parent_class.__bases__]

    res = []
    for cls in classes:
        sub_classes = [item for item in cls.__bases__]
        if Receiver in sub_classes:
            res.append(cls)

    return res


def receiverToSenderClasses(classes):
    import Objects.Listeners.Senders as Senders

    res = []

    for cls in classes:
        cls_str = cls.__name__
        cls_sender_str = cls_str.removesuffix("Receiver") + "Sender"
        cls_sender = getattr(Senders, cls_sender_str)
        res.append(cls_sender)

    return res


def senderToReceiverClasses(classes):
    import Objects.Listeners.Receivers as Receivers

    res = []

    for cls in classes:
        cls_str = cls.__name__
        cls_sender_str = cls_str.removesuffix("Sender") + "Receiver"
        cls_sender = getattr(Receivers, cls_sender_str)
        res.append(cls_sender)

    return res


class sender:
    @wrapt.decorator
    def __call__(self, func, sender_instance, args, kwargs):
        # print(sender_instance.__class__)
        func(*args, **kwargs)
        # if func.__name__ == "onSendExamStarted":
        #     print()

        classes = getSenderClasses(sender_instance.__class__)
        # print(func.__name__)
        classes = senderToReceiverClasses(classes)
        for cls in classes:
            instances = Receiver.RECEIVERS[cls]
            for receiver_instance in instances:
                getattr(receiver_instance, func.__name__)(*args, **kwargs)


class Sender:
    def __init__(self, parent):
        # parent_cls = parent.__class__
        if "SENDERS" not in dir(parent):
            parent.SENDERS = []
        parent.SENDERS.append(self)


class Receiver:
    RECEIVERS = {}

    def setupListeners(self):
        classes = getReceiverClasses(self.__class__)
        # classes = receiverToSenderClasses(classes)
        for cls in classes:
            if cls not in self.RECEIVERS.keys():
                Receiver.RECEIVERS[cls] = []

            if self.__class__.__name__ not in [item.__class__.__name__ for item in self.RECEIVERS[cls]]:
                Receiver.RECEIVERS[cls].append(self)
