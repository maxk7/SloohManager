from datetime import datetime


class NotionPage:
    def __init__(self, database_json_index):
        self.id = database_json_index["id"]
        self.url = database_json_index["url"]

        self.mission_type = database_json_index["properties"]["Mission Type"]["select"]["name"]
        self.telescope = database_json_index["properties"]["Telescope"]["select"]["name"]
        self.date = datetime.strptime(database_json_index["properties"]["Date"]["date"]["start"].split(".")[0],
                                      "%Y-%m-%dT%H:%M:%S")  # the important one
        self.status = database_json_index["properties"]["Status"]["status"]["name"]
        self.target = database_json_index["properties"]["Target"]["title"][0]["plain_text"]
