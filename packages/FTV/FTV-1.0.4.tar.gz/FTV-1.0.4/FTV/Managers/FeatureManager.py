from FTV.Managers.AbstractManager import AbstractManager
from FTV.Objects.Variables.DynamicIterators import DyFloatList


class FeatureManager(AbstractManager):
    __short_name__ = "FM"
    # features = []

    def __init__(self, _is_parent_app=None):
        super().__init__(_is_parent_app=_is_parent_app)
        self.init()

    def init(self):
        pass

    def _setupBuiltinVariables(self):
        super(FeatureManager, self)._setupBuiltinVariables()
        self.features = []
        self.loading_progress = DyFloatList(0, builtin=True)

    def setupFeatures(self):
        pass

    def addFeatures(self, *features):
        for feature in features:
            feature = feature()
            if feature.settings.enabled:
                feature._startSetupEnvironment()
                self.features.append(feature)

    def addFeature(self, feature):
        self.addFeatures(feature)

    def _resumeSetupFeatures(self):
        self.loading_progress.add(*[feature.fm.loading_progress for feature in self.features])

        for feature in self.features:
            feature._resumeSetupEnvironment()
            feature.fm.loading_progress.set(1)

    def setupSettings(self):
        pass
