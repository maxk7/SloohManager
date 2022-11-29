from datetime import datetime, timedelta


class Mission:
    def __init__(self, target_object, mission_time, mission_telescope, mission_type):
        self.target = target_object
        self.time = datetime.strptime(mission_time, "%b %d, %Y %H:%M %Z")  # mission time in utc
        self.time_et = self.time - timedelta(hours=5)
        self.telescope = mission_telescope
        self.type = mission_type  # advanced or normal mission

    def __str__(self):
        return f"[{self.time}] => [{self.time_et.strftime('%I:%M %p')} ET] " \
               f"{self.target} on {self.telescope}"
