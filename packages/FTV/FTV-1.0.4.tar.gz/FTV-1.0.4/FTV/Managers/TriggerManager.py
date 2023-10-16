from FTV.Managers.Log import Log
from FTV.Objects.Variables.DynamicObjects import DyObject


class TriggerManager:
    setter_links = {}
    getter_links = {}
    # preventLoop = False
    is_add_trigger_active = False

    def __init__(self):
        pass

    @classmethod
    def addTrigger(cls, variable, trigger, action, thread_id=None):
        cls.setter_links[id(variable)] = cls.Link(cls, trigger, action, thread_id)

    @classmethod
    def checkTriggers(cls, variable: DyObject, new_value, old_value):
        triggered_links = []
        Log.d("links: {}".format(variable.__links__))
        for link in variable.__links__:
            if link.trigger.condition():
                triggered_links.append(link)

        # if triggered_links:
        #     print()

        map(lambda _link: _link.runAction(), triggered_links)

    @classmethod
    def rename_key(cls, old_id, new_id):
        if old_id == new_id:
            return
        link = cls.setter_links[old_id]
        del cls.setter_links[old_id]
        cls.setter_links[new_id] = link

    class Link:
        def __init__(self, feature, trigger, action, thread_id):
            self.feature = feature
            self.trigger = trigger
            self.action = action
            self.thread_id = thread_id

        def runAction(self):
            self.feature.em.getThread(self.thread_id).start(self.action)

    @staticmethod
    class AddTriggerWrapper(object):
        def __init__(self, func):
            self.func = func

        def __call__(self, *args, **kwargs):
            TriggerManager.is_add_trigger_active = True
            Log.d("is_add_trigger_active: True")
            self.func(self, *args, **kwargs)
            Log.d("is_add_trigger_active: False")
            TriggerManager.is_add_trigger_active = False


def addTriggerWrapper(func):
    def wrapper(*args):
        Log.d("is_add_trigger_active: True")
        func(*args)
        Log.d("is_add_trigger_active: False")

    return wrapper
