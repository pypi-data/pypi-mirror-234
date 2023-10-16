from Examples.BackgroundLoadingApp.Features.SubFeaturesLoader.AbstractFeature import \
    AbstractFeature
from FTV.Managers.FeatureManager import FeatureManager


class FM(FeatureManager):
    def setupFeatures(self):
        from Examples.BackgroundLoadingApp.Features.SubFeaturesLoader.SubFeature2.Feature2_1 import \
            Feature2_1
        from Examples.BackgroundLoadingApp.Features.SubFeaturesLoader.SubFeature2.Feature2_2 import \
            Feature2_2
        from Examples.BackgroundLoadingApp.Features.SubFeaturesLoader.SubFeature2.Feature2_3 import \
            Feature2_3
        from Examples.BackgroundLoadingApp.Features.SubFeaturesLoader.SubFeature2.Feature2_4 import \
            Feature2_4

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

