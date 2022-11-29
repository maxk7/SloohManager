import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import yaml
from time import sleep

from mission import Mission
from schedule import Schedule

# Build mission schedule
path_to_mission = '//*[@id="app"]/div/section/div/div/div/div/div[1]/div/div[8]/div/div/div[1]/div[4]'
path_to_advanced = '//*[@id="app"]/div/section/div/div/div/div/div[1]/div/div[8]/div/div/div[1]/div[6]'


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
        selected_mission_obj = Mission(mission_target, mission_time, mission_telescope, 'normal')

        rlist.append(selected_mission_obj)
        mission_index += 1

    return rlist


def build_schedule():
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

    driver.close()

    return Schedule(mission_list, advanced_mission_list)
