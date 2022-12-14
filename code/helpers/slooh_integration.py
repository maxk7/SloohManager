import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import yaml
from time import sleep

from mission import Mission
from schedule import Schedule

# Paths for mission schedule
path_to_mission = '//*[@id="app"]/div/section/div/div/div/div/div[1]/div/div[8]/div/div/div[1]/div[4]'
path_to_advanced = '//*[@id="app"]/div/section/div/div/div/div/div[1]/div/div[8]/div/div/div[1]/div[6]'
path_to_recent = '//*[@id="app"]/div/section/div/div/div/div/div[1]/div/div[8]/div/div/div[1]/div[8]'

# Path for telescope availibility

path_to_telescopes = '//*[@id="app"]/div/nav/div/div/div/div[2]/div/div/div[2]/ul'


def base_xpath_to_mission_list(base_path):
    rlist = []
    mission_index = 1

    while True:
        mission_xpath = base_path + f'/div[{mission_index}]'

        try:
            driver.find_element(By.XPATH, mission_xpath)
        except selenium.common.exceptions.NoSuchElementException:
            if mission_index == 1:
                print("no mission found in topic")
            break  # reached the end of the mission schedule

        mission_target = driver.find_element(By.XPATH, mission_xpath + '/div[1]/h4').text
        mission_time = driver.find_element(By.XPATH, mission_xpath + '/div[2]/h4').text
        mission_telescope = driver.find_element(By.XPATH, mission_xpath + '/div[2]/div/h4').text

        # Now find specific characteristics for missions in 'Recent Missions' Panel
        mission_message = None  # assume missions had no completion status yet

        try:
            # Test is the missions have a status
            mission_message = driver.find_element(By.XPATH, mission_xpath + '/div[2]/div/div/h4').text
        except:
            pass  # the mission is not in the 'Recent Missions' category

        mission_status = mission_message

        selected_mission_obj = Mission(mission_target, mission_time, mission_telescope, 'normal', mission_status)

        rlist.append(selected_mission_obj)
        mission_index += 1

    return rlist


def fetch_telescope_availability(base_path=path_to_telescopes):
    # first click the button that shows the telescope dashboard
    driver.find_element(By.XPATH, '//*[@id="app"]/div/nav/div/div/div/div[1]/div/div[1]/ul/li[3]/div/button').click()

    sleep(0.15)

    rdict = {}
    scope_index = 1

    while True:
        scope_xpath_name = base_path + f'/li[{scope_index}]/a/div/div[1]/div[1]'
        scope_is_online = base_path + f'/li[{scope_index}]/a/div/div[2]/div[1]'
        scope_xpath_text = base_path + f'/li[{scope_index}]/a/div/div[1]/div[2]'

        try:
            driver.find_element(By.XPATH, scope_xpath_text)
        except selenium.common.exceptions.NoSuchElementException:
            if scope_index == 1:
                print("telescope not found by xpath")
            break  # reached the end of the mission schedule

        telescope_name = driver.find_element(By.XPATH, scope_xpath_name).text
        telescope_online_status = driver.find_element(By.XPATH, scope_is_online).get_attribute("class")
        telescope_status_message = driver.find_element(By.XPATH, scope_xpath_text).text

        if "is-online" in telescope_online_status:
            telescope_status_message = "[ONLINE] " + telescope_status_message

        rdict[telescope_name] = telescope_status_message
        scope_index += 1

    return rdict


def build_schedule_fetch_telescopes():
    global driver

    # Import Credentials
    credentials = yaml.safe_load(open("../credentials.yml"))
    slooh_username = credentials["slooh"]["username"]
    slooh_password = credentials["slooh"]["password"]

    # Set up headless selenium
    options = Options()
    options.headless = True
    options.page_load_strategy = "none"
    driver = webdriver.Chrome(options=options)

    # Load the Slooh login page
    driver.get("https://app.slooh.com/NewDashboard")

    # wait for page elements to load
    while True:
        try:
            submit = driver.find_element(By.CLASS_NAME, "login-btn")
            print("[✔] page loaded")
            break
        except:
            pass

    # Load login elements and automatically fill the elements in
    username = driver.find_element(By.NAME, "username")
    password = driver.find_element(By.NAME, "pwd")

    username.send_keys(slooh_username)
    password.send_keys(slooh_password)
    submit.click()

    print("[✔] successfully logged in")

    sleep(5)

    # Actual process of building the schedule
    mission_list = base_xpath_to_mission_list(path_to_mission)
    advanced_mission_list = base_xpath_to_mission_list(path_to_advanced)
    recent_missions = base_xpath_to_mission_list(path_to_recent)

    telescope_availability = fetch_telescope_availability()  # get updated telescope information

    driver.close()

    return Schedule(mission_list, advanced_mission_list, recent_missions), telescope_availability
