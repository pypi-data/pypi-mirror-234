import abc
import time
from datetime import datetime

from ticktick.oauth2 import OAuth2        # OAuth2 Manager
from ticktick.api import TickTickClient   # Main Interface

from FTV.Tools.Log import Log


class Calendar(object):
    @abc.abstractmethod
    def login(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def create(self, event: dict, folder: str=None):
        pass

    @abc.abstractmethod
    def update(self, event: dict, folder: str=None):
        pass

    @abc.abstractmethod
    def isExist(self, event: dict):
        pass

    @abc.abstractmethod
    def delete(self, event: dict = None, event_id=None):
        pass


class CustomTickTickClient(TickTickClient):
    def get(self, url, **kwargs):
        res = None

        for _ in range(5):
            try:
                res = self._session.get(url, **kwargs)
                break
            except Exception:
                time.sleep(10)
                Log.e("Trying again...")

        if res is None:
            return False

        return res

    def post(self, url, **kwargs):
        res = None

        for _ in range(5):
            try:
                res = self._session.post(url, **kwargs)
                break
            except Exception:
                time.sleep(10)
                Log.e("Trying again...")

        if res is None:
            return False

        return res

    def get_by_path(self, path, **kwargs):
        location_list = [item.strip() for item in path.split("/") if item.strip()]
        parent = None

        for directory in location_list:
            item_data = self.get_by_fields(name=directory, **kwargs)
            if not isinstance(item_data, list):
                item_data = [item_data]

            # lahav This mechanism should be improved.
            for item in item_data:
                if "groupId" in item.keys() and self.get_by_id(item["groupId"]) is not None:
                    if self.get_by_id(item["groupId"])["name"] == parent["name"]:
                        parent = item
                        break
                elif parent is None:
                    parent = item

        return parent

    def filter_projects(self, **kwargs):
        res = self.get('https://api.ticktick.com/open/v1/project/', headers=self.HEADERS)
        objects = res.json()

        filtered_objects = []

        for key, value in kwargs.items():
            filtered_objects += [item for item in objects if item[key] in value]

        return filtered_objects

    def filter_tasks(self, project_id, **kwargs):
        res = self.get(f'https://api.ticktick.com/open/v1/project/{project_id}/data', headers=self.HEADERS)
        objects = res.json()["tasks"]

        filtered_objects = []

        if not kwargs:
            return objects

        for key, value in kwargs.items():
            filtered_objects += [item for item in objects if item[key] in value]

        return filtered_objects

    def create_task(self, task):
        return self.post(f'https://api.ticktick.com/open/v1/task', json=task, headers=self.HEADERS)

    def update_task(self, task):
        return self.post(f'https://api.ticktick.com/open/v1/task/{task["id"]}', json=task, headers=self.HEADERS)


class TickTick(Calendar):

    def __init__(self, username, password):
        self.client: CustomTickTickClient
        self.username = username
        self.password = password

    def login(self):
        auth_client = OAuth2(client_id="rB4A6LTJZBm5O358tm",
                             client_secret="2#57O$ejC$0Nr1Cdb%o34E^sXayNjZ8a",
                             redirect_uri="http://127.0.0.1:8080",
                             cache_path=f"ticktick-tokens/{self.username}")

        self.client = CustomTickTickClient(self.username, self.password, auth_client)

    def create(self, event: dict, folder: str=None):
        return self.client.create_task(self._generateTask(event, folder))

    def update(self, event: dict, folder: str=None):
        new_task = self._getTask(event, folder).copy()
        new_task.update(self._generateTask(event, folder))
        return self.client.update_task(new_task)

    def isExist(self, task: dict, folder: str=None):
        return bool(self._getTask(task, folder))

    def _getTask(self, task: dict, folder: str=None) -> dict:
        if folder is not None:
            project = self.getProject(folder)

            non_completed_res = self.client.filter_tasks(project["id"])
            if isinstance(non_completed_res, dict):
                non_completed_res = [non_completed_res]

            res = [item for item in non_completed_res if item["status"] != 0]
            # res = self.client.task.get_completed(
            #     datetime.now() - timedelta(days=30),
            #     datetime.now() + timedelta(days=30)
            # )
            if isinstance(res, dict):
                res = [res]

            res += non_completed_res
            res = [item for item in res if item["title"] == task["title"]]
            if res:
                return res[0]
            else:
                return {}

        return self.client.get_by_fields(content=task["url"])

    def _getTaskId(self, task: dict, folder: str=None):
        return self._getTask(task, folder)["id"]

    def getProject(self, path):
        return self.client.filter_projects(name=path)[0]

    @staticmethod
    def formatDateTime(date, time, addition=0):
        date_list = [int(item) for item in date.split("/")]
        date_list.reverse()
        date_list += [int(item) for item in time.split(":")]
        date_list[-1] += addition
        if all(item == 0 for item in date_list[:-3:-1]):
            date_list[-2] = 23
            date_list[-1] = 59

        full_date = datetime(*date_list)
        return full_date

    def _generateTask(self, event: dict, folder: str, timezone="Asia/Jerusalem"):
        title = event["title"]
        description = event["description"]
        date = event["date"]
        time = event["time"]
        duration = event["duration"]
        due_date = event["end_time"]

        all_day = False
        if "all_day" in event.keys():
            all_day = event["all_day"]

        priority = 1
        if "priority" in event.keys():
            priority = event["priority"]

        start_date = TickTick.formatDateTime(date, time)
        due_date = TickTick.formatDateTime(date, due_date)

        task = self.client.task.builder(
            title=title,
            content=description,
            priority=priority,
            allDay=all_day,
            startDate=start_date,
            dueDate=due_date,
            sortOrder=12345,
            projectId=self.getProject(folder)["id"],
            timeZone=timezone
        )
        return task

    @staticmethod
    def formatDateTime(date, time, addition=0):
        input_format = '%d/%m/%Y %H:%M'
        output_format = '%Y %m %d %H %M'

        dt = datetime.strptime(f"{date} {time}", input_format)
        date_list = [int(item) for item in dt.strftime(output_format).split(" ")]

        full_date = datetime(*date_list)
        return full_date

    def filterTasks(self, local_data, task, local_key="url", task_key="url"):
        return [local_task for local_task in local_data if local_task[local_key].strip().strip("/") == task[task_key].strip().strip("/")]

    def isTaskChanged(self, local_task, task):
        comparison_keys = ("title", "startDate", "endDate")
        for comparison_key in comparison_keys:
            if local_task[comparison_key].strip() != task[comparison_key].strip():
                return True
        return False


class GoogleCalendar(Calendar):
    pass
