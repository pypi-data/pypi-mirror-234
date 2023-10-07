from FTV.Extra.Examples.Yad2Monday import Yad2Website
from FTV.Extra.Examples.Yad2Monday import DATA_DIR
from FTV.Extra.Examples.Yad2Monday import Json
from FTV.FrameWork.Features import NIFeature
from FTV.Managers.VariableManager import VariableManager
from FTV.Objects.Variables.DynamicMethods import DyMethod
from FTV.Objects.Variables.DynamicObjects import DySwitch


class VM(VariableManager):
    def setupVariables(self):
        from FTV.Extra.Examples.Yad2Monday.Yad2App import Yad2App

        self.collectors = []
        self.houses = Yad2App.vm.houses

        self.collector = Yad2Website(
            "lahav.manage@gmail.com",
            "sYZEqt9Z8ddV@c",
            "https://www.yad2.co.il/",
            hidden=False
        )

        self.onCollectorLoginCompleted = DySwitch()
        self.onCollectorReadyToCollect = DySwitch()
        self.onCollectorGetLinksCompleted = DySwitch()
        self.onCollectorGetHousesCompleted = DySwitch()

    def setupTriggers(self):
        pass


class HouseCollection(NIFeature):
    def setupSettings(self):
        self.settings.setEnabled()

    def setupManagers(self):
        self.setVariableManager(VM)

    def setupTriggers(self):
        from FTV.Extra.Examples.Yad2Monday.Yad2App import Yad2App

        # Login
        self.addTrigger(Yad2App.vm.onReadyToCollect).setAction(self.collectorLogin)
        self.addTrigger(self.collectorLogin).setAction(self.vm.onCollectorLoginCompleted)

        # Collect links
        self.addTrigger(self.vm.onCollectorLoginCompleted).setAction(self.vm.onCollectorReadyToCollect)
        self.addTrigger(self.vm.onCollectorReadyToCollect).setAction(self.collectorGetLinks)
        self.addTrigger(self.collectorGetLinks).setAction(self.vm.onCollectorGetLinksCompleted)

        # Collect houses
        self.addTrigger(self.vm.onCollectorGetLinksCompleted).setAction(self.collectorGetHouses)
        self.addTrigger(self.collectorGetHouses).setAction(self.vm.onCollectorGetHousesCompleted)

        # Collection completed
        self.addTrigger(self.vm.onCollectorGetHousesCompleted).setAction(Yad2App.vm.onCollectionCompleted)

    @DyMethod()
    def collectorLogin(self):
        self.vm.collector.login("auth/login")

    @DyMethod()
    def collectorGetLinks(self):
        self.vm.collector.collectFavoriteLinks()

    @DyMethod()
    def collectorGetHouses(self):
        self.vm.houses += self.vm.collector.getHouses()
        self.updateHousesJson()

    @staticmethod
    def getHouseId(house, link_key):
        return HouseCollection.getLinkId(house[link_key])

    @staticmethod
    def getLinkId(link):
        link_id = link.split("open-item-id=")[-1].split("&", 1)[0]
        link_id = link_id.split("/item/")[-1]
        return link_id

    def getOpenItemIdsFromHouses(self, houses, key):
        return [self.getHouseId(item, key) for item in houses]

    def updateHousesJson(self):
        file_path = DATA_DIR + "houses.json"
        old_houses = Json.read(file_path)
        new_houses = self.vm.houses.get()

        old_open_item_ids = self.getOpenItemIdsFromHouses(old_houses, "קישור")
        new_open_item_ids = self.getOpenItemIdsFromHouses(new_houses, "קישור")

        really_new_item_ids = [item for item in new_open_item_ids if item not in old_open_item_ids]
        really_new_houses = [item for item in new_houses if self.getHouseId(item, "קישור") in really_new_item_ids]

        updated_houses = old_houses
        updated_houses += really_new_houses

        Json.write(file_path, updated_houses)
