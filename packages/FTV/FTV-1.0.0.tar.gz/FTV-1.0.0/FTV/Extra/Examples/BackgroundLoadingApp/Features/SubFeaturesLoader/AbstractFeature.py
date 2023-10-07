import abc
import time

from FTV.FrameWork.Features import UIFeature


class AbstractFeature(UIFeature):
    @abc.abstractmethod
    def setupSettings(self):
        pass

    @abc.abstractmethod
    def setupManagers(self):
        pass

    def setupTriggers(self):
        # pass
        time.sleep(1)
