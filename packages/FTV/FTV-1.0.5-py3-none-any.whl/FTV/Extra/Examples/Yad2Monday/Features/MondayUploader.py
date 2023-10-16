import json

import geocoder
from monday import MondayClient

from FTV.Extra.Examples.Yad2Monday import DATA_DIR
from FTV.Extra.Examples.Yad2Monday import Json
from FTV.FrameWork.Features import NIFeature
from FTV.Tools.Log import Log
from FTV.Managers.VariableManager import VariableManager
from FTV.Objects.Variables.DynamicMethods import DyMethod
from FTV.Objects.Variables.DynamicObjects import DySwitch


class VM(VariableManager):
    def setupVariables(self):
        from FTV.Extra.Examples.Yad2Monday.Yad2App import Yad2App

        self.houses = Yad2App.vm.houses
        self.collectors = []

        self.column_ids = {
            "מיקום": "dup__of______5",
            "קישור": "link",
            'שכ"ד': "dup__of_additional_monthly_fee",
            "ועד בית (לחודש)": "dup__of_base_rent",
            "ארנונה לחודשיים": "numeric0",
            'שכ"ד כולל': "numeric",
            "מ\"ר בנוי": "numbers7"
        }

        self.onUploaderReady = DySwitch()
        self.onUploaderCompleted = DySwitch()

    def setupTriggers(self):
        pass


class MondayUploader(NIFeature):
    def setupSettings(self):
        self.settings.setEnabled()

    def setupManagers(self):
        self.setVariableManager(VM)

    def setupTriggers(self):
        from FTV.Extra.Examples.Yad2Monday.Yad2App import Yad2App

        # self.addTrigger(Yad2App.vm.START).setAction(self.vm.onUploaderReady)

        # Upload
        self.addTrigger(Yad2App.vm.onReadyToUploadToMonday).setAction(self.vm.onUploaderReady)
        self.addTrigger(self.vm.onUploaderReady).setAction(self.uploadToMonday)
        self.addTrigger(self.uploadToMonday).setAction(self.vm.onUploaderCompleted)

        # Upload completed
        self.addTrigger(self.vm.onUploaderCompleted).setAction(Yad2App.vm.onUploadToMondayCompleted)

    @DyMethod()
    def uploadToMonday(self):

        file_path = DATA_DIR + "houses.json"
        houses = Json.read(file_path)

        self.setupAPI()
        self.setupGeo()

        # houses = Yad2App.vm.houses.get()
        houses = Json.read(DATA_DIR + "houses.json")

        houses = self.formatHouses(houses)
        # Log.json(houses)

        group_name = "Optional"
        self.group_id = self.getGroupId(group_name)

        for house in houses:
            # Check if house exists in Monday
            is_exists = self.checkIfExistsInMonday(house)
            house["is_updated"] = is_exists

            if house["is_updated"]:
                Log.p(f"House '{house['דירה']}' is already updated.")
                continue

            # Item name
            item_name = house["דירה"]

            # Prepare item data
            column_values = self.getColumnValues(house)

            # Modify link representation
            link = {
                "url": column_values["link"],
                "text": "Yad2"
            }
            column_values["link"] = link

            # # Modify Location
            # location_address = column_values["location4"]
            # lat, lng = self.getGeoFromAddress(location_address)
            # location = {
            #     "lat": lat,
            #     "lng": lng,
            #     "address": location_address
            # }
            # column_values["location4"] = location

            res = self.monday.items.create_item(board_id=str(self.board_id), group_id=self.group_id, item_name=item_name, column_values=column_values)

            if "error_code" in res.keys() and res["error_code"]:
                continue

            house["is_updated"] = True
            Log.p(f"House '{house['דירה']}' has been added successfully!")

        Json.write(file_path, houses)

    def setupAPI(self):
        # Replace with your API token and board ID
        self.api_token = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjI4MTcxNTk5OCwiYWFpIjoxMSwidWlkIjoyMjc4NjQxMiwiaWFkIjoiMjAyMy0wOS0xM1QyMzo1NTozMi45NTFaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6OTI3MDAwNCwicmduIjoidXNlMSJ9._PLXG4PkvKtqlV-KdjYdVbf_0GjQ0PxrVs5s-Y4jX5c"
        self.board_id = 5153901736
        self.monday = MondayClient(self.api_token)

        # Endpoint URL
        self.url = f"https://api.monday.com/v2/"

        # Headers with authentication
        self.headers = {
            "Authorization": self.api_token,
            "Content-Type": "application/json",
            # 'API-Version': '2023-10'
        }

    def checkIfExistsInMonday(self, house):
        from FTV.Extra.Examples.Yad2Monday.Features import HouseCollection

        items = self.getItemsFromMonday()
        house_link_id = HouseCollection.getHouseId(house, "קישור")
        item_Link_ids = []

        for i in range(len(items)):
            link_column = next(item for item in items[i]["column_values"] if self.vm.column_ids["קישור"] == item["id"])
            temp_link = link_column["value"]
            link = json.loads(temp_link)["url"]
            link_id = HouseCollection.getLinkId(link)
            item_Link_ids.append(link_id)

        return house_link_id in item_Link_ids

    def getItemsFromMonday(self):
        temp_groups = self.monday.groups.get_groups_by_board(self.board_id)["data"]["boards"][0]["groups"]
        group_ids = [item["id"] for item in temp_groups]

        all_items = []

        for group_id in group_ids:
            temp_items = self.monday.groups.get_items_by_group(self.board_id, group_id)
            items = temp_items["data"]["boards"][0]["groups"][0]["items"]
            item_ids = [int(item["id"]) for item in items]
            if item_ids:
                temp_items = self.monday.items.fetch_items_by_id(item_ids)
                items = temp_items["data"]["items"]

            all_items += items

        return all_items

    def getGroupId(self, group_name):
        res_data = self.monday.groups.get_groups_by_board(self.board_id)

        groups_data = res_data.get("data")
        groups = groups_data["boards"][0]["groups"]

        # Search for the group by name
        group_id = None
        for group in groups:
            if group.get("title") == group_name:
                group_id = group.get("id")
                break

        if group_id:
            return group_id
        else:
            Log.e(f"No group found with the name '{group_name}'.")

    def getColumnValues(self, house):
        return {_id: house[nick_name] for nick_name, _id in self.vm.column_ids.items() if nick_name in house.keys()}

    def formatHouses(self, houses):
        new_houses = []
        for house in houses:
            new_house = house.copy()

            # Get initial fee
            initial_fee_str = new_house['שכ"ד'] = house['שכ"ד'].split(" ")[0].replace(",", "")
            initial_fee = int(initial_fee_str)

            # Get essentials fee
            house_essentials_fee = 0
            key = 'ועד בית (לחודש)'
            if key in house.keys():
                del new_house[key]
                house_essentials_fee_str = house[key].split(" ")[0].replace(",", "")
                try:
                    house_essentials_fee = int(house_essentials_fee_str)
                    new_house[key] = house_essentials_fee_str
                except Exception:
                    pass

            # Get taxes fee
            house_taxes_fee = 0
            key = 'ארנונה לחודשיים'
            if key in house.keys():
                del new_house[key]
                house_taxes_fee_str = house[key].split(" ")[0].replace(",", "")
                try:
                    house_taxes_fee = int(house_taxes_fee_str)
                    new_house[key] = house_taxes_fee_str
                except Exception:
                    pass

            # Calculate for the overall fee
            overall_fee = round(initial_fee + house_essentials_fee + (house_taxes_fee / 2))
            new_house['שכ"ד כולל'] = overall_fee

            # Add to the houses list
            new_houses.append(new_house)

        return new_houses

    def setupGeo(self):
        pass
        # self.geolocator = geocoder.opencage(address, language="he", key=None)

    def getGeoFromAddress(self, address):
        location = geocoder.opencage(address, language="he", key=None)
        return location.latlng

