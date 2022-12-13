from helpers.slooh_integration import build_schedule
from helpers.notion_database import readDatabase, formatDatabase
from helpers.notion_integration import updateMission, addMission

schedule = build_schedule()  # get info from slooh
database = formatDatabase()  # get the database from notiion

readDatabase()

# Add current missions (regular then advanced) to the database
if len(schedule.missions) != 0:
    for mission in schedule.missions:
        print(addMission(mission, "Basic", database))

if len(schedule.advanced_missions) != 0:
    for mission in schedule.advanced_missions:
        print(addMission(mission, "Advanced", database))


# Redo status updating based on Recent Missions
for object_index in range(0, len(database.objects)):
    page = database.objects[object_index]
    if page.status == 'waiting':
        updateMission(page, schedule)
