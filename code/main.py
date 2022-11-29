from helpers.slooh_integration import build_schedule
from helpers.notion_database import formatDatabase
from helpers.notion_integration import createPage, updateDatabaseStatus
from datetime import datetime, timedelta

schedule = build_schedule()  # get info from slooh
database = formatDatabase()


def addMission(target_mission, mission_type):
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
                        return "mission already exists"

    createPage(target_mission.target, target_mission.time_et.strftime("%Y-%m-%dT%H:%M:%S"), status, target_mission.telescope, mission_type)
    return f"added {target_mission.target}"


# Add current mission to the database
# Right now only 1 of each target object is added to the database which could cause problems
if len(schedule.missions) != 0:
    for mission in schedule.missions:
        print(addMission(mission, "Basic"))

if len(schedule.advanced_missions) != 0:
    for mission in schedule.advanced_missions:
        print(addMission(mission, "Advanced"))


# Update the database with appropriate mission status
for object_index in range(0, len(database.objects)):
    page = database.objects[object_index]

    # Based on mission time, update the status of the mission
    if datetime.now() - timedelta(minutes=5) <= page.date <= datetime.now():
        if page.status == "capturing":
            continue  # no need to update

        page.status = "capturing"
    elif page.date + timedelta(minutes=5) <= datetime.now():
        if page.status == "done":
            continue  # no need to update

        page.status = "done"
    else:
        if page.status == "waiting":
            continue  # no need to update

        page.status = "waiting"

    updateDatabaseStatus(page)
