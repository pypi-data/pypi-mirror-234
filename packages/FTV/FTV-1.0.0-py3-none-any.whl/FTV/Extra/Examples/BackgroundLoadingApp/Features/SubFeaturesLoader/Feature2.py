from FTV.Extra.Examples.BackgroundLoadingApp.Features.SubFeaturesLoader import \
    AbstractFeature
from FTV.Managers.FeatureManager import FeatureManager


class FM(FeatureManager):
    def setupFeatures(self):
        from FTV.Extra.Examples.BackgroundLoadingApp.Features.SubFeaturesLoader.SubFeature2 import Feature2_1
        from FTV.Extra.Examples.BackgroundLoadingApp.Features.SubFeaturesLoader.SubFeature2 import Feature2_2
        from FTV.Extra.Examples.BackgroundLoadingApp.Features.SubFeaturesLoader.SubFeature2 import Feature2_3
        from FTV.Extra.Examples.BackgroundLoadingApp.Features.SubFeaturesLoader.SubFeature2 import Feature2_4

        self.addFeatures(
            Feature2_1,
            Feature2_2,
            Feature2_3,
            Feature2_4
        )


class Feature2(AbstractFeature):
    def setupSettings(self):
        pass
        # self.settings.setDisabled()

    def setupManagers(self):
        self.setFeatureManager(FM)

