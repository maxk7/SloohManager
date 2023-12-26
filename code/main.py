from helpers.slooh_integration import build_schedule_fetch_telescopes
from helpers.notion_database import formatDatabase
from helpers.notion_integration import updateTelescope, updateMission, addMission

# Database IDs
# Replace these ids with the notion databases you've created
missions_Database_Id = "REPLACE ID!"
telescope_Database_Id = "REPLACE ID!"

schedule, telescope_availability = build_schedule_fetch_telescopes()  # get info from slooh regarding user missions and telescope availibility
missions_database = formatDatabase(missions_Database_Id)  # get the mission database from notion missions database
telescope_database = formatDatabase(telescope_Database_Id)

print(f"[✔] loaded {len(missions_database.objects)} missions and {len(telescope_database.objects)} telescopes")

# Add current missions (regular then advanced) to the database
if len(schedule.missions) != 0:
    for mission in schedule.missions:
        addMission(mission, "Basic", missions_database, telescope_database)

if len(schedule.advanced_missions) != 0:
    for mission in schedule.advanced_missions:
        addMission(mission, "Advanced", missions_database, telescope_database)

print("[✔] added new missions to database")

# Update telescope availability
if len(telescope_database.objects) > 0:
    for telescope in telescope_database.objects:
        updateTelescope(telescope, telescope_availability)

print("[✔] updated telescope availability")

# Update mission status based on 'Recent Missions' category
for object_index in range(0, len(missions_database.objects)):
    page = missions_database.objects[object_index]
    if page.status == 'waiting':
        updateMission(page, schedule)

print("[✔] updated mission status")
