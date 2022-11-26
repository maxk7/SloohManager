def format_schedule(mission_list, advanced_mission_list):
    formatted_basic_missions = "\n".join([f"│ ╞══[{mission}]" for mission in mission_list[:-1]])

    if len(mission_list) > 0:
        formatted_basic_missions += f"\n│ ╘══[{mission_list[-1]}]"

    formatted_advanced_missions = "\n".join([f"│ ╞══[{mission}]" for mission in advanced_mission_list[:-1]])

    if len(advanced_mission_list) > 0:
        formatted_advanced_missions += f"\n│ ╘══[{advanced_mission_list[-1]}]"

    return formatted_basic_missions, formatted_advanced_missions


class Schedule:
    def __init__(self, mission_list, advanced_mission_list):
        self.missions = mission_list
        self.advanced_missions = advanced_mission_list

    def __str__(self):
        f_basic, f_adv = format_schedule(self.missions, self.advanced_missions)

        if len(self.missions) > 0 and len(self.advanced_missions) > 0:
            return f"┌─[Schedule]────────\n╞═[{len(self.missions)} Basic Missions]\n{f_basic}\n╞═[{len(self.advanced_missions)} Advanced Missions]\n{f_adv}"

        elif len(self.missions) > 0 >= len(self.advanced_missions):
            return str(
                f"┌─[Schedule]────────\n╞═[{len(self.missions)} Basic Missions]\n{f_basic}\n╘═[No Advanced Missions]")

        elif len(self.advanced_missions) > 0 >= len(self.missions):
            return str("┌─[Schedule]────────\n╞═[No Basic Missions]\n╘═[{len(self.advanced_missions)} Advanced Missions]\n{f_adv}")
