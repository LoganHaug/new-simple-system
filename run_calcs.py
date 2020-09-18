"""Runs the calcs using the Team class"""
from pymongo import MongoClient

from team import Team


def get_team_list():
    """Grabs the team list based on teams that played in a match

    Returns the team list"""
    db = MongoClient().scouting_system  # Connect to the DB
    teams = set()  # Use a set for exclusivity
    for match in db.matches.find():
        teams.add(match["team_num"])
    return list(teams)  # Cast to list


# Run the calcs
for team in get_team_list():
    team_obj = Team(team)
    team_obj.run_calcs()
    print("Calcs been ran doe")
