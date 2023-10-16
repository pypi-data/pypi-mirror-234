import abc
import math
import time
from datetime import datetime, timedelta
from subprocess import CREATE_NO_WINDOW

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from FTV.Tools.Log import Log


class Collector(object):
    def __init__(self, username, password, website_url, hidden=True):
        self.username = username
        self.password = password
        self.website_url = website_url
        self.token = None
        self.driver: WebDriver = None
        self.hidden = hidden

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


class Yad2Website(Collector):
    def get(self, link):
        self.driver.get(link)
        self.currentHTML = self.driver.page_source
        self.soup = BeautifulSoup(self.currentHTML, "html.parser")

    def post(self, link, json=None, params=None):
        res_item = self.driver.post(link, json=json, params=params)
        self.currentHTML = res_item.text
        self.soup = BeautifulSoup(self.currentHTML, "html.parser")
        return res_item

    def login(self, url_ext):
        # Setup url

        url_req = f"{self.website_url}{url_ext}"

        # Setup the driver
        options = webdriver.ChromeOptions()
        if self.hidden:
            options.add_argument('--headless')
            options.add_experimental_option('excludeSwitches', ['enable-logging'])

        options.add_argument("--disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-user-media-security=true")

        service = Service()
        service.creation_flags = CREATE_NO_WINDOW

        self.driver: WebDriver = webdriver.Chrome(service=service, options=options)


        # Load login page
        self.driver.get(url_req)

        # # Add cookies
        # cookies = Json.read(DATA_DIR + "Yad2Cookies.json")
        # for cookie in cookies:
        #     try:
        #         self.driver.add_cookie(cookie)
        #         Log.p(f"cookie added: '{cookie['name']}'")
        #     except Exception:
        #         Log.p(f"cookie dismissed: '{cookie['name']}'")

        # Insert the username
        self.find_element(By.XPATH, '//input[@type="email"]').send_keys(self.username)

        # Insert the password
        self.find_element(By.XPATH, '//input[@type="password"]').send_keys(self.password)

        # Click the login button
        self.find_element(By.CLASS_NAME, "submit-and-errors").find_element(By.XPATH, '//button[@type="submit"]').click()

        # Wait until site loads
        self.find_element(By.TAG_NAME, "body")

    def collectFavoriteLinks(self):
        pass

    def getHouses(self):
        # Go to favorites
        favorites_url = "https://www.yad2.co.il/favorites"
        self.get(favorites_url)

        # Collect links
        self.links = []

        temp_favorite_items = self.find_element(By.CLASS_NAME, "favorite_items")
        temp_favorite_items = temp_favorite_items.find_element(By.CLASS_NAME, "category_items")
        favorite_items = temp_favorite_items.find_elements(By.CLASS_NAME, "item_favorite")

        # Close the alert
        try:
            self.find_element(By.CLASS_NAME, "tooltip_button").click()
        except Exception:
            pass

        self.houses = []
        urls = []

        for i, favorite_item in enumerate(favorite_items):
            try:
                # Open house link
                self._waitForFavoritesToLoad()
                # Try opening the link
                is_link_opened = False
                max_attempts = 5
                attemps = 0
                while not is_link_opened and attemps < max_attempts:
                    try:
                        favorite_item.click()
                        is_link_opened = True
                    except ElementClickInterceptedException:
                        time.sleep(0.2)
                        attemps += 1

                dialog = self.find_element(By.CLASS_NAME, "light_box_dialog_wrapper")
                self.find_element(By.CLASS_NAME, "lightbox_header")
                dialog = dialog.find_element(By.XPATH, '//section[@id="lightbox_education-content"]')
                dialog_html = dialog.get_attribute('outerHTML')

                # Collect page data
                house = self.htmlToJson(dialog_html)
                self.houses.append(house)

                # Close window
                temp_close_button = self.find_element(By.CLASS_NAME, "lightbox_header")
                close_button = temp_close_button.find_element(By.CLASS_NAME, "close_button")
                close_button.click()
            except Exception as e:
                Log.traceback()
                Log.e(f"Could not load item {i}", color=Log.color.RED)

        return self.houses

    def _waitForFavoritesToLoad(self):
        temp_favorite_items = self.find_element(By.CLASS_NAME, "favorite_items")
        temp_favorite_items = temp_favorite_items.find_element(By.CLASS_NAME, "category_items")
        favorite_items = temp_favorite_items.find_elements(By.CLASS_NAME, "item_favorite")

    def htmlToJson(self, html):
        # Parse the HTML using Beautiful Soup
        soup = BeautifulSoup(html, 'html.parser')

        # Find the section with id 'lightbox_education-content'
        section = soup.find('section', {'id': 'lightbox_education-content'})

        # Initialize a dictionary to store house data
        house = {}

        # Extract house information
        house['title'] = section.find('h3', {'class': 'title_madad_nadlan ad_about'}).text.strip()

        # Extract additional information about the property
        additional_info = section.find('div', {'class': 'show-more-contents bold-text'})
        if additional_info:
            house['additional_info'] = additional_info.text.strip()

        # Extract details about the property
        details = section.find_all('dl', {'class': 'item'})
        for detail in details:
            try:
                title = detail.find('dd', {'class': 'title'}).text.strip()
                value = detail.find('dt', {'class': 'value'}).text.strip()
                house[title] = value
            except Exception:
                pass

        # Extract features of the property
        features = section.find_all('div', {'class': 'info_feature'})
        for feature in features:
            feature_name = feature.find('span', {'class': 'title'}).text.strip()
            house[feature_name] = True

        # Add name
        main_title = self.find_element(By.CLASS_NAME, "main_title")
        house["דירה"] = main_title.text
        del house["title"]

        # Add location
        location = main_title.parent.find_element(By.CLASS_NAME, "description").text
        house['מיקום'] = location

        # Add price
        price = self.find_element(By.XPATH, '//strong[@class="price"]')
        house['שכ"ד'] = price.text

        # Add data
        children = list(section.find('div', {'class': 'details_wrapper'}).children)
        children = children[2:-2]
        for child in children:
            table_item = child.text.split("\n")
            key, value = [item.strip() for item in table_item if item.strip()]
            house[key] = value

        # Add link
        house["קישור"] = self.driver.current_url

        house["is_updated"] = False

        # Return the JSON object
        return house
