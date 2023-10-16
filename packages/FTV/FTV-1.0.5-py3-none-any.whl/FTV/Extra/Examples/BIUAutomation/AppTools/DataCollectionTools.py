import abc
import json
import math
import time
from datetime import datetime, timedelta
from datetime import date as dt_date
from subprocess import CREATE_NO_WINDOW

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC

import requests
from bs4 import BeautifulSoup

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from FTV.Tools.Log import Log


class Collector(object):
    def __init__(self, username, password, website_url):
        self.username = username
        self.password = password
        self.website_url = website_url
        self.token = None
        self.driver: WebDriver = None

    @abc.abstractmethod
    def login(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def getEvents(self, *args, **kwargs):
        pass

    def find_element(self, by, value, timeout=30, post_wait=0):
        try:
            res = WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((by, value)))
            time.sleep(post_wait)
            return res
        except TimeoutException:
            Log.p("Loading took too much time!")


class Moodle(Collector):
    def login(self, url_ext, with_index=True):
        # Setup the driver
        options = webdriver.ChromeOptions()

        options.add_argument("--disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-user-media-security=true")

        self.driver: WebDriver = webdriver.Chrome(options=options)

        # Insert the email
        self.driver.get("https://lemida.biu.ac.il/auth/multioauth/login.php?userType=teacher")
        self.find_element(By.CLASS_NAME, "input").send_keys(self.username)
        self.find_element(By.ID, "idSIButton9").click()
        time.sleep(2)

        # Insert the password
        self.find_element(By.CLASS_NAME, "input").send_keys(self.password)
        self.find_element(By.ID, "idSIButton9").click()

        # Send SMS message
        self.find_element(By.CLASS_NAME, "table").click()
        # time.sleep(2)

        # Insert the code
        # self.driver.find_element(By.ID, "idChkBx_SAOTCC_TD").click()
        code = input("Type the code: ")
        self.find_element(By.ID, "idTxtBx_SAOTCC_OTC").send_keys(code)
        self.find_element(By.ID, "idSubmit_SAOTCC_Continue").click()
        time.sleep(2)

        self.find_element(By.ID, "page-site-index")
        self.updateCurrentHTML()

    def updateCurrentHTML(self):
        self.currentHTML = self.driver.page_source
        self.soup = BeautifulSoup(self.currentHTML, "html.parser")

    def getAllCourses(self):
        # li_elements = self.driver.find_element_by_id("main-navbar").find_element_by_class_name("navbar-collapse").find_elements_by_tag_name("li")
        li_elements = self.soup.find(id="main-navbar").find(class_="navbar-collapse").find_all(name="li")
        a_course_elements = next(item.find("ul").find_all("a") for item in li_elements if
             item.find(name="a") and "הקורסים שלי" in item.find(name="a").text)

        courses_data = [{"name": item.attrs["title"], "id": item.text, "link": item.attrs["href"]} for item in a_course_elements if item]
        return courses_data

    def getAllCoursesSchedule(self, coursesData, duration=30):
        for i in range(len(coursesData)):
            course = coursesData[i]
            link = course["link"]
            self.get(link)
            coursesData[i] = self.getCourseHomeworks(course, duration=duration)
        return coursesData

    def getCourseHomeworks(self, course, months=12, duration=30):
        [course.update({f"{item.split('-')[0]}id": item.split("-")[-1]}) for item in self.soup.find("body").attrs["class"] if
         item.startswith("course-") or item.startswith("category-")]
        link = course["link"].split("/course/")[0] + "/lib/ajax/service.php"
        # cookies = self.driver.get_cookies()

        course["events"] = []

        self.get(f"https://lemida.biu.ac.il/calendar/view.php?view=upcoming&course={course['courseid']}")

        if self.find_element(By.CLASS_NAME, "calendar-no-results", timeout=0) is not None:
            return course

        event_elements = self.driver.find_element(By.CLASS_NAME, "eventlist").find_elements(By.CLASS_NAME, "event")

        for event_element in event_elements:
            name = event_element.get_attribute("data-event-title").split("'")[1]
            raw_time = event_element.find_element(By.CLASS_NAME, "col-11").text
            date, end_time = raw_time.split(",")
            date = date.strip()
            end_time = end_time.strip()
            url = event_element.find_element(By.CLASS_NAME, "card-link").get_attribute("href").rsplit("&", 1)[0]

            if date == "מחר":
                date = "/".join(str(dt_date.today() + timedelta(days=1)).split("-")[::-1])

            event_item = {
                "date": date
            }

            end_time_digits = end_time.split(":")
            end_time_minutes = 60*int(end_time_digits[0]) + int(end_time_digits[1])

            if end_time_minutes == 0:
                event_item["date"] = self.addDaysToDate(date, -1)

            end_time_minutes = round(end_time_minutes/15)*15
            time_minutes = end_time_minutes - duration

            time_digits = [(time_minutes // 60) % 24, time_minutes % 60]
            time_digits = [str(item).rjust(2, '0') for item in time_digits]
            time = ":".join(time_digits)

            end_time_digits = [(end_time_minutes // 60) % 24, end_time_minutes % 60]
            end_time_digits = [str(item).rjust(2, '0') for item in end_time_digits]
            end_time = ":".join(end_time_digits)

            # print(time, end_time)
            event_item.update({
                "name": name,
                "time": time,
                "end_time": end_time,
                "url": url,
                "duration": duration
            })

            course["events"].append(event_item)

        return course

    @staticmethod
    def addDaysToDate(date, addition, _format="%d/%m/%Y"):
        return (datetime(*[int(item) for item in date.split("/")[::-1]]) + timedelta(days=addition)).strftime(_format)

    def get(self, link):
        self.driver.get(link)
        self.updateCurrentHTML()

    def post(self, link, json=None, params=None):
        res_item = self.driver.post(link, json=json, params=params)
        self.currentHTML = res_item.text
        self.soup = BeautifulSoup(self.currentHTML, "html.parser")
        return res_item

    def getEvents(self):
        all_events = []
        urls = []

        # Collect the homework data
        self.updateCurrentHTML()
        courses = self.getAllCoursesSchedule(self.getAllCourses(), duration=30)

        for course in reversed(courses):
            events = reversed(course["events"])
            for event in events:
                title_parts = event["name"].replace('"', "'").strip("'").split("'")
                title = f'{course["name"]} - {[item.replace("-", " ").strip() for item in title_parts][-1]}'
                url = event["url"]
                event["title"] = title
                event["description"] = url

                if not url or url in urls:
                    continue

                all_events.insert(0, event)
                urls.append(url)

        return all_events


class InBar(Collector):
    def login(self, url_ext, with_index=True):
        # Setup url

        index_suffix = ""
        if with_index:
            index_suffix = "index.php"

        url_req = f"{self.website_url}{url_ext}{index_suffix}" + "?ReturnUrl=/live/Main.aspx"

        # Setup the driver
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        # options.add_argument('--silent-debugger-extension-api')
        # options.add_argument("--disable-gpu")  # Disable GPU acceleration (useful for some systems)
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-user-media-security=true")

        service = Service()
        service.creation_flags = CREATE_NO_WINDOW

        self.driver: WebDriver = webdriver.Chrome(service=service, options=options)

        # Load login page
        self.driver.get(url_req)

        # Insert the username
        self.find_element(By.NAME, "edtUsername").send_keys(self.username)

        # Insert the password
        self.find_element(By.NAME, "edtPassword").send_keys(self.password)

        # Click the login button
        self.find_element(By.NAME, "btnLogin").click()

    def closeDialogMessage(self):
        try:
            dialog = self.find_element(By.CLASS_NAME, "ModalDialogFocus", timeout=1)
            dialogs = self.driver.find_elements(By.CLASS_NAME, "ModalDialogFocus")

            for dialog in dialogs:
                title_item = self.find_element(By.CLASS_NAME, "ModalDialogTop", timeout=1)

                if title_item is None:
                    continue

                try:
                    title = title_item.text.strip()
                except Exception:
                    continue

                if "הודעה" in title:
                    break

            try:
                button = dialog.find_element(By.CLASS_NAME, "buttons")
                button.click()
            except Exception:
                pass
        except TimeoutException:
            pass

    def registerCourse(self, course_code):
        # Go to course registration page
        url_req = f"{self.website_url}" + "live/CreateStudentWeeklySchedule.aspx"
        self.driver.get(url_req)

        # Close the dialog message
        self.closeDialogMessage()

        # Search for the course
        search_field = self.find_element(By.CLASS_NAME, "SearchByCourseCode").find_element(By.TAG_NAME, "input")
        try:
            search_field.send_keys(course_code + "\n")
        except Exception:
            pass

        # Close the dialog message
        self.find_element(By.CLASS_NAME, "ModalDialogFocus", timeout=5)
        self.closeDialogMessage()

        # Setup beautiful soup
        soup = BeautifulSoup(self.driver.page_source, "html.parser")

        # Find the relevant table by ID
        temp_table = soup.find(id="divLessons")

        # Find the table with the class name "GridView" within the temp_table
        table = temp_table.find(class_="GridView")

        # Extract header items
        header_items = table.find(class_="GridHeader").find_all("th")
        headers = [item.text for item in header_items][1:-1]

        # Extract rows
        rows = table.find_all(class_="GridRow")

        is_available_dict = {
            "0": False,
            "1": True
        }
        course_options = []

        for row in rows:
            row_items = row.find_all("td")
            items = [item.text.strip() for item in row_items if not item.has_attr("class") and not item.has_attr("width")][1:-2]
            is_available_str = row_items[-2].find("input")["value"]
            is_available = is_available_dict[is_available_str]
            items.append(is_available)
            option = dict(zip(headers, items))

            course_options.append(option)

        # Log.p("course_options:")
        # Log.json(course_options)

        # Register for courses
        available_course_index = None
        for i, item in enumerate(course_options):
            if item["פנוי"]:
                available_course_index = i
                break

        if available_course_index is None:
            Log.p(f"course {course_code}: Not available")
            return False

        Log.p(f"course {course_code}: Available")

        temp_table = self.driver.find_element(By.ID, "divLessons")
        table = temp_table.find_element(By.CLASS_NAME, "GridView")
        rows = table.find_elements(By.CLASS_NAME, "GridRow")
        row = rows[available_course_index]

        register_btn = row.find_element(By.TAG_NAME, "input")
        register_btn.click()

        # Accept the alert (press "OK")
        alert = self.driver.switch_to.alert

        if alert is not None:
            alert.accept()

        Log.p("\tRegistered :)")

        return True

    def getAllCourses(self):
        soup = BeautifulSoup(self.currentHTML, "html.parser")
        # li_elements = self.driver.find_element_by_id("main-navbar").find_element_by_class_name("navbar-collapse").find_elements_by_tag_name("li")
        li_elements = soup.find(id="main-navbar").find(class_="navbar-collapse").find_all(name="li")
        a_course_elements = next(item.find("ul").find_all("a") for item in li_elements if
             item.find(name="a") and "הקורסים שלי" in item.find(name="a").text)

        courses_data = [{"name": item.attrs["title"], "id": item.text, "link": item.attrs["href"]} for item in a_course_elements if item]
        return courses_data

    def getAllCoursesSchedule(self, coursesData, duration=30):
        for i in range(len(coursesData)):
            course = coursesData[i]
            link = course["link"]
            self.get(link)
            coursesData[i] = self.getCourseHomeworks(course, duration=duration)
        return coursesData

    def getCourseHomeworks(self, course, months=12, duration=30):
        [course.update({f"{item.split('-')[0]}id": item.split("-")[-1]}) for item in self.soup.find("body").attrs["class"] if
         item.startswith("course-") or item.startswith("category-")]
        link = course["link"].split("/course/")[0] + "/lib/ajax/service.php"
        # cookies = self.driver.get_cookies()
        current_datetime = datetime.now()
        year = current_datetime.year
        month = current_datetime.month
        day = current_datetime.day

        sesskey = self.currentHTML.split('"sesskey":')[-1].split(",")[0].strip().replace('"', "")

        req_body = []
        months = 12

        for i in range(months):
            updated_month = (month + i) % 12
            if updated_month == 0:
                updated_month = 12
            req_body.append({
                "methodname": "core_calendar_get_calendar_monthly_view",
                "index": i,
                "args": {
                    "year": int(math.floor(year + (month + i - 1)/12)),
                    "month": int(updated_month),
                    "courseid": int(course["courseid"]),
                    "categoryid": int(course["categoryid"]),
                    "includenavigation": True,
                    "mini": True,
                    "day": 1
                }
            })
            # 66077
            # 2976

        params = {
            "info": "core_calendar_get_calendar_monthly_view",
            "sesskey": sesskey,
        }

        link2 = f"{link}?sesskey={sesskey}&info={'core_calendar_get_calendar_monthly_view'}"
        # requests.post(link, data=req_body, params=params, cookies=cookies)


        # self.curSession.post(link, json=req_body, params=params).json()[0]

        # params = {
        #     "view": "month",
        #     "course": course["courseid"]
        # }

        # link = course["link"].replace("/course/", "/calendar/").split("?")[0]
        res_item = self.post(link, json=req_body, params=params)
        data_list = [item["data"] for item in res_item.json()]
        #
        # td_object_list = [item.find("tbody").find_all("td") for item in
        #               self.soup.find(id="block-region-side-post").find_all(attrs={"data-period": "month"})]
        # td_objects = []
        # [td_objects.__iadd__(item) for item in td_object_list]
        # a_objects = [item.find("a") for item in td_objects if item.find("a")]
        # dates = [item.parent.find("span").text for item in a_objects]

        days_list = [[day for day in item["days"] if day["events"]] for item in data_list[0]["weeks"]]
        days = []
        [days.__iadd__(item) for item in days_list]

        temp_list = [item["weeks"] for item in data_list]
        temps = []
        [temps.__iadd__(item) for item in temp_list]

        temp_list = [item["days"] for item in temps]
        temps = []
        [temps.__iadd__(item) for item in temp_list]

        days = [item for item in temps if item["events"]]

        course["events"] = []
        for day_item in days:
            date = day_item["daytitle"].split(",")[-1].strip()

            temp_day, temp_month, temp_year = [int(item) for item in date.split("/")]
            d = datetime(int(year), int(month), int(day))
            temp_d = datetime(temp_year, temp_month, temp_day)

            if temp_d < d:
                continue

            event_item = {
                "date": date
            }
            for event in day_item["events"]:
                end_time = None
                # print(f'formattedtime: {event["formattedtime"]}')
                formatted_time = event["formattedtime"].strip()

                if "span" in formatted_time:
                    formatted_time = formatted_time.split(">", 1)[-1].rsplit("<", 1)[0].strip()

                if len(formatted_time.split(":")) == 3:
                    time = formatted_time.split("<", 1)[0].strip()
                    end_time = formatted_time.rsplit(">", 1)[-1].strip()

                elif len(formatted_time) == 5 and formatted_time[2] == ":":
                    end_time = formatted_time
                    end_time_digits = end_time.split(":")
                    end_time_minutes = 60*int(end_time_digits[0]) + int(end_time_digits[1])

                    if end_time_minutes == 0:
                        event_item["date"] = self.addDaysToDate(date, -1)

                    end_time_minutes = round(end_time_minutes/15)*15
                    time_minutes = end_time_minutes - duration

                    time_digits = [(time_minutes // 60) % 24, time_minutes % 60]
                    time_digits = [str(item).rjust(2, '0') for item in time_digits]
                    time = ":".join(time_digits)

                    end_time_digits = [(end_time_minutes // 60) % 24, end_time_minutes % 60]
                    end_time_digits = [str(item).rjust(2, '0') for item in end_time_digits]
                    end_time = ":".join(end_time_digits)

                else:
                    raise Exception(f"Could not get the time and end_time of the event: {event['formattedtime']}")

                # print(time, end_time)
                event_item.update({
                    "name": event["name"],
                    "time": time,
                    "end_time": end_time,
                    "url": event["url"],
                    "duration": duration
                })

                course["events"].append(event_item)

        return course

    @staticmethod
    def addDaysToDate(date, addition, _format="%d/%m/%Y"):
        return (datetime(*[int(item) for item in date.split("/")[::-1]]) + timedelta(days=addition)).strftime(_format)

    def get(self, link, params=None):
        res_item = self.curSession.get(link, params=params)
        self.currentHTML = res_item.text
        self.soup = BeautifulSoup(self.currentHTML, "html.parser")
        return res_item

    def post(self, link, json=None, params=None):
        res_item = self.curSession.post(link, json=json, params=params)
        self.currentHTML = res_item.text
        self.soup = BeautifulSoup(self.currentHTML, "html.parser")
        return res_item

    def getEvents(self):
        all_events = []
        urls = []

        # Collect the homework data
        courses = self.getAllCoursesSchedule(self.getAllCourses(), duration=30)

        for course in reversed(courses):
            events = reversed(course["events"])
            for event in events:
                title_parts = event["name"].replace('"', "'").strip("'").split("'")
                title = f'{course["name"]} - {[item.replace("-", " ").strip() for item in title_parts][-1]}'
                url = event["url"]
                event["title"] = title
                event["description"] = url

                if not url or url in urls:
                    continue

                all_events.insert(0, event)
                urls.append(url)

        return all_events


class MoodleCalendar(Collector):
    def __init__(self, url):
        super().__init__(None, None, url)

    def login(self, *args, **kwargs):
        pass

    def changeEventsFormat(self, events: dict):
        new_events = []

        input_format = '%Y%m%dT%H%M%SZ'
        date_format = '%d/%m/%Y'
        time_format = '%H:%M'
        default_duration = 30
        timezone_offset = timedelta(hours=3)

        for event in events:
            new_event = {}

            dtstart = None
            dtend = None

            for key, value in event.items():
                key = key.lower()

                if key == "summary":
                    new_event["name"] = value.split("'")[1]

                elif key == "description":
                    new_event["description"] = value

                elif key == "dtstart":
                    # Parse the input timestamp string to a datetime object
                    dtstart = datetime.strptime(value, input_format) + timezone_offset
                    new_event["date"] = dtstart.strftime(date_format)
                    new_event["time"] = dtstart.strftime(time_format)

                elif key == "dtend":
                    # Parse the input timestamp string to a datetime object
                    dtend = datetime.strptime(value, input_format) + timezone_offset
                    new_event["end_time"] = dtend.strftime(time_format)

                elif key == "location":
                    new_event["course"] = value

            if dtstart is not None:
                if new_event["time"] == new_event["end_time"]:
                    dtend = dtstart + timedelta(minutes=default_duration)
                    new_event["end_time"] = dtend.strftime(time_format)
                    new_event["duration"] = default_duration

                else:
                    if dtend is not None:
                        dttemp = dtend - dtstart
                        new_event["duration"] = dttemp.minutes()

            new_event["title"] = f'{new_event["course"]} - {new_event["name"]}'
            new_event["url"] = ""

            new_events.append(new_event)

        return new_events

    def getEvents(self, *args, **kwargs):
        res = requests.get(self.website_url)
        raw_events = res.text
        raw_lines = raw_events.split("\r\n")
        lines = []

        skip_to_events = False

        for line in raw_lines:
            if not skip_to_events:
                if line.lower().startswith("begin:vevent"):
                    skip_to_events = True
                else:
                    continue

            if line.lower().startswith("begin:"):
                line = "{"
            elif line.lower().startswith("end:"):
                line = "},"
            else:
                line = line.replace("\\", "\\\\").replace("\t", "\\t").replace("\r", "\\r").replace("\n", "\\n")

                if ":" in line:
                    key, value = line.split(":", 1)
                    line = f"\"{key}\": \"{value}\","
                else:
                    lines[-1] = f"{lines[-1][:-2:]}\\n{line}\","
                    continue

            line = line.strip()

            lines.append(line)

        del lines[-1]
        lines[-1] = lines[-1].strip(",")

        events_dump = "".join(lines)
        events_dump = events_dump.replace(",}", "}")
        events_dump = f"[{events_dump}]"

        events = json.loads(events_dump)
        return self.changeEventsFormat(events)

if __name__ == '__main__':
    collector = Moodle(
        "username",
        "password",
        "https://lemida.biu.ac.il/"
    )
    collector.login("blocks/login_ldap/")
    events = collector.getEvents()
    [print(item) for item in events]

