class Feature:
    ui_platform = None

    def __init__(self):
        self.setSettings()
        self.init()

    def init(self):
        pass

    def setSettings(self):
        pass

    @classmethod
    def setUIPlatform(cls, ui_platform):
        cls.ui_platform = ui_platform
