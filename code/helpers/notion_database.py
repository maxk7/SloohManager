from notion_integration import readDatabase
from notion_page import NotionPage


def formatDatabase(databaseid):
    database = readDatabase(databaseid)  # get json database info from notion
    child_objects = []

    # create list of child objects
    for object_index in range(0, len(database["results"]) - 1):
        child_objects.append(NotionPage(database["results"][object_index]))

    return NotionDatabase(child_objects)


class NotionDatabase:
    def __init__(self, list_of_child_objects: list[NotionPage]):
        self.objects = list_of_child_objects
