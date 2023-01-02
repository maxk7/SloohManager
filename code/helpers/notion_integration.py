import requests
import json
import yaml
from datetime import datetime, timedelta
from notion_errors import *
from notion_page import NotionPage

credentials = yaml.safe_load(open("../credentials.yml"))
token = credentials["notion"]["token"]

payload = {"page_size": 100}
headers = {
    "Authorization": "Bearer " + token,
    "accept": "application/json",
    "Notion-Version": "2022-06-28",
    "content-type": "application/json"
}

missions_Database_Id = "73267a9a841b45bebd36993a7acef99e"


def readDatabase(target_databaseId):
    readUrl = f"https://api.notion.com/v1/databases/{target_databaseId}/query"

    res = requests.post(readUrl, json=payload, headers=headers)

    data = res.json()

    # Uncomment code below for inspecting json
    json_object = json.dumps(data, indent=4)
    with open(f"../../{target_databaseId[5:]}_database.json", "w") as file:
        file.write(json_object)

    return data


def addMission(target_mission, mission_type, database, telescope_database):
    # Select Status
    if datetime.now() - timedelta(minutes=5) <= target_mission.time_et <= datetime.now():
        status = "capturing"
    elif target_mission.time_et + timedelta(minutes=5) <= datetime.now():
        status = "done"
    else:
        status = "waiting"

    # If duplicate entry exists, do not add
    for object_index in range(0, len(database.objects)):
        test_entry = database.objects[object_index]
        if datetime.now() - timedelta(minutes=5) <= test_entry.date:
            if target_mission.target == test_entry.target:
                if target_mission.time_et == test_entry.date:
                    if target_mission.telescope == test_entry.telescope:
                        return  # the mission already exists

    # get the page id of the related telescope
    telescope_page_id = None

    for telescope in telescope_database.objects:
        if telescope.telescope_name == target_mission.telescope:
            telescope_page_id = telescope.id

    createPage(target_mission.target, target_mission.time_et.strftime("%Y-%m-%dT%H:%M:%S"), status,
               target_mission.telescope, mission_type, telescope_page_id)

    print(f"[+] mission to {target_mission.target}")
    return


def updateMission(page, schedule):
    # First, detect if the photo is currently capturing
    if datetime.now() - timedelta(minutes=5) <= page.date <= datetime.now():
        page.status = 'capturing'
        return

    # Second, detect if mission is done or did not capture
    # link the database page to its associated mission in Slooh
    linked_mission = None

    for mission in schedule.recent_missions:
        if mission.time_et == page.date and mission.target == page.target and mission.telescope == page.telescope:
            # Found a link
            linked_mission = mission
            break

    if linked_mission is not None:  # the mission is over (complete or did not run)
        if linked_mission.status_message == 'Mission accomplished!\nSee your images.':
            page.status = 'done'
        else:
            page.status = 'did not run'

    updateDatabaseStatus(page)


def updateTelescope(page, telescope_availibility: dict):
    updateUrl = f"https://api.notion.com/v1/pages/{page.id}"

    status_message = telescope_availibility[page.telescope_name]

    if "[ONLINE]" in status_message:
        new_status = "Online"
    else:
        new_status = "Offline"

    if "DAYLIGHT" in status_message:
        new_time = "Day \u2600\ufe0f"
    else:
        new_time = "Night \ud83c\udf19"

    updateData = {
        "properties": {
            "Status": {
                "select": {
                    "name": new_status
                }
            },
            "Time": {
                "select": {
                    "name": new_time
                }
            }
        }
    }

    data = json.dumps(updateData)
    res = requests.request("PATCH", updateUrl, headers=headers, data=data)

    return res.status_code


def createPage(title, time, status, telescope, mission_type, telescope_page_id, target_databaseId=missions_Database_Id):
    createUrl = 'https://api.notion.com/v1/pages'

    if status not in ["waiting", "capturing", "done"]:
        raise StatusError(f"{status} not in ['waiting', 'capturing', 'done']")

    if telescope not in ["Chile One", "Chile Two", "Chile Three",
                         "Canary One", "Canary Two", "Canary Three", "Canary Four"]:
        raise StatusError(f"{telescope} not found")

    newPageData = {
        "parent": {"database_id": target_databaseId},
        "properties": {
            "Status": {
                "status": {
                    "name": status}
            },
            "Telescope": {
                "select": {
                    "name": telescope}
            },
            "Date": {
                "type": "date",
                "date": {
                    "start": time,
                    "time_zone": "America/New_York"
                }
            },
            "Target": {
                "title": [
                    {
                        "type": "text",
                        "text": {
                            "content": title
                        }
                    }
                ]
            },
            "Mission Type": {
                "select": {
                    "name": mission_type
                }
            },
            "Telescope Availability": {
                "relation": [
                    {
                        "id": telescope_page_id
                    }
                ]
            }
        }
    }

    data = json.dumps(newPageData)

    res = requests.request("POST", createUrl, headers=headers, data=data)

    # Return the status code after operation was attempted
    return res


def updateDatabaseStatus(page: NotionPage):
    updateUrl = f"https://api.notion.com/v1/pages/{page.id}"

    updateData = {
        "properties": {
            "Status": {
                "status": {
                    "name": page.status
                }
            }
        }
    }

    data = json.dumps(updateData)

    res = requests.request("PATCH", updateUrl, headers=headers, data=data)

    return res.status_code
