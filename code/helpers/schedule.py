def format_schedule(mission_list, advanced_mission_list):
    if len(mission_list) == 0:
        formatted_basic_missions = None

    elif len(mission_list) > 1:
        formatted_basic_missions = "\n".join([f"│ ╞══{mission}" for mission in mission_list[:-1]])
        formatted_basic_missions += f"\n│ ╘══{mission_list[-1]}"
    else:
        formatted_basic_missions = f"│ ╘══{mission_list[0]}"

    if len(mission_list) == 0:
        formatted_advanced_missions = None
    elif len(advanced_mission_list) > 1:
        formatted_advanced_missions = "\n".join([f"│ ╞══{mission}" for mission in advanced_mission_list[:-1]])
        formatted_advanced_missions += f"\n│ ╘══{advanced_mission_list[-1]}"
    else:
        formatted_advanced_missions = f"│ ╘══{advanced_mission_list[0]}"

    return formatted_basic_missions, formatted_advanced_missions


class Schedule:
    def __init__(self, mission_list, advanced_mission_list, recent_missions):
        self.missions = mission_list
        self.advanced_missions = advanced_mission_list
        self.recent_missions = recent_missions

    def __str__(self):
        f_basic, f_adv = format_schedule(self.missions, self.advanced_missions)

        if f_basic == f_adv is None:
            return "No missions scheduled"

        elif f_adv is None:
            return str(
                f"┌─[Schedule]────────\n╞═[{len(self.missions)} Basic Missions]\n{f_basic}\n╞═[No Advanced Missions]\n└───────────────────")

        elif f_basic is None:
            return str(f"┌─[Schedule]────────\n╞═[No Basic Missions]\n╘═[{len(self.advanced_missions)} Advanced Missions]\n{f_adv}\n└───────────────────")

        # Else
        # if len(self.missions) > 0 and len(self.advanced_missions) > 0:
        else:
            return f"┌─[Schedule]────────\n╞═[{len(self.missions)} Basic Missions]\n{f_basic}\n╞═[{len(self.advanced_missions)} Advanced Missions]\n{f_adv}\n└───────────────────"
