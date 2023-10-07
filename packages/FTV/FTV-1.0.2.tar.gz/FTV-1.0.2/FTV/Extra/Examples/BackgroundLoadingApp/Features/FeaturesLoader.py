from FTV.FrameWork.Features import NIFeature
from FTV.Managers.FeatureManager import FeatureManager


class FM(FeatureManager):
    def setupFeatures(self):
        from FTV.Extra.Examples.BackgroundLoadingApp.Features.SubFeaturesLoader import Feature1
        from FTV.Extra.Examples.BackgroundLoadingApp.Features.SubFeaturesLoader import Feature2
        from FTV.Extra.Examples.BackgroundLoadingApp.Features.SubFeaturesLoader import Feature3

        self.addFeatures(
            Feature1,
            Feature2,
            Feature3
        )

    def setupVariables(self):
        self.loading_progress.setBuiltin(False)


class FeaturesLoader(NIFeature):
    def setupSettings(self):
        self.settings.setEnabled()

    def setupManagers(self):
        self.setFeatureManager(FM)
