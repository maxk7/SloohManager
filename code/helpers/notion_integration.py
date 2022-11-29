import requests
import json
import yaml

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

databaseId = "73267a9a841b45bebd36993a7acef99e"


def readDatabase(target_databaseId=databaseId):
    readUrl = f"https://api.notion.com/v1/databases/{target_databaseId}/query"

    res = requests.post(readUrl, json=payload, headers=headers)

    data = res.json()

    # Uncomment code below for inspecting json
    # json_object = json.dumps(data, indent=4)
    # with open("../../database.json", "w") as file:
    #     file.write(json_object)

    return data


def createPage(title, time, status, telescope, mission_type, target_databaseId=databaseId):
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
            }
        }
    }

    data = json.dumps(newPageData)

    res = requests.request("POST", createUrl, headers=headers, data=data)

    # Return the status code after operation was attempted
    return res.status_code


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
