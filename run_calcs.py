"""Runs the calcs using the Team class"""
from pymongo import MongoClient

from team import Team

def get_team_list():
    db = MongoClient().scouting_system
    teams = set()
    for match in db.matches.find():
        teams.add(match["team_num"])
    return list(teams)

for team in get_team_list():
    team_obj = Team(team)
    team_obj.run_calcs()
    print("Calcs been ran doe")